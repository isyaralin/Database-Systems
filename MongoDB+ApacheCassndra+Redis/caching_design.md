I selected **Query 2 (Top Categories)** for caching because category revenue is expensive to compute (requires `$unwind` and multiplication across 100k records) but the results do not change second-by-second. 

## Key Design

* **Pattern:** `top_cat:{region}`
* **Example:** `top_cat:EU-CZ`
* **Rationale:** 

I including the region in the key to ensure that an analyst in Prague doesn't accidentally receive the cached results intended for an analyst in London. This way I actually filtered the regions for the application.

## TTL & Invalidation

* **TTL:** 3600 seconds (1 hour). This balances data freshness with database load reduction. (As mentioned in lecture)

* **Invalidation Strategy:** I used a **Manual Invalidation** approach. When `main.py --insert` is called, the script executes `r.flushdb()`.

* **Reasoning:** Since a manual insert or update (Mutation) changes the underlying "Source of Truth," we must clear the cache to prevent the application from serving "Stale Data."

## Why other queries are NOT cached

* **Q1 (Revenue Trend):** Trends are viewed over custom, varying time ranges. Caching every possible date range would mix up the data

* **Q5 (Audit):** Audit data must be completely accurate and reflect the most recent database writes. A single difference between the actual time may cause business to get in trouble with audit purposes. 

