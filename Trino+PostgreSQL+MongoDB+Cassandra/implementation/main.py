import argparse
from sqlalchemy import create_engine, text
from dataclasses import dataclass

engine = create_engine("trino://student@localhost:8080/system")

@dataclass
class CustomerProfile:
    customer_id: int
    full_name: str
    region: str
    marketing_opt_in: bool
    total_orders: int

@dataclass
class Recommendation:
    follower_user_id: int
    recommended_title: str
    genres: str
    evidence_count: int

def run_query_1():
    sql = """
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
        LIMIT 10
    """
    print("--- Query 1: Top Engaged Customers (Federated) ---")
    with engine.connect() as conn:
        rows = conn.execute(text(sql)).mappings().all() 
        
        profiles = [CustomerProfile(**row) for row in rows]
        
        for p in profiles:
            print(f"ID: {p.customer_id} | Name: {p.full_name} | Region: {p.region} | Orders: {p.total_orders}")

def run_query_2():
    sql = """
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
        WHERE fl.follower_user_id = :target_user
        ORDER BY fl.evidence_count DESC
        LIMIT 10
    """
    print("--- Query 2: Social Recommendations (Federated) ---")
    with engine.connect() as conn:
        rows = conn.execute(text(sql), {"target_user": 1}).mappings().all()
        
        recommendations = [Recommendation(**row) for row in rows]
        
        for r in recommendations:
            print(f"Title: {r.recommended_title} | Genres: {r.genres} | Evidence: {r.evidence_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--q1", action="store_true", help="Run Query 1")
    parser.add_argument("--q2", action="store_true", help="Run Query 2")
    args = parser.parse_args()

    if args.q1:
        run_query_1()
    if args.q2:
        run_query_2()

