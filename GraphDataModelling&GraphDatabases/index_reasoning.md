1. **Automatic Edge Indexes**

- For **likes** and **produced_by** edge collections, I am relying on the automatic indexes ArangoDB creates on the **_from** and **_to** attributes. These are the most important for my code because they allow the graph traversals in all three queries to follow relationships quickly without scanning every document.

2. **New Manual Index: **brands.name** 

- I added a persistent index to the **name** field in the **brands** collection using **add_persistent_index**.

- **Justification**: Query 2 filters for a specific brand name ("TechCorp") to start the traversal.

- **Impact**: This index prevents a full collection scan for the starting vertex, making the lookup much faster as the number of brands grows

3. **Intentional Omission:** `people.region`

-I decided not to create a new index for the **region** field in the **people** collection, even though I use it as a filter in Query 3.

- ** Justification: **  I checked the seed data and found there are 1,200 people but only 8 different regions.

- **Reasoning:** Because many people share the same region, the selectivity is too low for an index to be efficient. It’s better to avoid the extra memory usage and the slower insertion speeds that another index would cause.

