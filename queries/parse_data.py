from pymongo import MongoClient
import json 
import pandas as pd

def save_to_csv(file_path, dataset):
    df = pd.read_json(json.dumps(dataset))
    df.to_csv(file_path + ".csv")

def save_to_json(file_path, dataset):
    with open(file_path + ".json","w",encoding="utf-8") as file:
        json.dump(dataset, file)

def final_collection(file_path, save_csv=False, save_json=False):
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
        save_to_json(file_path, dataset)

    if (save_csv):
        save_to_csv(file_path, dataset)

def counts_collection (file_path, save_csv=False, save_json=False):
    client = MongoClient('localhost')
    db = client['metrics']
    col = db['counts']

    data = list(col.find({}))
    dataset = []
    for elem in data:
        obj = {}
        obj['screencastName'] = elem['screencastName']
        for elto in elem['count']:
            words = elto['type'].split(" ")
            camelcase = ""
            for word in words:
                camelcase += word.capitalize()
            obj[camelcase] = elto['total']
        dataset.append(obj)
    
    if (save_json):
        save_to_json(file_path, dataset)

    if (save_csv):
        save_to_csv(file_path, dataset)