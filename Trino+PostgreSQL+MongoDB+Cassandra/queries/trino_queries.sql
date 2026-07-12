-- Query 1: Customer Activity and Social Engagement Profiling
-- Systems: MongoDB, Cassandra, PostgreSQL
-- Features: 3-way join, Subquery, Aggregation

SELECT 
    m.id AS customer_id,
    m.given_name || ' ' || m.family_name AS full_name,
    c.region,
    c.marketing_opt_in,
    (SELECT COUNT(*) FROM mongodb.shop.orders_flat o WHERE o.customer_id = m.id) AS total_orders
FROM mongodb.shop.people m
JOIN cassandra.shopstream.user_profile_by_id c ON c.user_id = m.id
JOIN postgresql.public.social_people p ON p.user_id = m.id
WHERE c.marketing_opt_in = true
ORDER BY total_orders DESC
LIMIT 10;

-- Query 2: Cross-Model Social Recommendation Engine
-- Systems: PostgreSQL, Cassandra
-- Features: WITH clause (CTE), Aggregation, Joins across systems

WITH followed_likes AS (
    SELECT 
        f.follower_user_id, 
        l.item_id AS title_id, 
        COUNT(l.user_id) as evidence_count
    FROM postgresql.public.follows f
    JOIN postgresql.public.likes l ON f.followed_user_id = l.user_id
    WHERE l.item_type = 'TITLE'
    GROUP BY f.follower_user_id, l.item_id
)
SELECT 
    fl.follower_user_id,
    t.name AS recommended_title,
    t.genres,
    fl.evidence_count
FROM followed_likes fl
JOIN cassandra.shopstream.title_page_by_id t ON t.title_id = fl.title_id
WHERE fl.follower_user_id = 1
ORDER BY fl.evidence_count DESC
LIMIT 10;

