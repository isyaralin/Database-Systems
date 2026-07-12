# Polystore and Federated Query Processing (Trino + PostgreSQL + NoSQL)

## Business Context & Evolution
This project represents the fourth maturity phase of the enterprise data architecture. Over the course of the previous architectural iterations, data was decentralized into specialized storage layers based on workload affinity: analytical batch drops (MinIO + Spark) and application-facing transactional layers (MongoDB/Cassandra). 

To prevent data silos and eliminate the need for engineering complex, multi-database extraction scripts at the application layer, the enterprise has adopted a **Polystore Architecture**. By introducing **Trino** as a high-performance distributed SQL query engine, developers can execute unified federated queries bridging relational systems (PostgreSQL) and operational document or column-family storage arrays through a single, abstracted SQL access layer.

---

## Role & Assignment Parameters
In this solo version, you act as both the Solutions Architect and Data Engineer. Your objective is to map data across disparate engine catalogs and implement federated Python workflows utilizing SQLAlchemy.

### Core Architectural Requirements
* **Unified Query Engine:** Connect to the prepared Trino polystore instance to query underlying systems via ANSI SQL without system-specific database drivers.
* **Storage Diversity:** Every single federated query must actively query and join data from at least **two underlying engines**, establishing cross-system lookups across:
  * Relational Datastores (**PostgreSQL**)
  * NoSQL Datastores (**MongoDB** or **Apache Cassandra**)
* **Application Mapping:** Implement query execution pipelines in Python using SQLAlchemy, translating the untyped tabular row returns into explicit Python application data structures (dictionaries, dataclasses, or custom DTOs).

### Technical & Query Engineering Constraints
Your federated query configurations must satisfy the following syntax boundaries:
* **Analytical Scope:** Implement **2 meaningful federated SQL queries** that provide cross-domain business intelligence.
* **Join Complexity:** Each query must join at least **3 distinct tables, collections, or column-families** across the catalog boundaries using consistent identifiers.
* **SQL Constructs:** Across your query set, you must explicitly integrate:
  * At least one Common Table Expression (`WITH` clause) for structured readability.
  * At least one SQL subquery evaluating deep criteria logic.
  * At least one SQL aggregation function processing statistical returns.
* **Command Line Controls:** Route pipeline executions directly from `main.py` accepting explicit execution hooks (`--q1`, `--q2`).

---

## Required Deliverables

### 1. Polystore Mapping & Catalog Documentation (`query_catalog.md`)
Comprehensive structural documentation including:
* Clear descriptions of the 2 federated queries, their underlying business KPIs, and cross-system join keys.
* A breakdown of the exact SQL structural operations utilized alongside the explicit output schema of the typed application results.

### 2. Execution Queries (`queries/trino_queries.sql`)
The standalone, raw SQL script collection containing the optimized federated query strings executed by the application connector layer.

### 3. Application Implementation Layer (`implementation/`)
```text
homework4_solo/
├── README.md               # Environment execution notes and connected Trino catalog layouts
├── query_catalog.md        # Deep dive into business logic, cross-system joins, and schemas
├── queries/
│   └── trino_queries.sql   # Native SQL script blueprints containing the federated queries
├── implementation/         # Executable Python script directory
│   └── main.py             # Main routing application supporting CLI flags (--q1, --q2)
└── LICENSE                 # Open-source licensing parameters
