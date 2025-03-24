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


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def exclude_fields(doc, fields):
    return {k: v for k, v in doc.items() if k not in fields}

def json_from_bson(document):
    return json.dumps(exclude_fields(document, {"_id"}), default=json_util.default)

@app.route("/api/v1/fetch/MAG/<int:magid>")
def get_mag_doc(magid):
    MAGobj = MAG_collection.find_one({"MAGid": magid})
    #print (MAGobj)
    if MAGobj is None:
        return ""
    return json_from_bson(MAGobj)

@app.route("/api/v1/fetch/MAG_by_DOI/<path:doi>")
def get_mag_bydoi_doc(doi):
    MAGobj = MAG_collection.find_one({"DOI": doi})
    #print (MAGobj)
    if MAGobj is None:
        return ""
    return json_from_bson(MAGobj)


@app.route("/api/v1/fetch/DBLP/<path:dblp_id>")
def get_dblp_doc(dblp_id):
    MAGobj = DBLP_collection.find_one({"paper_id": dblp_id})
    #print (MAGobj)
    if MAGobj is None:
        return ""
    return json_from_bson(MAGobj)
