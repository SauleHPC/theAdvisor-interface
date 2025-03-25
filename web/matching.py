import networkx as nx
from pymongo import MongoClient
import os

'''
File is used as a simple matching script to cross refrence paper in MongoDB.
'''

#Setup MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db_name = os.getenv('MONGO_DATABASE') or 'theAdvisor'
db = client[db_name]

#DBLP to MAG
DBLPtoMAG = db['DBLPtoMAG']
DBLPtoCiteseer = db['DBLPtoCiteseer'] 
Original_DBLP = db['Original_DBLP'] 
Original_MAG = db['Original_MAG'] 
MAG_Ref = db['Original_MAG_References']

#DBLP to Citeseer
DBLPtoCiteseer = db['DBLPtoCiteseer'] 


def dblp_node_name(paper_id):
    return f"DBLP:{paper_id}"

def dblp_node_data(paper_id):
    return {'src':'DBLP', 'id':paper_id}

def mag_node_name(paper_id):
    return f"MAG:{paper_id}"

def mag_node_data(paper_id):
    return {'src':'MAG', 'id':paper_id}

def citeseer_node_name(paper_id):
    return f"Citeseer:{paper_id}"

def citeseer_node_data(paper_id):
    return {'src':'Citeseer', 'id':paper_id}

def make_matching_graph():
    G = nx.Graph()

    print ("parsing DBLP data")
    #first add all DBLP papers
    original_dblp_papers = Original_DBLP.find({}, {'paper_id': 1, '_id': 0})

    for paper in original_dblp_papers:
        paper_id = paper['paper_id']

        G.add_node(dblp_node_name(paper_id), data = dblp_node_data(paper_id))

    print ("parsing DBLP to MAG data")
    # go through all DBLP to MAG match
    for ma in DBLPtoMAG.find({}, {'candidate_mag_id':1, 'candidate_dblp_id':1, '_id':0}):
        dblp_id = ma['candidate_dblp_id']
        mag_id = ma['candidate_mag_id']

        if mag_node_name(mag_id) not in G.nodes:
            G.add_node(mag_node_name(mag_id), data = mag_node_data(mag_id))
        G.add_edge(dblp_node_name(dblp_id), mag_node_name(mag_id))

    print ("parsing DBLP to Citeseer data")
    # go through all DBLP to Citeseer match
    for ma in DBLPtoCiteseer.find({}, {'candidate_dest_id':1, 'candidate_source_id':1, '_id': 0}):
        dblp_id = ma['candidate_source_id']
        citeseer_id = ma['candidate_dest_id'] #this is of the format ('10.1.1.1.1484', '9074107')"
        citeseer_id = tuple(citeseer_id.strip("()").replace("'", "").split(", "))[0] #now in the format '10.1.1.1.1484'
        
        if citeseer_node_name(citeseer_id) not in G.nodes:
            G.add_node(citeseer_node_name(citeseer_id), data = citeseer_node_data(citeseer_id))
        G.add_edge(dblp_node_name(dblp_id), citeseer_node_name(citeseer_id))

    
    return G

graph = make_matching_graph()

mag_seen=set()

for v in graph.nodes:
    try :
        if graph.nodes[v]['data']['src'] == 'MAG':
            mag_id = graph.nodes[v]['data']['id']
            mag_seen = mag_seen & set([mag_id])
    except Exception as e:
        print(e)
        print (v)

#add all mag papers within 1 of the one we matched to get a real graph
for mag_edge in MAG_Ref.find({},{"citer":1, "citee":1, "_id":0}):
    src_magid = mag_edge['citer']
    dest_magid = mag_edge['citee']
    if dest_magid in mag_seen:
        if src_magid not in mag_seen:
            mag_seen = mag_seen & set([src_magid])
            graph.add_node(mag_node_name(src_magid), data = mag_node_data(src_magid))

    if src_magid in mag_seen:
        if dest_magid not in mag_seen:
            mag_seen = mag_seen & set([dest_magid])
            graph.add_node(mag_node_name(dest_magid), data = mag_node_data(dest_magid))
        

conn = nx.connected_components(graph)

for co in conn:
    print (co)
