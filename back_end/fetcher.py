from flask import Flask, Blueprint
from pymongo import MongoClient
import os
import json
from bson import json_util
from config import MAG_collection, DBLP_collection, Citeseer_papers_collection, Citeseer_authors_collection, Citeseer_citations_collection, theAdvisor_collection, theAdvisor_reverseindex
from util import exclude_fields, obj_from_bson


fetchers = Blueprint('fetcherssomething', __name__)



@fetchers.route("/api/v1/fetch/MAG/<int:magid>")
def get_mag_doc(magid):
    MAGobj = MAG_collection.find_one({"MAGid": magid})
    #print (MAGobj)
    if MAGobj is None:
        return ""
    return obj_from_bson(MAGobj)

@fetchers.route("/api/v1/fetch/MAG_by_DOI/<path:doi>")
def get_mag_bydoi_doc(doi):
    MAGobj = MAG_collection.find_one({"DOI": doi})
    #print (MAGobj)
    if MAGobj is None:
        return ""
    return obj_from_bson(MAGobj)


@fetchers.route("/api/v1/fetch/DBLP/<path:dblp_id>")
def get_dblp_doc(dblp_id):
    DBLPobj = DBLP_collection.find_one({"paper_id": dblp_id})
    #print (MAGobj)
    if DBLPobj is None:
        return ""
    return obj_from_bson(DBLPobj)

@fetchers.route("/api/v1/fetch/citeseer/<path:citeseer_id>")
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


@fetchers.route("/api/v1/fetch/citeseer_by_cluster/<int:cluster_id>")
def get_citeseer_by_clusterdoc(cluster_id):
    cluster_proj = {"cluster":1, "id":1}
    cluster = Citeseer_papers_collection.find({"cluster": cluster_id}, cluster_proj)
    if cluster is None:
        return ""
    return_array = []
    for cid in cluster:
        return_array.append (get_citeseer_doc(cid["id"]))
    return return_array
    

@fetchers.route("/api/v1/fetch/theAdvisor/<int:adv_id>")
def get_theadvisor_doc(adv_id):
    theAdv_obj = theAdvisor_collection.find_one({"theadvisor_id": adv_id})
    #print (theAdv_obj)
    if theAdv_obj is None:
        return ""
    return obj_from_bson(theAdv_obj)

def get_theadvisorobj_by_src(src):
    match = theAdvisor_reverseindex.find_one(src)
    if match is None:
        return ""
    theadv_id = match['theadvisor_id']
    return get_theadvisor_doc(theadv_id)

@fetchers.route("/api/v1/fetch/theAdvisor_byDOI/<path:doi>")
def get_theadvisor_by_doi(doi):
    magObj = MAG_collection.find_one({'DOI':doi}, {'MAGid':1})
    if magObj is None:
        return ""
    return get_theadvisorobj_by_src({'src':'MAG', 'id': magObj['MAGid']})

@fetchers.route("/api/v1/fetch/theAdvisor_byDBLP/<path:dblpid>")
def get_theadvisor_by_dblp(dblpid):
    return get_theadvisorobj_by_src({'src':'DBLP', 'id': dblpid})

@fetchers.route("/api/v1/fetch/theAdvisor_byMAG/<int:magid>")
def get_theadvisor_by_MAG(magid):
    return get_theadvisorobj_by_src({'src':'MAG', 'id': magid})

