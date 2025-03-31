from flask import Flask, Blueprint, request
from pymongo import MongoClient
import os
import json
from bson import json_util
from config import MAG_collection, DBLP_collection, Citeseer_papers_collection, Citeseer_authors_collection, Citeseer_citations_collection, theAdvisor_collection, theAdvisor_reverseindex
from util import exclude_fields, obj_from_bson
from numbers import Number
import math

fetchers = Blueprint('fetcherssomething', __name__)


#somehow there are nans that show up in DOIs
def normalize_advisor_objects(adv):
    try:
        if isinstance(adv['doi'], Number) and math.isnan(adv['doi']):
            adv['doi']=""
    except:
        pass #weird formats should not die in here
    return adv
    
#somehow there are nans that show up in DOIs
def normalize_MAG_objects(magp):
    try:
        if isinstance(magp['DOI'], Number) and math.isnan(magp['DOI']):
            magp['DOI']=""
    except:
        pass #weird formats should not die in here
    return magp

@fetchers.route("/api/v1/fetch/MAG/<int:magid>")
def get_mag_doc(magid):
    MAGobj = MAG_collection.find_one({"MAGid": magid})
    #print (MAGobj)
    if MAGobj is None:
        return {}
    return normalize_MAG_objects(obj_from_bson(MAGobj))

@fetchers.route("/api/v1/fetch/MAG_by_DOI/<path:doi>")
def get_mag_bydoi_doc(doi):
    MAGobj = MAG_collection.find_one({"DOI": doi})
    #print (MAGobj)
    if MAGobj is None:
        return {}
    return obj_from_bson(MAGobj)


@fetchers.route("/api/v1/fetch/DBLP/<path:dblp_id>")
def get_dblp_doc(dblp_id):
    DBLPobj = DBLP_collection.find_one({"paper_id": dblp_id})
    #print (MAGobj)
    if DBLPobj is None:
        return {}
    return obj_from_bson(DBLPobj)

@fetchers.route("/api/v1/fetch/citeseer/<path:citeseer_id>")
def get_citeseer_doc(citeseer_id):
    CSobj = Citeseer_papers_collection.find_one({"id": citeseer_id})
    #print (MAGobj)
    if CSobj is None:
        return {}
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
        return {}
    return_array = []
    for cid in cluster:
        return_array.append (get_citeseer_doc(cid["id"]))
    return return_array
    

@fetchers.route("/api/v1/fetch/theAdvisor/<int:adv_id>")
def get_theadvisor_doc(adv_id):
    theAdv_obj = theAdvisor_collection.find_one({"theadvisor_id": adv_id})
    print (theAdv_obj)
    if theAdv_obj is None:
        return {}
    return normalize_advisor_objects(obj_from_bson(theAdv_obj))

@fetchers.route("/api/v1/fetch/theAdvisor_array", methods=['POST'])
def get_theadvisor_array():
    query = request.get_json(force=True)
    print (query)
    query = query["query"]
    if (len(query) > 1000):
        return {} #proper error message for "that's too much"
    ret = []
    
    for advp in theAdvisor_collection.find({"theadvisor_id": {"$in":query}}):
        ret.append(normalize_advisor_objects(obj_from_bson(advp)))
    
    return ret


def get_theadvisorobj_by_src(src):
    match = theAdvisor_reverseindex.find_one(src)
    if match is None:
        return {}
    theadv_id = match['theadvisor_id']
    return get_theadvisor_doc(theadv_id)

@fetchers.route("/api/v1/fetch/theAdvisor_byDOI/<path:doi>")
def get_theadvisor_by_doi(doi):
    magObj = MAG_collection.find_one({'DOI':doi}, {'MAGid':1})
    if magObj is None:
        return {}
    return get_theadvisorobj_by_src({'src':'MAG', 'id': magObj['MAGid']})

@fetchers.route("/api/v1/fetch/theAdvisor_byDBLP/<path:dblpid>")
def get_theadvisor_by_dblp(dblpid):
    return get_theadvisorobj_by_src({'src':'DBLP', 'id': dblpid})

@fetchers.route("/api/v1/fetch/theAdvisor_byMAG/<int:magid>")
def get_theadvisor_by_MAG(magid):
    return get_theadvisorobj_by_src({'src':'MAG', 'id': magid})

@fetchers.route("/api/v1/fetch/theAdvisor_bysrc", methods=['POST'])
def get_theadvisor_by_explicitsrc():
    #This is done to santize input from user
    query = request.get_json(force=True)
    print(query)
    return get_theadvisorobj_by_src({'src':query['src'], 'id': query['id']})

@fetchers.route("/api/v1/fetch/theAdvisor_bysrc_array", methods=['POST'])
def get_theadvisor_by_explicitsrc_array():
    #This is done to santize input from user
    query = request.get_json(force=True)
    print(query)
    query = query["query"]
    ret = []

    advids = []
    for q in query:
        match = theAdvisor_reverseindex.find_one({'src':q['src'], 'id':q['id']})
        if match is not None:
            advids.append(match['theadvisor_id'])

    for advp in theAdvisor_collection.find({"theadvisor_id": {"$in":advids}}):
        ret.append(normalize_advisor_objects(obj_from_bson(advp)))

    return ret
