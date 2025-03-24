import pandas as pd
from pymongo import MongoClient
import os
import sys

def batch_insert_csv_to_mongodb(csv_file_path:str, collection, batch_size:int =50000) -> None:

    # Read the CSV file in chunks (batch_size rows at a time)
    chunks = pd.read_csv(csv_file_path, chunksize=batch_size, header=0)

    
    # Process each chunk and insert into MongoDB
    for i, chunk in enumerate(chunks):
        data = chunk.to_dict(orient='records')        # Convert the pandas DataFrame to a list of dictionaries
        if len(data) > 0:
            collection.insert_many(data)
            print(f"Inserted batch {i+1} containing {len(data)} records")

    print("CSV upload to MongoDB completed.")

def usage():
    print ("Usage: python3 upload_matched_files.py <collection_name> <file1> [file2] [...]")
    print ("Note: You can set the Mongo Database by setting environment variable MONGO_DATABASE")
    sys.exit(-1)
    
if __name__ == "__main__":
    db_name = os.getenv('MONGO_DATABASE') or "theAdvisor"
    
    if len(sys.argv) < 3:
        usage()
    collection_name = sys.argv[1]

    flush_collection = False

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')  # Adjust if using a remote MongoDB server
    db = client[db_name]
    collection = db[collection_name]

    if flush_collection:
        print (f"Flushing data from {collection_name}")
        collection.delete_many({})
    
    print (f"Adding data to {collection_name}")
    
    
    for file_idx in range(2, len(sys.argv)):
        csv_file_path = sys.argv[file_idx]
        print (f"processing {csv_file_path}")
        batch_insert_csv_to_mongodb(csv_file_path, collection)
