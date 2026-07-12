# Graph Data Modeling and Connected Data over Graph Databases (Neo4j / ArangoDB)

## Business Context & Evolution
This project represents the third stage of platform maturity for the enterprise data infrastructure. Moving beyond large-scale raw data batch processing (MinIO + Spark) and document/key-value access optimization (MongoDB + Redis), the system now introduces support for **highly connected operational data**. 

In this phase, business-critical insights rely heavily on capturing the complex relationships between entities rather than querying flat, isolated transaction logs. By transitioning to a native **Graph Database Architecture**, the system can run multi-hop traversal queries to uncover patterns like deep recommendation networks, complex entity dependencies, cluster communities, or multi-tier logistics routings with extreme efficiency.

---

## Role & Assignment Parameters
In this solo version, you act as both the Graph Architect and Data Engineer. Your objective is to expand a graph data layout using a programmatic Object-Graph Mapper (OGM) or standard driver mapping, modeling connected access patterns using either **Neo4j** or **ArangoDB**.

### Core Architectural Requirements
* **Graph Engine Stack:** Implement the programmatic graph mapping layer using:
  * **`neomodel`** if executing over Neo4j (utilizing Cypher).
  * **`python-arango` + `pydantic`** if executing over the ArangoDB Graph Model (utilizing AQL).
* **Graph Topology Extension:** Artificially scale out the baseline graph topology by introducing:
  * At least **1 entirely new Vertex / Node type** (Label).
  * At least **1 entirely new Edge / Relationship type** (Type).
  * Programmatic insertion of a minimum of **5 new vertices** and **5 new edges** bridging new nodes to existing entity anchors.
* **Command Line Interfaces:** Structure code routing directly from `main.py` accepting native CLI switches (`--insert`, `--q1`, `--q2`, `--q3`).

### Shared & Technical Query Constraints
You must implement **3 non-trivial graph queries** designed around relational paths. Flat record lookups are strictly invalid. The queries must satisfy the following syntax boundaries:
* **Deep Traversals:** At least **two queries** must explicitly execute **two-hop or longer ($2+$ degrees of separation)** path lookups.
* **Path Processing:** At least **one query** must calculate computational results using graph-native aggregation metrics.
* **Language Constructs:** * **Cypher (Neo4j):** Must comprehensively apply `MATCH`, `OPTIONAL MATCH`, `RETURN`, `WITH`, `WHERE` (or inline matching filters), and `ORDER BY` across the script collection.
  * **AQL (ArangoDB):** Must comprehensively apply `FOR`, `FILTER`, `RETURN`, `LET`, `COLLECT ... AGGREGATE`, `SORT / LIMIT`, and variable-length traversals (e.g., `1..k OUTBOUND`) across the script collection.
* **Index Mechanics:** Evaluate execution traversals and mathematically or theoretically justify index placement optimizations, documenting cases where custom indexes were intentionally avoided.

---

## Required Deliverables

### 1. Entity-Relationship & Path Catalog (`query_catalog.md`)
Detailed technical breakdown containing:
* Comprehensive explanations of the 3 graph queries, their real-world business KPIs, and mathematical traversal pathways.
* Architectural justification detailing why graph topologies are fundamentally superior to relational schemas for these specific queries.

### 2. Graph Index Optimization Tuning (`index_reasoning.md`)
Justification of the graph engine's physical index parameters:
* Clear analysis showing property index configurations supporting traversal startup node lookups.
* Formal explanations for edge cases where manual indexing was skipped to reduce graph insertion overhead.

### 3. Application Implementation Layer (`implementation/`)
```text
homework3_solo/
├── README.md               # Environment spin-up steps, credentials, and framework execution guides
├── query_catalog.md        # Traversal descriptions, graph design justifications, and path layouts
├── index_reasoning.md      # Graph lookup profiling and index constraint justifications
├── implementation/         # Executable Python code layer
│   └── main.py             # Main routing application supporting CLI flags (--insert, --q1, --q2, --q3)
└── LICENSE                 # Open-source licensing parameters
