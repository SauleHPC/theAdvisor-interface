from parse import parse_DBLP_file, parse_MAG_file, parse_citeseer
from callback import populate_dblp_mongo
from pymongo import MongoClient
import pandas as pd
import gzip
import os

#DBLP
#-----------------------------
# Connect to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')
# Select the database
mongo_database = os.getenv('MONGO_DATABASE') or "theAdvisor"
db = client[mongo_database]

# Select the collection
# Collection name
collection_name = "Original_DBLP"
papers_collection = db[collection_name]
delete_collection_first = False

if delete_collection_first:
    result = papers_collection.delete_many({})
    print(f"Deleted {result.deleted_count} documents from {mongo_collection}.")


for i in range(0, 6800000, 50000):
    paper_docs = []

    callbacks = [lambda currentPaper: populate_dblp_mongo(currentPaper, paper_docs)]

    print("parsing DBLP")
    paper_docs = parse_DBLP_file(callbacks, i, i+50000)

    if paper_docs is not None:    
        papers_collection.insert_many(paper_docs)

