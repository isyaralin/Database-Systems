"""
workflow1_revenue_trend.py
==========================
NDBI040 Homework 1 – Solo Version
Workflow 1: Daily Revenue Trend by Region

Business Question:
    What is the daily revenue and transaction count per day for a selected region?

Input:   s3a://data/raw/transactions.csv
Output:  s3a://data/analytics/daily_revenue_by_region/  (Parquet, partitioned by date)

Run with:
docker compose exec -T spark /opt/spark/bin/spark-submit \ --master "local[*]" \ /opt/spark-jobs/workflow1_revenue_trend.py \ --region EU-CZ

After running the command you will see 180 rows of results. 
"""

import argparse

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def build_spark(app_name: str) -> SparkSession:
    return (
        SparkSession.builder
        .appName(app_name)
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.aws.credentials.provider",
                "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
        .getOrCreate()
    )


def run_workflow1(input_path: str, output_path: str, region: str, app_name: str) -> None:
    spark = build_spark(app_name)

    # Load CSV as DataFrame
    df = spark.read.csv(input_path, header=True, inferSchema=True)

    print("==Schema==")
    df.printSchema()

    # Get the date column from timestamp
    df = df.withColumn("date", F.to_date(F.col("timestamp"), "yyyy-MM-dd HH:mm:ss"))

    # Filter the region you selected
    df = df.filter(F.col("region") == region)

    # Dont take the invalid ones
    df = df.filter(F.col("amount") > 0)

    # Get the infos you need 
    df = df.select("date", "amount")

    # groupBy date, compute revenue metrics
    df = df.groupBy("date").agg(
        F.sum("amount").alias("total_revenue"),
        F.count("*").alias("transaction_count"),
        F.avg("amount").alias("avg_transaction_value")
    )

    df = df.withColumn("revenue_rounded", F.round(F.col("total_revenue"), 2))
  
    # sort them in order
    df = df.orderBy(F.col("date").asc())

    print("==Execution Plan==")
    df.explain()

    #count result rows
    print("==Total Days with Data==")
    print(df.count())

    #show sample output
    print("Sample Output")
    df.show(10, truncate=False)

    # write as Parquet (partion the date)
    (df.write
       .mode("overwrite")
       .partitionBy("date")
       .parquet(output_path))

    # Stop the Spark
    spark.stop()


def parse_args():
    p = argparse.ArgumentParser(prog="workflow1_revenue_trend")
    p.add_argument("--input",    default="s3a://data/raw/transactions.csv")
    p.add_argument("--output",   default="s3a://data/analytics/daily_revenue_by_region")
    p.add_argument("--region",   default="NA")
    p.add_argument("--app-name", default="DailyRevenueTrendByRegion")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_workflow1(args.input, args.output, args.region, args.app_name)
