import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient
import os

mysql_username = 'root'
mysql_password = 'Hurricanes99'
mysql_database = 'theAdvisor'

#sql query
mysql_engine = create_engine(f'mysql+pymysql://{mysql_username}:{mysql_password}@localhost/{mysql_database}')

mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['theAdvisor']

table = 'citations'

#batch size for processing
batch_size = 20000

#where you want to start for processing
last_id = 0

try:
    while True:
        # Query with explicit index usage
        query = f"SELECT * FROM {table} USE INDEX (idx_citations_id) WHERE id > {last_id} ORDER BY id ASC LIMIT {batch_size}"
        df = pd.read_sql(query, con=mysql_engine)

        # Break the loop if no more data is found
        if df.empty:
            print(f'All records from table {table} have been successfully imported.')
            break

        # Convert DataFrame to dictionary format for MongoDB
        records = df.to_dict(orient='records')

        # Insert records into MongoDB
        mongo_db[table].insert_many(records)

        # Update last_id to the maximum 'id' of the current batch
        last_id = df['id'].max()

        # Print progress
        print(f'Successfully imported {len(records)} records from {table}. Last ID: {last_id}')

except Exception as e:
    print(f'Error processing table {table}: {e}')

# Close the MongoDB connection
mongo_client.close()
