# Homework 4: Polystores (Solo Version)

## Setup
1. Start the polystore environment: `docker compose up -d`
2. Seed the databases: `python3 -m python.seed_all`
3. Activate the virtual environment: `source .venv/bin/activate`

## Execution
Run the federated queries via the Python application using the SQLAlchemy Trino dialect:
* Run Query 1: `python3 implementation/main.py --q1`
* Run Query 2: `python3 implementation/main.py --q2`

## Included Catalogs
* `mongodb` (MongoDB)
* `cassandra` (Apache Cassandra)
* `postgresql` (PostgreSQL)
* `system` (Trino runtime)

