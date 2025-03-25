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
Orginal_DBLP = db['Original_DBLP'] 
Orginal_MAG = db['Original_MAG'] 

#DBLP to Citeseer
DBLPtoCiteseer = db['DBLPtoCiteseer'] 


def dblp_node_name(paper_id):
    return f"DBLP:{paper_id}"

def mag_node_name(paper_id):
    return f"MAG:{paper_id}"

def citeseer_node_name(paper_id):
    return f"MAG:{paper_id}"


def make_matching_graph():
    G = nx.DiGraph()

    print ("parsing DBLP data")
    #first add all DBLP papers
    original_dblp_papers = Orginal_DBLP.find({}, {'paper_id': 1, '_id': 0})

    for paper in original_dblp_papers:
        paper_id = paper['paper_id']

        G.add_node(paper_id, label='Original_DBLP')

        G.add_node(dblp_node_name(paper_id), data = {'src':'DBLP', 'id':paper_id})

    print ("parsing DBLP to MAG data")
    # go through all DBLP to MAG match
    for ma in DBLPtoMAG.find({}, {'candidate_mag_id':1, 'candidate_dblp_id':1, '_id':0}):
        dblp_id = ma['candidate_dblp_id']
        mag_id = ma['candidate_mag_id']

        if mag_node_name(mag_id) not in G.nodes:
            G.add_node(mag_node_name(mag_id), data = {'src':'MAG', 'id':mag_id})
        G.add_edge(dblp_node_name(dblp_id), mag_node_name(mag_id))

    print ("parsing DBLP to MAG data")
    # go through all DBLP to Citeseer match
    for ma in DBLPtoCiteseer.find({}, {'candidate_dest_id':1, 'candidate_source_id':1, '_id': 0}):
        dblp_id = ma['candidate_source_id']
        citeseer_id = ma['candidate_dest_id'] #this is of the format ('10.1.1.1.1484', '9074107')"
        citeseer_id = tuple(citeseer_id.strip("()").replace("'", "").split(", "))[0] #now in the format '10.1.1.1.1484'
        
        if citeseer_id not in G.nodes:
            G.add_node(mag_node_name(mag_id), data = {'src':'Citeseer', 'id':citesser_id})
        G.add_edge(dblp_node_name(dblp_id), citeseer_node_name(citeseer_id))

    
    return G

graph = make_matching_graph()

# Get nodes and edges
nodes = list(graph.nodes(data=True))
edges = list(graph.edges(data=True))

print("Nodes:", nodes)
print("Edges:", edges)

