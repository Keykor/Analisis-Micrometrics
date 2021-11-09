import json 
from pymongo import MongoClient
import ast
import os
from pathlib import Path
import special_case
import clean_data

def execute_queries(mongo_client, db_name, directory_name):
    db = mongo_client[db_name]

    directory = os.path.join(Path().absolute(), directory_name)

    for filename in os.listdir(directory):
        if not filename.endswith(".json"):
            continue

        with open(os.path.join(directory, filename), encoding="utf-8") as file:
            query = json.load(file)

            # Chequea que existan las colecciones necesarias
            needed_coll = query['dependsOf']
            needed_coll.append(query['forCollection'])
            all_coll = db.list_collection_names()
            if not (all(coll in all_coll for coll in needed_coll)):
                continue

            with open (os.path.join(directory, query['name']), 'r') as fp:
                pipeline = fp.read()

                # Transforma de string a lista con objetos
                pipeline = ast.literal_eval(pipeline)

                # Ejecuta la query en la coleccion
                col = db[query['forCollection']]
                col.aggregate(pipeline, allowDiskUse=True)

def main():
    client = MongoClient('localhost')
    execute_queries(client,'metrics','collect-event-queries')
    execute_queries(client,'metrics','union-event-queries')
    execute_queries(client,'metrics','calculate-metric-queries')
    #CASO ESPECIAL DE BORRADO Y AVGINTRACARACTER
    special_case.execute()
    execute_queries(client,'metrics','union-metric-queries')
    clean_data.execute()
    pass

if __name__ == "__main__":
    main()