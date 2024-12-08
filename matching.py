import networkx as nx
from pymongo import MongoClient

#Setup MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['theAdvisor']

#DBLP to MAG
DBLPtoMAG = db['DBLPtoMAG'] 
Orginal_DBLP = db['Original_DBLP'] 
Orginal_MAG = db['Original_MAG'] 

#DBLP to Citeseer
DBLPtoCiteseer = db['DBLPtoCiteseer'] 



def make_graph():
    G = nx.DiGraph()

    original_dblp_papers = Orginal_DBLP.find({}, {'paper_id': 1, '_id': 0})
    
    for paper in original_dblp_papers:
        paper_id = paper['paper_id']
        
        #look through mag match for dblp id that was matched
        mag_match = DBLPtoMAG.find_one({'dblp_id': paper_id}, {'_id': 0})
        
        #look through citeseer match for dblp id that was matched
        citeseer_match = DBLPtoCiteseer.find_one({'candidate_dblp_id': paper_id}, {'_id': 0})
        
        G.add_node(paper_id, label='Original_DBLP')
        print(G)
        
        if mag_match:
            mag_id = mag_match.get('mag_id') 
            G.add_node(mag_id, label='DBLPtoMAG')
            G.add_edge(paper_id, mag_id)
        
        if citeseer_match:
            citeseer_id = citeseer_match.get('citeseer_id')  
            G.add_node(citeseer_id, label='DBLPtoCiteseer')
            G.add_edge(paper_id, citeseer_id)
    
    return G

graph = make_graph()





