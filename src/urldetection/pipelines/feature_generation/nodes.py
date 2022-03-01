"""
This is a boilerplate pipeline 'feature_generation'
generated using Kedro 0.17.7
"""

from .URLFeatureGenerator import URLFeatureGenerator
import pandas as pd

def create_features(url_df):
    feature_list = []
    # iterate through the urls while generating features
    for url, label in zip(url_df['url'], url_df['label']):
        features = URLFeatureGenerator(url).create_features()
        features['label'] = label
        feature_list.append(features)
    feature_df = pd.DataFrame.from_dict(feature_list)
    return feature_df