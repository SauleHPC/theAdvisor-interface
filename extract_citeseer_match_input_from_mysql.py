import pandas as pd
from sqlalchemy import create_engine
import os
import csv

# MySQL connection configuration
mysql_username = os.getenv('MYSQL_USER') or ''
mysql_password = os.getenv('MYSQL_PASSWORD') or ''
mysql_database = os.getenv('MYSQL_DATABASE') or 'theAdvisor'

# Create a SQLAlchemy engine for MySQL
mysql_engine = create_engine(f'mysql+pymysql://{mysql_username}:{mysql_password}@localhost/{mysql_database}')


table = 'papers'

# Batch size
batch_size = 2000

try:
    with open('citeseer_data.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        # Read the data in chunks from MySQL
        total = 0

        writer.writerow(["paperid", "cluster", "title"])
        
        while True:
            # Use the SQLAlchemy engine to read the data
            df = pd.read_sql(f'SELECT * FROM {table} LIMIT {batch_size} OFFSET {total}', con=mysql_engine)

            if df.empty:
                break

            # Convert DataFrame to dictionary format
            records = df.to_dict(orient='records')

            data = []
            
            for p in records:
                data.append([ p['id'], p['cluster'], p['title']])

            writer.writerows(data)
            
                
            total += batch_size

except Exception as e:
    print(f'Error processing table {table}: {e}')

