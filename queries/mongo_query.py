from pymongo import MongoClient
import json
import ast
import os

def make_query(node_name, query_graph, started_queries, maked_queries, db):
    if (node_name in maked_queries):
        return False

    if (node_name in started_queries):
        return True
    started_queries.append(node_name)

    # chequeo de si es una collection de otra pipeline
    if (node_name not in query_graph):
        if (node_name not in db.list_collection_names()):
            return True
        maked_queries.append(node_name)
        return False

    needed_coll = query_graph[node_name]['dependsOf']
    needed_coll.append(query_graph[node_name]['forCollection'])

    for query_name in needed_coll:
        circular_reference = make_query(query_name, query_graph, started_queries, maked_queries, db)
        if (circular_reference):
            return True
    
    # hace la query en mongodb
    col = db[query_graph[node_name]['forCollection']]
    col.aggregate(query_graph[node_name]['pipeline'], allowDiskUse=True)

    maked_queries.append(node_name)
    return False

def execute_queries(db, directory):

    query_graph = {}

    for filename in os.listdir(directory):
        if not filename.endswith(".json"):
            continue

        with open(os.path.join(directory, filename), encoding="utf-8") as file:
            query = json.load(file)

            with open (os.path.join(directory, query['name']), 'r') as fp:
                pipeline = fp.read()

                # Transforma de string a lista con objetos
                pipeline = ast.literal_eval(pipeline)

                query['pipeline'] = pipeline

            query_graph[query['name']] = query
    
    started_queries = []
    maked_queries = []
    for node_name in query_graph:
        circular_reference = make_query(node_name, query_graph, started_queries, maked_queries, db)
        if (circular_reference):
            print("Se corto ejecución por problema")
            break

def execute_query(db, directory, query_name, params=None):
    all_coll = db.list_collection_names()
    with open(os.path.join(directory, query_name + ".json"), encoding="utf-8") as file:
        query = json.load(file)

        needed_coll = query['dependsOf']
        needed_coll.append(query['forCollection'])
        for coll in needed_coll:
            if coll not in all_coll:
                print("Se corto ejecución por problema")
                return

        with open (os.path.join(directory, query['name']), 'r') as fp:
            pipeline = fp.read()

            if (not params):
                params = query['params']

            for idx,param in enumerate(params):
                val = "params[" + str(idx) + "]"
                pipeline = pipeline.replace(val, str(param))

            pipeline = ast.literal_eval(pipeline)
            col = db[query['forCollection']]
            col.aggregate(pipeline, allowDiskUse=True)
