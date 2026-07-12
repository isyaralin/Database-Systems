**Required Materials**

Docker and Docker Compose
Python3
Dependencies: mongoengine, redis, pymongo

**Environment Setup**


Start Database
docker compose up -d 


Seed Database


 python3 -m seed_mongo

Initialize Lab Data

python3 main.py --insert

**Running Queries**


Query 1 (Revenue Trend):
python3 implementation/main.py --q1 "EU-CZ" 


Query 2 (Top Categories):
 python3 implementation/main.py --q2 "EU-CZ"


Query 3 (Category Price Analysis):
python3 implementation/main.py --q3 "Office"


Query 4 (Top 5 Spenders):
python3 implementation/main.py --q4


Query 5 (Status Audit):
python3 implementation/main.py --q5 "AUDITED_SOLO"
