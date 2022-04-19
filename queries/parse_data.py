from pymongo import MongoClient
import json 
import pandas as pd

def execute(file_path, save_csv=False, save_json=False):
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
    
    if (save_json):
        with open(file_path + ".json","w",encoding="utf-8") as file:
            json.dump(dataset, file)

    if (save_csv):
        df = pd.read_json(json.dumps(dataset))
        df.to_csv(file_path + ".csv")
