import json
from bson import json_util


def exclude_fields(doc, fields):
    return {k: v for k, v in doc.items() if k not in fields}

def obj_from_bson(document):
    return exclude_fields(document, {"_id"})
