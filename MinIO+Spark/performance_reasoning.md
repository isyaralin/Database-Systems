1) Why Parquet over CSV

CSV is a plain text and row oriented format. It uses commas to separate fields (the columns) and new lines to separate records (the rows) 

Because of this, for computing a single aggregation (like sum("amount")), Spark must read and parse every column of every row. This would also require parsing the columns that we actually don't need.

This is the main reason why we nead Parquet. Because:

Parquet is in a columnar, binary format. Unlike CSV, it stores the values for each column separately. This way, Spark reads only the columns required by the query. It applies the functionalities like comprassion, min/max, etc. to per row group allowing Spark to skip chunks of data that does not match a filter. This allows faster execution for larger workloads.

2) Partitioning Choice

Workflow1: Partitioned by Date 

The output is daily revenue data. The query is based on the time. By partitioning by date we let Spark to only read the date format in the workload, date = YYYY-MM-DD directories and ignoring all other directories that the workload has. 

Workflow2: Partitioned by Region 

The output is category rankings per region. The quey is region based. Partitioning by region means only the region=EU/ directory is read for the query.

3) How groupBy Introduces Shuffle

When Spark executes groupBy("date").agg(sum("amount")), it cannot compute the final aggresion locally on each executor because rows with the same date may be spread across multiple partitions on different executers.

To fix this issue Spark applies:
Mapping: Each executor computers partial aggregates for the rows it holds locally

Shuffle: Spark redistributes data across executors by hashing the group key (date)

Reduce: Each executor finalizes the aggregattion for the assigned keys.


