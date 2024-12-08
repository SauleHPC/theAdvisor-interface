from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.theAdvisor
collection = db.Original_MAG

# Define batch size
batch_size = 50000
count = 0
last_id = None

while True:
    # Build the query to fetch the next batch of documents
    query = {'_id': {'$gt': last_id}} if last_id else {}

    # Fetch the next batch of documents
    batch = list(collection.find(query).sort('_id', 1).limit(batch_size))

    # Break the loop if there are no more documents
    if not batch:
        print("No more documents to update.")
        break

    # Update the fields for each document in the batch
    for doc in batch:
        collection.update_one(
            {'_id': doc['_id']},  # Filter by document _id
            {
                '$rename': {
                    'col_0': 'id',
                    'col_1': 'doi_id',
                    'col_2': 'title',
                    'col_3': 'year',
                    'col_4': 'published'
                }
            }
        )

    # Log progress
    count += len(batch)
    print(f"Updated {count} documents so far.")

    # Get the _id of the last document in this batch for the next query
    last_id = batch[-1]['_id']

print("Field renaming complete for all documents!")
