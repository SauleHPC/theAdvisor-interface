import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient

# MySQL connection configuration
mysql_username = ''
mysql_password = ''
mysql_database = 'theAdvisor'

# Create a SQLAlchemy engine for MySQL
mysql_engine = create_engine(f'mysql+pymysql://{mysql_username}:{mysql_password}@localhost/{mysql_database}')

# MongoDB connection configuration
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['theAdvisor']

# List of tables to export and import
tables = ['citations']

# Batch size
batch_size = 20000

# Export from MySQL and import to MongoDB in batches
for table in tables:
    try:
        # Read the data in chunks from MySQL
        total = 50900000
        
        while True:
            # Use the SQLAlchemy engine to read the data
            df = pd.read_sql(f'SELECT * FROM {table} LIMIT {batch_size} OFFSET {total}', con=mysql_engine)

            if df.empty:
                break

            # Convert DataFrame to dictionary format
            records = df.to_dict(orient='records')

            # Insert records into MongoDB
            mongo_db[table].insert_many(records)
            print(f'Successfully imported {len(records)} records from {table} total: {total}')

            total += batch_size

    except Exception as e:
        print(f'Error processing table {table}: {e}')

# Close the MongoDB connection
mongo_client.close()
