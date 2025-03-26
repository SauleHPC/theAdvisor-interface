from config import MAG_collection, DBLP_collection, Citeseer_papers_collection, Citeseer_authors_collection, Citeseer_citations_collection, theAdvisor_collection, theAdvisor_reverseindex
import networkx as nx
from flask import Flask, Blueprint

citation_bp = Blueprint('citation_something', __name__)

graph = None
#from citer to citee
#so citers are predeccessors
#and citees are successors

def safe_add_edge(src, dest):
    global graph
    if src not in graph.nodes:
        graph.add_node(src)
    if dest not in graph.nodes:
        graph.add_node(dest)
    graph.add_edge(src, dest)

@citation_bp.route('/load')
def load_citation_graph():
    global graph
    graph = nx.DiGraph()
    for theadvisor_paper in theAdvisor_collection.find({}, {'theadvisor_id':1, 'citer':1, 'citee':1}):
        for pred in theadvisor_paper['citer']:
            safe_add_edge(pred, theadvisor_paper['theadvisor_id'])
    return f"{len(graph.nodes)} {len(graph.edges)}"


@citation_bp.route('/api/v1/citation/most_cited'):
def most_cited():
    global graph
    

