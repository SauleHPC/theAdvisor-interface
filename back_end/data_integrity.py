from config import MAG_collection, DBLP_collection, Citeseer_papers_collection, Citeseer_authors_collection, Citeseer_citations_collection, theAdvisor_collection, theAdvisor_reverseindex
import networkx as nx
from flask import Flask, Blueprint

integrity_bp = Blueprint('integrity_something', __name__)


@integrity_bp.route('/api/v1/integrity/multipleMAG')
def multiple_mag():
    magreport = []
    for paper in theAdvisor_collection.find({}):
        magcount = 0
        for source in paper['sources']:
            if source['src'] == 'MAG':
                magcount+=1
        if magcount > 1:
            magreport.append(paper['theadvisor_id'])
    return magreport
