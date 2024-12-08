from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db = client.theAdvisor
papers_collection = db.papers_Citeseer
papers_collection_match_field = 'cluster'
citeseer_collection = db.citations
citeseer_collection_match_field = 'cluster'

#Set a batch to perform the merges for memory management
batch_size = 10000
batch = []
#NOTE: this is the new collection that will be made where the merge will happen
merged_collection = db.mergePapersCitations_Citeseer
total_batches_completed = 0

#boolean value if you only want to fetch specific fields from the collection you are searching (not looping)
fetch_specific_fields = True  

#iterate through all papers in Citeseer
for paper in papers_collection.find():

    paper_cluster = paper.get(papers_collection_match_field)

    if not paper_cluster:
        continue

    if fetch_specific_fields:
        #these are the only fields taht will be kept if fetch_specific_fields is true
        matched_citations = list(citeseer_collection.find(
            {citeseer_collection_match_field: paper_cluster},
            {"cluster": 1, "paperid": 1, "_id": 0} 
        ))
    else:
        matched_citations = list(citeseer_collection.find({citeseer_collection_match_field: paper_cluster}))

    paper['citations'] = matched_citations

    batch.append(paper)

    if len(batch) >= batch_size:
        merged_collection.insert_many(batch)
        total_batches_completed += batch_size
        print(total_batches_completed)
        batch = []

#this is for leftover papers if we kick out of the loop before the batch size is fully iterated over
if batch:
    merged_collection.insert_many(batch)

print("Merging completed and results inserted into 'mergePapersCitations_Citeseer' collection.")

client.close()
