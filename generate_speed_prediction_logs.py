import queries.special_case as special_case
import queries.parse_data as parse_data
import queries.mongo_query as mongo_query
from pymongo import MongoClient
from pathlib import Path
import os

def main():
    client = MongoClient('localhost')
    for i in range(100,2100,100):
        names=['queries/collect-event-queries',
                'queries/union-event-queries',
                'queries/filter-events-queries',
                'queries/calculate-metric-queries',
                'special_case',
                'queries/union-metric-queries',
                'queries/count-events-queries']

        for name in names:
            if (name == 'special_case'):
                #CASO ESPECIAL DE BORRADO Y AVGINTRACARACTER
                special_case.execute()
                continue

            directory_path = os.path.join(Path().absolute(), name)

            if (name == 'queries/filter-events-queries'):
                mongo_query.execute_query(client['metrics'],directory_path, 'EventWindow', [0,i])
                continue
            
            mongo_query.execute_queries(client['metrics'],directory_path)
    
        directory_path = os.path.join(Path().absolute(), 'speed-prediction/speed-prediction-logs/' + str(i))
        parse_data.final_collection(directory_path,save_csv=True)
        parse_data.counts_collection(directory_path + "-counts",save_csv=True)
    pass

if __name__ == "__main__":
    main()