import queries.special_case as special_case
import queries.parse_data as parse_data
import queries.mongo_query as mongo_query
from pymongo import MongoClient
from pathlib import Path
import os

def main():
    client = MongoClient('localhost')
    names=['queries/collect-event-queries',
            'queries/union-event-queries',
            'queries/calculate-metric-queries',
            'special_case',
            'queries/union-metric-queries']

    for name in names:
        if (name == 'special_case'):
            #CASO ESPECIAL DE BORRADO Y AVGINTRACARACTER
            special_case.execute()
            continue

        directory_path = os.path.join(Path().absolute(), name)
        mongo_query.execute_queries(client['metrics'],directory_path)

    directory_path = os.path.join(Path().absolute(), "level-prediction/raw_logs")
    parse_data.execute(directory_path,save_csv=True,save_json=True)
    pass

if __name__ == "__main__":
    main()