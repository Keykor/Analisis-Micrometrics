import queries.special_case as special_case
import queries.parse_data as parse_data
import queries.mongo_query as mongo_query
from pymongo import MongoClient
from pathlib import Path
import os

def main(filterName, range_start, range_end, range_step):
    client = MongoClient('localhost')
    for i in range(range_start,range_end,range_step):
        print(filterName + " hasta " + str(i))
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
                mongo_query.execute_query(client['metrics'],directory_path, filterName, [0,i])
                continue
            
            mongo_query.execute_queries(client['metrics'],directory_path)
    
        directory_path = os.path.join(Path().absolute(), 'speed-prediction/speed-prediction-logs/' + filterName + '/' + str(i))
        parse_data.final_collection(directory_path,save_csv=True)
        parse_data.counts_collection(directory_path + "-counts",save_csv=True)

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

    directory_path = os.path.join(Path().absolute(), 'speed-prediction/speed-prediction-logs/' + filterName + '/all')
    parse_data.final_collection(directory_path,save_csv=True)
    pass

if __name__ == "__main__":
    print("TimeWindow Logs")
    main('TimeWindow',5000,300000,5000)
    #print("EventWindow Logs")
    #main('EventWindow',100,2100,100)
    #print("TimePercentage Logs")
    #main('TimePercentage',25,125,25)
    #print("EventPercentage Logs")
    #main('EventPercentage',25,125,25)