from parse import parse_DBLP_file, parse_MAG_file, parse_citeseer
from callback import populate_dblp_mongo
from pymongo import MongoClient
import pandas as pd
import gzip
import os

#MAG
#-----------------------------------
selected_columns = [0, 2, 4, 7]
column_names= ["MAGid", "DOI", "title", "year"]
gz_file_path = "../../../mnt/large_data/MAG-2021-12/Papers.txt.gz"

client = MongoClient('mongodb://localhost:27017/')
batch_size = 50000 

mongo_database = os.getenv('MONGO_DATABASE') or "theAdvisor"
db = client[mongo_database]
collection_name = "Original_MAG"
papers_collection = db[collection_name]


flush_collection = True
if flush_collection:
    print ("Deleting {collection_name}")
    result = papers_collection.delete_many({})
    print(f"Deleted {result.deleted_count} documents from {collection_name}.")

print ("parsing")
    
with gzip.open(gz_file_path, 'rt', encoding='utf-8') as f:
    batch_counter = 0
    
    for chunk in pd.read_csv(f, sep='\t', header=None, usecols=selected_columns, chunksize=batch_size):
        chunk.columns = [column_names[i] for i in range(len(selected_columns))]
        
        data = chunk.to_dict(orient='records')
        
        papers_collection.insert_many(data)
        
        batch_counter += len(data)

        print (batch_counter)
