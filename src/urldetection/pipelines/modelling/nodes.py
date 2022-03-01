"""
This is a boilerplate pipeline 'modelling'
generated using Kedro 0.17.7
"""
import logging
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split, GridSearchCV
from imblearn.pipeline import Pipeline 
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.under_sampling import RandomUnderSampler
from xgboost import XGBClassifier


def split_data(data: pd.DataFrame, parameters: Dict) -> Tuple:
    X = data.drop(['label', 'url', 'geo_loc', 'tld'], axis=1)
    y = data['label']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=parameters["test_size"], random_state=parameters["random_state"]
    )
    return X_train, X_test, y_train, y_test

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> LinearRegression:
    num_cols = X_train.select_dtypes(include=np.number).columns.tolist()
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy="mean")),
        ('std_scaler', StandardScaler())
    ])

    cat_cols = X_train.select_dtypes(include=object).columns.tolist()
    cat_pipeline = Pipeline([
        ('enc', OneHotEncoder())
        ])

    pre_pipeline = ColumnTransformer([
            ("num", num_pipeline, num_cols),
            ("cat", cat_pipeline, cat_cols),
        ], remainder = 'passthrough')

    sampler = RandomUnderSampler(sampling_strategy = 0.3)
    xgb = XGBClassifier(use_label_encoder = False, eval_metric='mlogloss')

    pipe = Pipeline([
        ('pre', pre_pipeline),
        ('sampler', sampler),
        ('xgb', xgb)
    ])
    param_grid = {
        'xgb__n_estimators': [5, 10, 50], 
        'xgb__gamma' : [0, 0.2, 0.5]
    }
    search = GridSearchCV(pipe, param_grid, scoring = 'f1', cv = 3)    
    search.fit(X_train, y_train)
    return search


def evaluate_model(
    search, X_test: pd.DataFrame, y_test: pd.Series
):
    """Calculates and logs the coefficient of determination.

    Args:
        regressor: Trained model.
        X_test: Testing data of independent features.
        y_test: Testing data for price.
    """
    y_pred = search.predict(X_test)
    score = f1_score(y_pred, y_test)
    logger = logging.getLogger(__name__)
    logger.info("Model has an F1 score of of %.3f on test data.", score)