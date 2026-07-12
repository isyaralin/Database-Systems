You must make sure you have docker in your current environment

1) **Navigate to the lab directory**:
   `cd ~/web-master-lab07-arangodb/lab07-arangodb`
   

2) ** Start the Database **: 
` docker compose up -d`

3) ** Initialize the Base Data **: 

` python3 -m app.seed `

4) ** Activate Virtual Environment **:
` source .venv/bin/activate `

** Running the solution **

- Navigate to the implementation folder to execute the main script
`cd homework3_solo/implementation`

1) ** Data Extension ** 
* Inserts 5 Brand vertices, 5 Edges connecting products to brands, and creates a persistent index on the brand name:
- `python3 main.py --insert`

2) ** Execute Graph Queries ** 
* Each query satisfies the Shared Query Requirements including multi-hop traversals and aggregations:

* Query1 (Aggregation): Product count per brand 
- ` python3 main.py --q1`

* Query2 (2-Hop Traversal): Finding customers who like "TechCorp" products 
-  `python3 main.py --q2 `

* Query3 (Regional Analysis): Popular brands in the EU-CZ Regional
- `python3 main.py --q3`


