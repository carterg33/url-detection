"""
This is a boilerplate pipeline 'feature_generation'
generated using Kedro 0.17.7
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_features

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=create_features,
            inputs="urls",
            outputs="features",
            name="create_features_node",
            )
        ]
    )
