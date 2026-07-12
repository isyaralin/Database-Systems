import argparse
import json
import sys
from typing import List, Union
from arango import ArangoClient
from pydantic import BaseModel

sys.path.append('../../')
from app.config import arango_config

cfg = arango_config()
client = ArangoClient(hosts=cfg.hosts)
db = client.db(cfg.db_name, username=cfg.username, password=cfg.password)

class QueryResult(BaseModel):
    label: str
    value: Union[str, int, float]

def perform_insert():
    if not db.has_collection('brands'):
        db.create_collection('brands')
    if not db.has_collection('produced_by'):
        db.create_collection('produced_by', edge=True)

    db.collection('brands').add_persistent_index(fields=['name'])

    brands = [
        {"_key": "b1", "name": "TechCorp", "country": "USA"},
        {"_key": "b2", "name": "EuroApp", "country": "Czechia"},
        {"_key": "b3", "name": "AsiaSoft", "country": "Japan"},
        {"_key": "b4", "name": "GlobalGear", "country": "Germany"},
        {"_key": "b5", "name": "NordicTools", "country": "Sweden"}
    ]
    db.collection('brands').import_bulk(brands, overwrite=True)

    edges = [
        {"_from": "products/1", "_to": "brands/b1", "type": "original"},
        {"_from": "products/2", "_to": "brands/b2", "type": "original"},
        {"_from": "products/3", "_to": "brands/b3", "type": "original"},
        {"_from": "products/4", "_to": "brands/b4", "type": "original"},
        {"_from": "products/5", "_to": "brands/b5", "type": "original"}
    ]
    db.collection('produced_by').import_bulk(edges, overwrite=True)
    return "-> Insertion complete."

def query_1():
    aql = """
    FOR b IN brands
      LET p_list = (FOR p IN 1..1 INBOUND b._id produced_by RETURN p)
      RETURN { label: b.name, value: LENGTH(p_list) }
    """
    cursor = db.aql.execute(aql)
    return [QueryResult.model_validate(row).model_dump() for row in cursor]

def query_2():
    aql = """
    FOR b IN brands
      FILTER b.name == "TechCorp"
      FOR v IN 2..2 INBOUND b._id produced_by, likes
        COLLECT full_name = CONCAT(v.given_name, " ", v.family_name) WITH COUNT INTO total
        RETURN { label: full_name, value: total }
    """
    cursor = db.aql.execute(aql)
    return [QueryResult.model_validate(row).model_dump() for row in cursor]

def query_3():
    aql = """
    FOR p IN people
      FILTER p.region == "EU-CZ"
      FOR item IN 1..1 OUTBOUND p._id likes
        FOR brand IN 1..1 OUTBOUND item._id produced_by
          COLLECT b_name = brand.name WITH COUNT INTO likes_count
          SORT likes_count DESC
          LIMIT 5
          RETURN { label: b_name, value: likes_count }
    """
    cursor = db.aql.execute(aql)
    return [QueryResult.model_validate(row).model_dump() for row in cursor]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--insert", action="store_true")
    parser.add_argument("--q1", action="store_true")
    parser.add_argument("--q2", action="store_true")
    parser.add_argument("--q3", action="store_true")
    args = parser.parse_args()

    if args.insert:
        print(perform_insert())
    elif args.q1:
        print(json.dumps(query_1(), indent=2))
    elif args.q2:
        print(json.dumps(query_2(), indent=2))
    elif args.q3:
        print(json.dumps(query_3(), indent=2))

