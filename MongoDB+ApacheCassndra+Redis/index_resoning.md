## Existing Indexes

* **`_id`**: Default index on all collections for primary key lookups.
* **`email_1`**: Unique index on the `people` collection (as seen in the DuplicateKeyError during testing) to ensure data integrity.

## Recommended Additional Indexes

1. **Orders: `{ "region": 1, "order_date": 1 }`**


   * **Reasoning:** This compound index would speed up Q1 and Q2. It allows MongoDB to filter by region and then find the relevant date range immediately after, without a full collection scan.

2. **Orders: `{ "order_status": 1 }`**
   * **Reasoning:** I used this for query 5. Since audits usually involve a small fraction of total orders, an index here makes the very hard search very fast 

3. **Products: `{ "category": 1 }`**
   * **Reasoning:** I used this for query 3. This allows the database to jump straight to the office or hardware segments.

