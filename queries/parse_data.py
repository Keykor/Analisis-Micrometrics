from pymongo import MongoClient
import json 
import os
from pathlib import Path
import pandas as pd

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
    
    with open("raw_logs.json","w",encoding="utf-8") as file:
        json.dump(dataset, file)
    
    df = pd.read_json("raw_logs.json")
    filepath = os.path.join(Path().absolute(), 'raw_logs.csv')
    df.to_csv(filepath)
