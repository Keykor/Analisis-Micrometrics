import json 
import numpy as np
import random
#import statistics
from sklearn.linear_model import LinearRegression
from sklearn import metrics

def generate_dataset(filename):
    logs = None
    with open(filename, encoding="utf-8") as file:
        logs = json.load(file)

    dataset = []
    for elem in logs:
        elem.pop('name', None)
        obj = {}
        obj['y'] = elem.pop('level', None)
        obj['X'] = []
        for clave, valor in elem.items():
            obj['X'].append(valor)
        dataset.append(obj)

    return dataset

def calculate_metrics(model, x, y):
    y_pred = model.predict(x)
    #error absoluto medio cuanto se erra con lo predicho
    #r2 es entre -1 y 1 -> arriba de 0.5 es bueno
    #     
    return {
        'MAE': metrics.mean_absolute_error(y_pred,y),
        'MSE': metrics.mean_squared_error(y_pred,y),
        'R^2': metrics.r2_score(y,y_pred)
    }

def main():
    dataset = generate_dataset('logs.json')

    metrics = []
    for i in range(0, 1000):
        random.shuffle(dataset)
        arrayX = []
        arrayY = []
        for each in dataset:
            arrayY.append(each['y'])
            arrayX.append(each['X'])

        X = np.array(arrayX)
        y = np.array(arrayY)

        reg = LinearRegression(normalize=True)
        reg.fit(X,y)

        metric = calculate_metrics(reg, X, y)
        metrics.append(metric)
        print(metric)

    #print(statistics.mean(scores))
    #print(min(scores))
    #print(max(scores))

if __name__ == "__main__":
    main()