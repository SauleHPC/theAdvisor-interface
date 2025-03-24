from flask import Flask
from pymongo import MongoClient
import os
import json
from bson import json_util

client = MongoClient('mongodb://localhost:27017/')
mongo_database = os.getenv('MONGO_DATABASE') or "theAdvisor"
db = client[mongo_database]
MAG_collection=db["Original_MAG"]
DBLP_collection=db["Original_DBLP"]
Citeseer_papers_collection=db["papers_Citeseer"]
Citeseer_authors_collection=db["authors_Citeseer"]
Citeseer_citations_collection=db["citations_Citeseer"]

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def exclude_fields(doc, fields):
    return {k: v for k, v in doc.items() if k not in fields}

def obj_from_bson(document):
    return exclude_fields(document, {"_id"})

@app.route("/api/v1/fetch/MAG/<int:magid>")
def get_mag_doc(magid):
    MAGobj = MAG_collection.find_one({"MAGid": magid})
    #print (MAGobj)
    if MAGobj is None:
        return ""
    return obj_from_bson(MAGobj)

@app.route("/api/v1/fetch/MAG_by_DOI/<path:doi>")
def get_mag_bydoi_doc(doi):
    MAGobj = MAG_collection.find_one({"DOI": doi})
    #print (MAGobj)
    if MAGobj is None:
        return ""
    return obj_from_bson(MAGobj)


@app.route("/api/v1/fetch/DBLP/<path:dblp_id>")
def get_dblp_doc(dblp_id):
    DBLPobj = DBLP_collection.find_one({"paper_id": dblp_id})
    #print (MAGobj)
    if DBLPobj is None:
        return ""
    return obj_from_bson(DBLPobj)

@app.route("/api/v1/fetch/citeseer/<path:citeseer_id>")
def get_citeseer_doc(citeseer_id):
    CSobj = Citeseer_papers_collection.find_one({"id": citeseer_id})
    #print (MAGobj)
    if CSobj is None:
        return ""
    CSobj = obj_from_bson(CSobj)
    print ("got paper")

    CSobj["authors"] = []
    author_proj = {"name": 1, "email": 1}
    for a in Citeseer_authors_collection.find({"paperid": citeseer_id}, author_proj).sort("ord", 1):
        CSobj["authors"].append(obj_from_bson(a))
    print ("got authors")

    CSobj["citations"] = []
    citation_proj = {"cluster":1, "authors": 1, "title": 1, "venue": 1, "year":1}
    for c in Citeseer_citations_collection.find({"paperid": citeseer_id}, citation_proj):
        CSobj["citations"].append(obj_from_bson(c))
    print ("got citations")
    
    return CSobj


@app.route("/api/v1/fetch/citeseer_by_cluster/<int:cluster_id>")
def get_citeseer_by_clusterdoc(cluster_id):
    cluster_proj = {"cluster":1, "id":1}
    cluster = Citeseer_papers_collection.find({"cluster": cluster_id}, cluster_proj)
    if cluster is None:
        return ""
    return_array = []
    for cid in cluster:
        return_array.append (get_citeseer_doc(cid["id"]))
    return return_array
    
