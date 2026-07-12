import json
import redis
import argparse
from mongoengine import *

connect("shop", host="mongodb://localhost:27017")
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

class People(Document):
    meta = {"collection": "people", "strict": False}
    given_name = StringField()
    family_name = StringField()
    email = StringField()

class Product(Document):
    meta = {"collection": "products", "strict": False}
    name = StringField()
    category = StringField()
    weight_kg = FloatField()
    base_price = DecimalField()

class Customer(EmbeddedDocument):
    id = IntField(required=True)
    given_name = StringField()
    family_name = StringField()

class Item(EmbeddedDocument):
    product_id = IntField(required=True)
    name = StringField()
    category = StringField()
    unit_price = DecimalField()
    quantity = IntField()

class Order(Document):
    meta = {"collection": "orders", "strict": False}
    region = StringField()
    order_date = StringField()
    order_status = StringField()
    total_price = DecimalField()
    customer = EmbeddedDocumentField(Customer)
    items = ListField(EmbeddedDocumentField(Item))

def get_revenue_trend(region):
    pipeline = [
        {"$match": {"region": region}},
        {"$group": {
            "_id": {"$substr": ["$order_date", 0, 10]},
            "revenue": {"$sum": "$total_price"}
        }},
        {"$sort": {"_id": 1}}
    ]
    return list(Order.objects.aggregate(*pipeline))

def get_top_categories_cached(region):
    cache_key = f"top_cat:{region}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    pipeline = [
        {"$match": {"region": region}},
        {"$unwind": "$items"},
        {"$group": {
            "_id": "$items.category", 
            "revenue": {"$sum": {"$multiply": ["$items.unit_price", "$items.quantity"]}}
        }},
        {"$sort": {"revenue": -1}},
        {"$limit": 5}
    ]
    results = list(Order.objects.aggregate(*pipeline))
    r.set(cache_key, json.dumps(results, default=str), ex=3600)
    return results

def get_category_analysis(category):
    pipeline = [
        {"$match": {"category": category}},
        {"$group": {"_id": "$name", "avg_price": {"$avg": "$base_price"}}},
        {"$project": {"product_name": "$_id", "avg_price": {"$round": ["$avg_price", 2]}, "_id": 0}}
    ]
    return list(Product.objects.aggregate(*pipeline))

def get_top_spenders():
    pipeline = [
        {"$group": {"_id": "$customer.id", "total_spent": {"$sum": "$total_price"}}},
        {"$sort": {"total_spent": -1}},
        {"$limit": 5},
        {"$project": {"customer_id": "$_id", "total_spent": 1, "_id": 0}}
    ]
    return list(Order.objects.aggregate(*pipeline))

def get_status_audit(status):
    pipeline = [
        {"$match": {"order_status": status}},
        {"$unwind": "$items"},
        {"$project": {"order_id": "$_id", "item": "$items.name", "region": 1, "_id": 0}}
    ]
    return list(Order.objects.aggregate(*pipeline))

def perform_mutations():
    People.objects(email="alice@example.com").delete()
    Product.objects(name="Lab Monitor").delete()
    Order.objects(order_date="2026-04-21").delete()
    People(given_name="Alice", family_name="Lab", email="alice@example.com").save()
    Product(name="Lab Monitor", category="Hardware", weight_kg=5.5, base_price=150.00).save()
    Order(
        region="EU-CZ", order_date="2026-04-21", order_status="NEW", total_price=150.00,
        customer=Customer(id=1, given_name="Alice", family_name="Lab"),
        items=[Item(product_id=1, name="Lab Monitor", category="Hardware", unit_price=150.00, quantity=1)]
    ).save()
    Order.objects(order_date="2026-04-21").update(set__order_status="AUDITED_SOLO")
    r.flushdb()
    return "-> Mutations complete (cleaned old data first)."

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--q1", help="Revenue Trend")
    parser.add_argument("--q2", help="Top Categories (Cached)")
    parser.add_argument("--q3", help="Category Prices")
    parser.add_argument("--q4", action="store_true", help="Top Spenders")
    parser.add_argument("--q5", help="Status Audit")
    parser.add_argument("--insert", action="store_true", help="Perform mutations")
    args = parser.parse_args()

    if args.insert:
        print(perform_mutations())
    elif args.q1:
        print(json.dumps(get_revenue_trend(args.q1), indent=4, default=str))
    elif args.q2:
        print(json.dumps(get_top_categories_cached(args.q2), indent=4, default=str))
    elif args.q3:
        print(json.dumps(get_category_analysis(args.q3), indent=4, default=str))
    elif args.q4:
        print(json.dumps(get_top_spenders(), indent=4, default=str))
    elif args.q5:
        print(json.dumps(get_status_audit(args.q5), indent=4, default=str))
