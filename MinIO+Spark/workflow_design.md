WORKFLOW1

Workflow1 calculates daily revenue for a specific region to show growth trends over time.

Extraction: 
    Connected the local network to MinIO to reach the transactions.csv file, and loaded it into the Spark's memory as a distributed DataFrame

Filtering: 
    The forkflow ignores the transactions were the amount was 0 or less (This way it gets rid of the bad data)

    It discarded all the transactions from the other countries and kept the rows where the region was EU-CZ

Transformations: Simplified timestamp into cleaner date

Aggregation:
     This workflow groups all the transactions by the date and the calculated:
        Total Revenue
        Transaction Count
        Average Sale Value

Optimization:
    Rounded money to 2 decimal for better readability 

Loading:
    Converted data from CSV format into Parquet and saved it back to MinIO 


Specific Question: 
    What is the daily revenue trend for the EU-CZ region?

Output Path in MinIO: 
    s3a://data/analytics/daily_revenue_by_region/

WORKFLOW2:

Workflow2 ranks product categories by total revenue within each region to identify the highest-performing sectors geographically.

Extraction:
    Connected to the MinIO S3 endpoint and reached transactions.csv file and loaded it into a distributed DataFrame.

Filtering: 
    It filtered out the bad data (where amount was ≤0)

    Uses dropDuplicates to ensure that if system recorded the same transaction ID twice, the report of the revenue stays consistent.

Aggregation: 
    Orginized the receipts into groups based on Region and Product Category.
    For every group it calculated:
        The Total Revenue
        The Transaction Count 

Formatting:
    Used F.round for better readability 

Sorting:
    It sorted the list to find the "Best Seller" category for each region.

Loading: Saved the results into MinIO using Parquet.

Specific Question: 
    Which product categories generate the highest total revenue within each region?

Output Path in MinIO: 
    s3a://data/analytics/category_ranking_by_region/