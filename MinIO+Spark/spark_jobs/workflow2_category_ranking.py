"""
wrokflow2_category_ranking.py

Wrokflow 2: Top Categories per Region

Bussiness Question:
	Which product categories generate the highest total revenue in each region

Input s3a://data/raw/transactions.csv
Output: s3a://data/analytics/top_categories_by_region/  (Parquet)

Run With:
docker compose exec -T spark /opt/spark/bin/spark-submit \
    --master "local[*]" \
    /opt/spark-jobs/workflow2_category_ranking.py

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


def run_category_ranking(input_path: str, output_path: str, app_name: str) -> None:
    spark = build_spark(app_name)

    # Load CSV as distributed DataFrame
    df = spark.read.csv(input_path, header=True, inferSchema=True)

    print("=== Schema ===")
    df.printSchema()

    # remove duplicate transactions and the invalid amounts if exists 
    df = (df
          .filter(F.col("amount") > 0)
          .dropDuplicates(["transaction_id"]))

    #  total revenue and transaction count per region
    df = (df
          .groupBy("region", "product_category")
          .agg(
              F.sum("amount").alias("total_revenue"),
              F.count("*").alias("transaction_count")
          )
          .withColumn("revenue_rounded", F.round(F.col("total_revenue"), 2))
          .orderBy(F.col("region").asc(), F.col("total_revenue").desc()))

    print("=== Execution Plan ===")
    df.explain()

    print("=== Total Rows ===")
    print(df.count())

    print("=== Top Categories per Region ===")
    df.show(50, truncate=False)

    # Write as parquet
    (df.write
       .mode("overwrite")
       .partitionBy("region")
       .parquet(output_path))

    spark.stop()


def parse_args():
    p = argparse.ArgumentParser(prog="workflow2_category_ranking")
    p.add_argument("--input",    default="s3a://data/raw/transactions.csv")
    p.add_argument("--output",   default="s3a://data/analytics/top_categories_by_region")
    p.add_argument("--app-name", default="TopCategoriesByRegion")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_category_ranking(args.input, args.output, args.app_name)
