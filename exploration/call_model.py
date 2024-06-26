import pandas as pd
from sklearn.linear_model import LinearRegression


def call_fe_model(model: LinearRegression, vec: pd.DataFrame):
    vec = vec.reindex(sorted(vec.columns), axis=1)
    vec = vec.drop(columns=['hvost_fact_lagged'])
    return model.predict(vec)[0]


def call_hvost_model(model: LinearRegression, vec: pd.DataFrame):
    vec = vec.reindex(sorted(vec.columns), axis=1)
    vec = vec.drop(columns=['fe_fact_lagged'])
    return model.predict(vec)[0]
