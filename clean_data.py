from pymongo import MongoClient
import json 

def execute():
    client = MongoClient('localhost')
    db = client['metrics']
    col = db['Final']

    data = list(col.find({}))
    dataset = []
    for elem in data:
        obj = {}
        for elto in elem['data']:
            for key, value in elto.items():
                obj[key] = value
        dataset.append(obj)
    
    logs = []
    for elem in dataset:
        if ('avgSpeedPerTest' in elem) and (elem['avgSpeedPerTest']) and ('level' in elem) and (elem['level']):
            
            if ('totalPauses' not in elem):
                elem['totalPauses'] = 0
                elem['avgPauseDuration'] = 0

            if ('avgIntratecla' not in elem):
                elem['avgIntratecla'] = 0

            if ('totalBorrado' not in elem):
                elem['totalBorrado'] = 0

            logs.append(elem)
    
    logs.sort(key=lambda x: x['level'])

    with open("logs.json","w",encoding="utf-8") as file:
        json.dump(logs, file)
