from pymongo import MongoClient
import json 
import os
from pathlib import Path
import pandas as pd

def execute(filename="raw_logs"):
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
    
    with open(filename + ".json","w",encoding="utf-8") as file:
        json.dump(dataset, file)
    
    df = pd.read_json(filename + ".json")
    filepath = os.path.join(Path().absolute(), filename + ".csv")
    df.to_csv(filepath)
