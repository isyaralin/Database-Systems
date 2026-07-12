**Overview** 

ArangoDB's multi-model architecture allows to combine filtering with graph-centric relationship traversals like documents. Document views are efficient for reading isolated profiles, but the graph view is better for answering questions about reachability and recommendations across entities.

1) **Query1: Manufacturing Portfolio Analysis **
- ** Business Meaning **: This query provides deep insight into the inventory distribution by calculating how many unique products are associated with each brand 

* **AQL Clauses used**: `FOR`, `LET`, `RETURN`, and ** Aggregation** via `LENGTH()`

* ** Graph Justification **: By using a 1-hop inbound traversal frm a **Brand** vertex to **Product** vertices via ** produced_by** edge, we can count inventory without needing a counter on Brand document.

2) ** Query2: Brand Loyalist Discovery**
* **Business Meaning:** This query identifies customers who have a direct interest in a specific manufacturer by finding people who "Like" the products that the brand produces.

* **AQL Clauses used:** `FOR`, `FILTER`, `COLLECT ... WITH COUNT` and 2-hop Bounded Traversal.

* ** Graph Justification **: This requires a 2-hop relationship path: **Brand** ← **produced_by** ← **Product** ← **likes** ← **Person**. Bounded traversal is essential here to link a specific manufacturer back to the consumer through the product intermediate.

3) **Query3: Regional Brand Popularity Ranking**
* **Business Meaning:** This query serves as a market research tool to identify which brands are currently the most popular within a specific geographic region

* **AQL Clauses used:** `FOR`, `FILTER`, `COLLECT`, `SORT`, `LIMIT` and 2-hop Bounded Traversal.

* **Graph Justification**: The query starts by filtering a specific document attribute and then expands outward into the graph: **Person** → **likes** → **Product** → **produced_by** → **Brand**. Using the graph model allows me to aggregate "Likes" across different products to determine total brand strength in a specific area. 


