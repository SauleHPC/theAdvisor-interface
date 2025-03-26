import networkx as nx
from pymongo import MongoClient
import os
import sys
from datetime import datetime

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
papers_Citeseer = db['papers_Citeseer'] 
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

    if True: #delete me
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
        if dblp_node_name(dblp_id) not in G.nodes: #shouldn't happen unless files are out of sync
            G.add_node(dblp_node_name(dblp_id), data = dblp_node_data(dblp_id))
        G.add_edge(dblp_node_name(dblp_id), mag_node_name(mag_id))
        if len(G.nodes) > 100000000: #delete me
            break

    print ("parsing DBLP to Citeseer data")
    # go through all DBLP to Citeseer match
    for ma in DBLPtoCiteseer.find({}, {'candidate_dest_id':1, 'candidate_source_id':1, '_id': 0}):
        dblp_id = ma['candidate_source_id']
        citeseer_id = ma['candidate_dest_id'] #this is of the format ('10.1.1.1.1484', '9074107')"
        citeseer_id = tuple(citeseer_id.strip("()").replace("'", "").split(", "))[0] #now in the format '10.1.1.1.1484'
        
        if citeseer_node_name(citeseer_id) not in G.nodes:
            G.add_node(citeseer_node_name(citeseer_id), data = citeseer_node_data(citeseer_id))
        if dblp_node_name(dblp_id) not in G.nodes:
            G.add_node(dblp_node_name(dblp_id), data = dblp_node_data(dblp_id))
        G.add_edge(dblp_node_name(dblp_id), citeseer_node_name(citeseer_id))
        if len(G.nodes) > 200000000: #delete me
            break

        
    
    return G


def add_mag_dist_1(graph):
    mag_seen=set()

    print(datetime.now())
    print ("Logging seen MAG papers")
    for v in graph.nodes:
        try :
            if graph.nodes[v]['data']['src'] == 'MAG':
                mag_id = graph.nodes[v]['data']['id']
                mag_seen = mag_seen.union( set([mag_id]) )
        except Exception as e:
            print ("Exception: "+str(e))
            print (f"vertex at exception time {v}")

    print (f"{len(mag_seen)} mag papers in")
        
    mag_dist_0 = mag_seen.copy()

    print(datetime.now())
    print ("Adding dist 1 papers from MAG")
    #add all mag papers within 1 of the one we matched to get a real graph
    magrefcount = 0
    newmagpapers = 0
    for mag_edge in MAG_Ref.find({},{"citer":1, "citee":1, "_id":0}):
        if magrefcount % 1000000 == 0:
            print (f"{magrefcount} MAG edges")
            print (f"{newmagpapers} new papers ")
            print (f"magseen: {len(mag_seen)}")
            print (f"magdist0: {len(mag_dist_0)}")

            if newmagpapers > 100: #delete me
                break
        magrefcount = magrefcount+1
        src_magid = mag_edge['citer']
        dest_magid = mag_edge['citee']
       
        if dest_magid in mag_dist_0:
            if src_magid not in mag_seen:
                mag_seen = mag_seen.union( set([src_magid]) )
                graph.add_node(mag_node_name(src_magid), data = mag_node_data(src_magid))
                newmagpapers += 1
            
        if src_magid in mag_dist_0:
            if dest_magid not in mag_seen:
                mag_seen = mag_seen.union ( set([dest_magid]) )
                graph.add_node(mag_node_name(dest_magid), data = mag_node_data(dest_magid))
                newmagpapers += 1


    print (f"dist 1 mag papers: {newmagpapers}")
    return graph

    
print(datetime.now())

graph = make_matching_graph()

print (f"vertices: {len(graph.nodes)}")

graph = add_mag_dist_1(graph)
print(datetime.now())

conn = nx.connected_components(graph)


def make_the_advisor_paper(connected_component):
    ret = {}
    ret['sources'] = connected_component.copy()
    found_dblp = None
    found_mag = None
    found_citeseer = None
    for p in connected_component:
        if graph.nodes[p]['data']['src'] == 'MAG':
            found_mag = graph.nodes[p]['data']['id']
        if graph.nodes[p]['data']['src'] == 'DBLP':
            found_dblp = graph.nodes[p]['data']['id']
        if graph.nodes[p]['data']['src'] == 'Citeseer':
            found_citeseer = graph.nodes[p]['data']['id']

    if found_dblp:
        dblppaper = db.Original_DBLP.find_one({'paper_id': found_dblp})
        ret ['title'] = dblppaper['title']
    elif found_mag:
        magpaper = db.Original_MAG.find_one({'MAGid': found_mag})
        ret ['title'] = magpaper['title']
    elif found_citeseer:
        citeseerpaper = db.papers_Citeseer.find_one({'id': found_citeseer})
        ret ['title'] = magpaper['title'] or ""
    return ret


print ("flushing")
print(datetime.now())
    
theadvisor_collection = db['theAdvisor_papers']

theadvisor_collection.delete_many({}) #always flush

print ("flushed")
print(datetime.now())


theadvisorid = 0

for co in conn:
    print (co)
    pap = make_the_advisor_paper(co)
    pap['theadvisor_id'] = theadvisorid
    theadvisorid +=1
    print (pap)


    
