# Designing Analytical Workflows over Object Storage (MinIO + Spark)

## Business Context & Scenario
A fast-growing digital analytics company operating in a data-intensive environment (such as professional sports analytics, horse breeding/racing statistics, zoo animal health tracking, e-commerce for pet supplies, wildlife observation data, ride-sharing platform data, climate measurements, or online gaming telemetry) collects large volumes of operational data daily. 

The enterprise is gradually transitioning toward a modern data lake architecture. Raw data arrives as CSV files, is stored directly in an object storage layer (MinIO, S-3 compatible), and all analytical processing is performed in batch mode using Apache Spark. The daily data volume is increasing rapidly and may exceed millions of records per day. There is no traditional relational database involved in the analytical pipeline.

---

## Role & Assignment Parameters
In this project, you act as both the Solutions Architect and the Data Engineer. You must design and implement two distinct analytical workflows over the provided dataset using the Apache Spark DataFrame API.

### Core Architecture Requirements
* **Ingestion:** Convert raw CSV datasets into the optimized, column-oriented Apache Parquet format.
* **Storage Optimization:** Implement an explicit partitioning strategy to improve query performance.
* **Lifecycle Management:** Use `spark-submit` to execute jobs and stop the `SparkSession` explicitly to ensure healthy cluster resource cleanup.
* **Execution Profiling:** Call `.explain()` on your final DataFrames to output the underlying logical and physical transformation plans.

### Workflow Engineering Constraints
Each of the two workflows must answer a clearly formulated business question and satisfy the following structural requirements:
* Use at least **5 different meaningful transformations** (e.g., `select`, `filter`, `withColumn`, `groupBy`, `agg`, `join`, `orderBy`, `dropDuplicates`, `cast`).
* Use at least **2 different actions** (e.g., `count`, `show`, `write`, `collect`).
* Include at least **one aggregation**, **one filter**, and **one derived column** per workflow.

---

## Required Deliverables

### 1. Workflow Documentation (`workflow_design.md`)
For each workflow, you must explicitly document:
* The core business question being answered.
* The sequential logical transformation plan.
* The expected output schema (field names and strict data types).
* The targeted output path/bucket destination in MinIO.

### 2. Architectural Analysis (`performance_reasoning.md`)
Provide engineering justifications detailing:
* **Partitioning Choices:** Why the specific partition key was selected relative to data cardinality.
* **Storage Formats:** Why Parquet is fundamentally preferable to flat CSV files for analytical workloads.
* **Distributed Mechanics:** How wide-dependency operations (like `groupBy`) introduce network-heavy data shuffles across a distributed cluster.

### 3. Repository Directory Layout
```text
homework1_solo/
├── README.md
├── task.md
├── workflow_design.md
├── performance_reasoning.md
├── spark_jobs/
└── LICENSE
