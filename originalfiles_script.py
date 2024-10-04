from parse import parse_DBLP_file, parse_MAG_file, parse_citeseer
from callback import populate_dblp_mongo
from pymongo import MongoClient
import pandas as pd
import gzip


#DBLP
#-----------------------------
# Connect to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')
# Select the database
db = client["theAdvisor"]

# Select the collection
# Collection name
collection_name = "Original_DBLP"
papers_collection = db[collection_name]

callbacks = [lambda currentPaper: populate_dblp_mongo(currentPaper, collection_name, papers_collection)]

print("parsing DBLP")
paper_docs = parse_DBLP_file(callbacks, 0, 9000000)



papers_collection.insert_many(paper_docs)


#MAG
#-----------------------------------
selected_columns = [0, 2, 4, 7, 9]
gz_file_path = "../../../mnt/large_data/MAG-2021-12/Papers.txt.gz"

with gzip.open(gz_file_path, 'rt', encoding='utf-8') as f:
    df = pd.read_csv(f, sep='\t', header=None, usecols=selected_columns)

df.columns = [f"col_{i}" for i in range(len(selected_columns))]

client = MongoClient('mongodb://localhost:27017/')  
db = client['theAdvisor']
collection_name = "Original_MAG"
papers_collection = db[collection_name]

data = df.to_dict(orient='records')  

papers_collection.insert_many(data)  

print(f"Inserted {len(data)} records into MongoDB")
