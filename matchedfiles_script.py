import pandas as pd
from pymongo import MongoClient

def batch_insert_csv_to_mongodb(csv_file_path, db_name, collection_name, batch_size=50000):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')  # Adjust if using a remote MongoDB server
    db = client[db_name]
    collection = db[collection_name]

    # Read the CSV file in chunks (batch_size rows at a time)
    chunks = pd.read_csv(csv_file_path, chunksize=batch_size)

    # Process each chunk and insert into MongoDB
    for i, chunk in enumerate(chunks):
        # Convert the pandas DataFrame to a list of dictionaries
        data = chunk.to_dict(orient='records')

        # Insert the data into the MongoDB collection
        collection.insert_many(data)

        print(f"Inserted batch {i+1} containing {len(data)} records")

    print("CSV upload to MongoDB completed.")

if __name__ == "__main__":
    csv_file_path = "dblp_to_mag_matched.csv"
    db_name = "theAdvisor"
    collection_name = "DBLPtoMAG"

    batch_insert_csv_to_mongodb(csv_file_path, db_name, collection_name)
