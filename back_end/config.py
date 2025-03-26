from pymongo import MongoClient
import os
import json

client = MongoClient('mongodb://localhost:27017/')
mongo_database = os.getenv('MONGO_DATABASE') or "theAdvisor"
db = client[mongo_database]

MAG_collection=db["Original_MAG"]
DBLP_collection=db["Original_DBLP"]
Citeseer_papers_collection=db["papers_Citeseer"]
Citeseer_authors_collection=db["authors_Citeseer"]
Citeseer_citations_collection=db["citations_Citeseer"]

theAdvisor_collection=db["theAdvisor_papers"]
theAdvisor_reverseindex=db["theAdvisor_reverse"]
