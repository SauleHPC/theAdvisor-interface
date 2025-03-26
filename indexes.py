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

DBLPtoMAG = db['DBLPtoMAG']

DBLPtoCiteseer = db['DBLPtoCiteseer'] 

Original_DBLP = db['Original_DBLP'] 
Original_DBLP.create_index("paper_id", background=True)

Original_MAG = db['Original_MAG']
Original_MAG.create_index("DOI", background=True)
Original_MAG.create_index("MAGid", background=True)

papers_Citeseer = db['papers_Citeseer'] 
papers_Citeseer.create_index("cluster", background=True)
papers_Citeseer.create_index("id", background=True)

MAG_Ref = db['Original_MAG_References']
MAG_Ref.create_index("citer", background=True)
MAG_Ref.create_index("citee", background=True)

DBLPtoCiteseer = db['DBLPtoCiteseer'] 

#
theadvisor_collection = db['theAdvisor_papers']
