import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient
import os

# MySQL connection configuration
mysql_username = os.getenv('MYSQL_USER') or ''
mysql_password = os.getenv('MYSQL_PASSWORD') or ''
mysql_database = os.getenv('MYSQL_DATABASE') or 'theAdvisor'

# Create a SQLAlchemy engine for MySQL
mysql_engine = create_engine(f'mysql+pymysql://{mysql_username}:{mysql_password}@localhost/{mysql_database}')

# MongoDB connection configuration
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_database = os.getenv('MONGO_DATABASE') or 'theAdvisor'
mongo_db = mongo_client[mongo_database]

# List of tables to export and import
#tables = ['citations']
#tables = ['authors']
tables = ['papers', 'paperVersions', 'citations']
mongo_collection_suffix = '_Citeseer'
delete_collection_first = False

# Batch size
batch_size = 20000

# Export from MySQL and import to MongoDB in batches
for table in tables:
    try:
        # Read the data in chunks from MySQL
        total = 0

        mongo_collection = table + mongo_collection_suffix
        
        if delete_collection_first:
            result = mongo_db[mongo_collection].delete_many({})
            print(f"Deleted {result.deleted_count} documents from {mongo_collection}.")

        while True:
            # Use the SQLAlchemy engine to read the data
            df = pd.read_sql(f'SELECT * FROM {table} LIMIT {batch_size} OFFSET {total}', con=mysql_engine)

            if df.empty:
                break

            # Convert DataFrame to dictionary format
            records = df.to_dict(orient='records')

            # Insert records into MongoDB
            mongo_db[mongo_collection].insert_many(records)
            print(f'Successfully imported {len(records)} records from {table} into {mongo_collection}. Total: {total}')

            total += batch_size

    except Exception as e:
        print(f'Error processing table {table}: {e}')

# Close the MongoDB connection
mongo_client.close()
