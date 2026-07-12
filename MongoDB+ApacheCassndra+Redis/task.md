# Query-Driven Design and Application Integration over NoSQL Systems (MongoDB + Redis)

## Business Context & Evolution
This project directly extends the analytical data lakehouse architecture designed in Homework 1. While the primary stage focused on large-scale raw file processing (via MinIO + Spark), the enterprise is now transitioning toward supporting real-time, application-facing data access layers.

To power responsive backend application endpoints with predictable latencies, the company is moving away from purely batch analytics toward application-driven NoSQL document structures. Some operational patterns are naturally document-oriented and map perfectly to MongoDB collection design, while highly repetitive, computational or low-latency reads are accelerated using Redis as an in-memory caching layer.

---

## Role & Assignment Parameters
In this solo version, you act as both the Solutions Architect and Data Engineer. You must extend your chosen business domain using MongoDB as the primary document database and Redis for fast execution caching.

### Core Architectural Requirements
* **Primary Database Layer:** Model and store collections in MongoDB, using MongoEngine as the object-document mapper (ODM) to bridge application logic with document structures.
* **In-Memory Caching Layer:** Deploy Redis to intercept and cache highly repetitive read workflows, maintaining tight cache consistency.
* **Command Line Routing:** Provide a structured CLI execution entry point via `main.py` accepting native task arguments (`--insert`, `--update`, `--q1`, `--q2`, `--q3`, `--q4`, `--q5`).

### Technical & Engineering Constraints
Your codebase must successfully execute the following NoSQL workflow specifications:
* **State Operations:** Programmatically append records by inserting at least one valid document into every assigned collection, followed by at least 1 transactional document update.
* **Advanced Aggregations:** Design and execute **5 non-trivial workloads**. Every query pipeline must consist of at least **3 discrete stages** and collectively use all 6 fundamental aggregation framework pipeline stages:
  * `$match`, `$project`, `$group`, `$unwind`, `$sort`, and `$lookup` (each used at least once).
* **Index Design Optimization:** Implement optimal query-supporting indexes. You must explicitly evaluate query access paths and mathematically or theoretically reason why an index helps or why it shouldn't be added (e.g., preventing high write-overhead on collection scans).
* **Cache Management:** Select **1 query** to run inside a Redis caching container. Design a distinct cache key taxonomy, set custom Time-To-Live (TTL) boundaries, and write cache invalidation callbacks that trigger immediately when underlying MongoDB source collection elements update.

---

## Required Deliverables

### 1. Document Schema & Workflow Catalog (`query_catalog.md`)
Detailed technical breakdown including:
* Definition of the 5 implemented application queries and their real-world business meaning.
* Architectural rationale explaining how chosen document structures natively support the system's operational workloads.

### 2. Physical Database Performance Tuning (`index_reasoning.md`)
Justification of the database's physical layout:
* Detailed trace of index usage across all active lookups.
* Formal explanations for edge cases where custom indexing was intentionally skipped to minimize index maintenance overhead.

### 3. Cache Design Blueprint (`caching_design.md`)
Comprehensive caching specification detailing:
* Cache key structural design patterns and selection criteria.
* Clear definitions of the caching strategy, default TTL settings, and invalidation workflows to eliminate stale cache reads.

### 4. Codebase Layout (`implementation/`)
```text
homework2_solo/
├── README.md               # Setup, initialization, and application execution instructions
├── query_catalog.md        # Documentation of business logic and document structures
├── index_reasoning.md      # Index strategies and database access optimization reasoning
├── caching_design.md       # Redis caching mechanics, key layouts, and TTL design
├── implementation/         # Executable Python environment
│   └── main.py             # Main entry point supporting parameters (--insert, --update, --q1...--q5)
└── LICENSE                 # Open-source licensing parameters
