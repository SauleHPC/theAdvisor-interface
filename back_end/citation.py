from config import MAG_collection, DBLP_collection, Citeseer_papers_collection, Citeseer_authors_collection, Citeseer_citations_collection, theAdvisor_collection, theAdvisor_reverseindex
import networkx as nx
from flask import Flask, Blueprint, request
import fetcher as fetcher
import psutil


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
def load_citation_graph(limit = 999999, back_edges = False):
    global graph
    process = psutil.Process()
    mem_before = process.memory_info().rss

    graph = nx.DiGraph()
    for theadvisor_paper in theAdvisor_collection.find({}, {'theadvisor_id':1, 'citer':1, 'citee':1}):
        if back_edges:
            for pred in theadvisor_paper['citer']:
                safe_add_edge(theadvisor_paper['theadvisor_id'], pred)
        for succ in theadvisor_paper['citee']: #We want the back edges
            safe_add_edge(theadvisor_paper['theadvisor_id'], succ)
            
        if len(graph.nodes) > limit:
            break

    mem_after = process.memory_info().rss
    mem_for_graph=mem_after - mem_before
    print (f"vertices={len(graph.nodes)} edges={len(graph.edges)} memory={mem_for_graph/1024/1024}MB memperedge={mem_for_graph/len(graph.edges)}")
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

    # we don't want to return the vertices used in seeding the
    # search. so filtering them out
    for q in queries:
        ranks[q]= 0.
    
    verts = sorted(verts, key=lambda x: ranks[x])
    ret = []
    for i in range(0, 100):
        ret.append((verts[-i-1], ranks[verts[-i-1]]))
    return ret

