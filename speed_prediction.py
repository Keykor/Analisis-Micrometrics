import pandas as pd
from pathlib import Path
import os

def calculate(filename):
    directory = os.path.join(Path().absolute(), "speed_prediction_logs")
    path = os.path.join(directory, filename + ".csv")
    df = pd.read_csv(path)

    df = df.fillna(0)
    df = df[df["avgSpeedPerTest"] > 0]
    df = df[df["avgIntratecla"] > 0]
    df = df[df["avgScrollSpeed"] > 0]

    df["sum" + filename] = df["avgSpeedPerTest"] + df["avgIntratecla"] + df["avgScrollSpeed"]
    df["mul" + filename] = df["avgSpeedPerTest"] * df["avgIntratecla"] * df["avgScrollSpeed"]

    column_names = df.columns.values.tolist()
    column_names.remove('name')
    column_names.remove("sum" + filename)
    column_names.remove("mul" + filename)
    for name in column_names:
        df.pop(name)
    
    return df

def main():
    directory = os.path.join(Path().absolute(), "speed_prediction_logs")
    path = os.path.join(directory, "eventAmountPerTest.csv")
    df = pd.read_csv(path)

    logs = ["100", "300", "500", "700", "1000", "all"]
    for name in logs:
        df = df.merge(right=calculate(name), on='name', how='left')
    print(df)
    df.to_csv('speed_prediction.csv')

    for name in logs:
        df["sum"+name] = df["sum"+name]  / df["sumall"]
        df["mul"+name] = df["mul"+name]  / df["mulall"]

    df.to_csv('speed_prediction_normalized.csv')
    pass

if __name__ == "__main__":
    main()