# Query Catalog: Polystore Federated Analytics

## Query 1: Top Engaged Customers Profiling
* **Business Meaning:** Identifies highly active customers by analyzing their purchase history, how much they purchased, and ensuring that they have an active social profile and have opted into marketing for targeted campaigns.

* **Systems & Catalogs Used:** MongoDB (`shop.people`, `shop.orders_flat`), Cassandra (`shopstream.user_profile_by_id`), PostgreSQL (`public.social_people`).
* **SQL Constructs:** * **Cross-System Joins:** Joins across 3 distinct database systems using a shared identifier.
  * **Subquery:** Calculates total orders dynamically from MongoDB.
  * **Aggregation:** Uses `COUNT(*)` inside the subquery.
* **Output Schema:** `customer_id`, `full_name`, `region`, `marketing_opt_in`, `total_orders`.

## Query 2: Social Recommendation Engine
* **Business Meaning:** Generates personalized title recommendations by finding what a specific user's social connections and what they have liked 
* **Systems & Catalogs Used:** PostgreSQL (`public.follows`, `public.likes`), Cassandra (`shopstream.title_page_by_id`).
* **SQL Constructs:**
  * **WITH Clause:** Computes social evidence as a readable step before the final query.
  * **Aggregation:** Uses `COUNT(l.user_id)` to rank recommendations by popularity among friends.
  * **Cross-System Join:** Bridges relational edges with wide-column metadata 
* **Output Schema:** `follower_user_id`, `recommended_title`,`genres`, `evidence_count`.

