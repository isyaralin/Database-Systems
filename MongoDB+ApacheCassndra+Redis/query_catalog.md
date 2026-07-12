# Query Catalog

## Q1: Daily Revenue Trend


**Business Meaning:** 

This query allows business owners to track revenue in a specific region over the time. This allows owners to see when the revenue is down and when its high through out the seasons. 

**Implementation:** 

Filters by `region`, uses `$substr` to normalize timestamps into YYYY-MM-DD format, and groups by date to sum `total_price`.

**Structure Support:** 

The embedded `total_price` in the Order document avoids the need to join with individual items, making this operation very high-speed 

## Q2: Top 5 Categories by Revenue

**Business Meaning:** 

Finds out which products are selling in a region more, helping with inventory procurement and marketing focus.

**Implementation:** 

Uses `$unwind` to flatten the items array and `$multiply` on `unit_price` and `quantity`.

**Structure Support:** 

Having the `category` and `unit_price` embedded inside the `items` array allows this query to run entirely within the `orders` collection.

## Q3: Product Price Analysis

**Business Meaning:** 
This query determines the pricing strategy for a specific category so the business can ensure that their base prices are optimal.

**Implementation:** 

Groups products by name and calculates the `$avg` of the `base_price` field.

**Structure Support:** 

This query targets the `products` collection directly, utilizing the flat structure for rapid aggregation.

## Q4: Top 5 Spenders
**Business Meaning:** 

This query identifies the top 5 spenders all the time depending on their purchases. This can give option for owners to identify their loyal customers and maybe make them special offers in return. 

**Implementation:** 

Groups the entire `orders` collection by `customer.id` and sorts by the sum of `total_price`.

**Structure Support:**

 Embedding the `customer.id` within the `Order` document ensures we don't need to look up the `People` collection to identify spending power.

## Q5: Status Audit
**Business Meaning:** 

Operational oversight. Allows logistics teams to pull a detailed item list for orders requiring special attention 

**Implementation:** 

Filters by `order_status` and projects only the necessary fields (`order_id`, `region`, `item_name`).

