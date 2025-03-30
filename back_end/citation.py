from config import MAG_collection, DBLP_collection, Citeseer_papers_collection, Citeseer_authors_collection, Citeseer_citations_collection, theAdvisor_collection, theAdvisor_reverseindex
import networkx as nx
from flask import Flask, Blueprint, request
import fetcher as fetcher

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
    graph.add_edge(dest, src) #delete me

@citation_bp.route('/load')
def load_citation_graph(limit = 99999999, back_edges = True):
    global graph
    graph = nx.DiGraph()
    for theadvisor_paper in theAdvisor_collection.find({}, {'theadvisor_id':1, 'citer':1, 'citee':1}):
        for pred in theadvisor_paper['citer']:
            safe_add_edge(pred, theadvisor_paper['theadvisor_id'])
        if back_edges:
            for succ in theadvisor_paper['citee']: #We want the back edges
                safe_add_edge(succ, theadvisor_paper['theadvisor_id'])
            
        if len(graph.nodes) > limit:
            break
    return f"{len(graph.nodes)} {len(graph.edges)}"

@citation_bp.route('/quickload')
def QL():
    load_citation_graph(10000)
    return ""


@citation_bp.route('/api/v1/citation/most_cited')
def most_cited():
    global graph
    deg = graph.in_degree()
    verts = [v for v in graph.nodes]
    verts = sorted(verts, key=lambda x: deg[x])
    return f"{verts[0]} {deg[verts[0]]}  {verts[-1]} {deg[verts[-1]]}"


@citation_bp.route('/api/v1/citation/most_citing')
def most_citing():
    global graph
    deg = graph.out_degree()
    verts = [v for v in graph.nodes]
    verts = sorted(verts, key=lambda x: deg[x])
    return f"{verts[0]} {deg[verts[0]]}  {verts[-1]} {deg[verts[-1]]}"

@citation_bp.route('/api/v1/citation/page_rank')
def page_rank():
    global graph
    ranks = nx.pagerank(graph)
    verts = [v for v in graph.nodes]
    verts = sorted(verts, key=lambda x: ranks[x])
    ret = []
    for i in range(0, 100):
        ret.append((verts[-i-1], ranks[verts[-i-1]]))
    return ret

@citation_bp.route('/api/v1/citation/recommend', methods=['POST'])
def recommend():
    global graph
    queries = []
    query = request.get_json(force=True)["query"]
    for s in query:
        match = theAdvisor_reverseindex.find_one(s)
        if match is None:
            continue
        theadv_id = match['theadvisor_id']
        queries.append(theadv_id)
    print (f"something {queries}")

    pers = { }
    for q in queries:
        pers[q]= 1.0/len(query)
    
    ranks = nx.pagerank(graph, personalization = pers, dangling=pers)
    verts = [v for v in graph.nodes]
    verts = sorted(verts, key=lambda x: ranks[x])
    ret = []
    for i in range(0, 100):
        ret.append((verts[-i-1], ranks[verts[-i-1]]))
    return ret

