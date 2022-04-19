import json 
import numpy as np
import random
#import statistics
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, RepeatedKFold, RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

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

        #if obj['y'] == 4:
        #    obj['y'] = 3

    return dataset

def evaluate(model, x, y):
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

    random.shuffle(dataset)

    arrayX = []
    arrayY = []
    for each in dataset:
        arrayY.append(each['y'])
        arrayX.append(each['X'])

    X = np.array(arrayX)
    y = np.array(arrayY)

    # muestrea un conjunto de entrenamiento almacenando el 40% de datos para probar
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

    #cv = KFold(n_splits=10)
    #cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3)
    fold_number = 1
    list_r2 = []
    list_mae = []
    list_mse = []
    for train, test in cv.split(X, y):
        x_train = X[train]
        y_train = y[train]
        x_test = X[test]
        y_test = y[test]

        sd = StandardScaler()
        sd.fit(x_train)
        x_train = sd.transform(x_train)
        x_test = sd.transform(x_test)

        model = LinearRegression()
        #model = DecisionTreeClassifier()
        model.fit(x_train, y_train)

        print("------------------------------------------")
        print("FOLD NUMBER " + str(fold_number))
        fold_number += 1

        training_result = evaluate(model, x_train, y_train)
        print("Training evaluate results")
        print(training_result)

        testing_result = evaluate(model, x_test, y_test)
        print("Testing evaluate results")
        print(testing_result)
        list_r2.append(testing_result['R^2'])
        list_mae.append(testing_result['MAE'])
        list_mse.append(testing_result['MSE'])

        print("------------------------------------------")
        print("")

    print('R^2: %.3f (%.3f)' % (np.mean(list_r2), np.std(list_r2)))
    print('MAE: %.3f (%.3f)' % (np.mean(list_mae), np.std(list_mae)))
    print('MSE: %.3f (%.3f)' % (np.mean(list_mse), np.std(list_mse)))

if __name__ == "__main__":
    main()