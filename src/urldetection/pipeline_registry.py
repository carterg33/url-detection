"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline

from urldetection.pipelines import feature_generation as fg
from urldetection.pipelines import modelling as ml

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    create_features_pipeline = fg.create_pipeline()
    create_modelling_pipeline = ml.create_pipeline()

    return {"__default__": create_features_pipeline + create_modelling_pipeline,
    "fg" : create_features_pipeline,
    "ml" : create_modelling_pipeline}
