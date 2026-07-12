**Download material and data**

# Linux/macOS:
curl -L -o lab01-minio-spark.zip "https://gitlab.mff.cuni.cz/teaching/ndbi040/web/-/archive/master/web-master.zip?ref_type=heads&path=lab01-minio-spark"
unzip lab01-minio-spark.zip
cd web-master-lab01-minio-spark
cd lab01-minio-spark
ls -l

# Windows:
curl.exe -L -o lab01-minio-spark.zip "https://gitlab.mff.cuni.cz/teaching/ndbi040/web/-/archive/master/web-master.zip?ref_type=heads&path=lab01-minio-spark"
tar -xf lab01-minio-spark.zip
cd web-master-lab01-minio-spark
cd lab01-minio-spark
dir




1) Project Overview 

This project contains two PySpark workflows designed to process raw transaction data (transactions.csv) stored in a MinIO S3 bucket and save the result in an optimized Parquet format 

2) Construction and Methodology 

I constructed these workflows by following Skeleton Pattern and Architecture provided in the Lab1 materials.

* Both scripts use centralized build_spark() function to handle S3A configurations and connection to the MinIO cluster

* I implemented argparse to allow the script to be flexible, such as filtering for specific regions (like I did --region EU-CZ)

* I started by processing raw CSV, then filtered according to the question structure and requirements, aggreagted by the business dimension and writing them to optimized Parquet partitions. 

3) Sources 

I kept the structure and logic of the implementations similar to the examples and lines from the Lab1 materials. 

* Lab Exercises: I adapted the fundamental "Group-By-Aggregate" from the Lab Exercises 1.3 and 1.4. I expanded on these by adding rounding and dropDuplicates.

* The choice to use Parquet as a columnar storage format and Partitioning (by Date and Region) was directly based on the performance optimization strategies discussed in Lecture 1

* I designed Workflow2 to specifically address regional performance by ranking categories.


4) Use of AI Tools 

I used ChatGpt for collabration and for technical questions that I couldn't find answers in the lecture notes.

These are the cases I used AI mainly:

During development, I initially attempted to use th esimplified one line S3 connection string mentioned in the lab materials. However my code crashed because the Spark environment required explicit configuration to comminucate with a local MinIO container (S3).

First, I tried to change the code for the environment to run without the warnings I got. But no change I made fixed the problem. This is where I sarted to discuss the output of the terminal and the issue I was facing with AI tools. And I learned that I need the folowing part of my code (specifically the .config() part, the keys and other informations, such as "http://minio:9000", "spark.hadoop.fs.s3a.access.key", "minioadmin", are implemented completely by me) 

```
   .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.aws.credentials.provider",
                "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
        .getOrCreate()

```

I learned that while the one-line code works for stansard cloud environments, local development in Docker requires configuration to bridge the gap between Spark and MinIO
    
I also found some discussions in Gitlab, and StackOverflow 
https://gist.github.com/harshavardhana/93c28c28bf700243b3199748427a62a4

and similar implementations for the .config()

I used AI tools as a mentor to discuss my ideas, approaches, the business question quality and my idea, and for the debugging the issue I faced. I implemented the rest of the code following the lecture and lab content and using the lab skeletons. 

5) How To Run

Start the Cluster docker compose up -d

Run Workflow 1 (Daily Revenue):
    docker compose exec -T spark /opt/spark/bin/spark-submit /opt/spark-jobs/workflow1_revenue_trend.py --region EU-CZ

Run Workflow 2 (Category Rankings):
    docker compose exec -T spark /opt/spark/bin/spark-submit /opt/spark-jobs/workflow2_category_ranking.py

(docker compse exec can be replaced with ./mc.sh upon creating the mc.sh)

