import sys

from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

from src.entities.artifact_entity import ClassificationMetricArtifact
from src.exceptions.exception import SensorException


def get_classification_score(
    y_actual, y_predicted
) -> ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score(y_actual, y_predicted)
        model_recall_score = recall_score(y_actual, y_predicted)
        model_precision_score = precision_score(y_actual, y_predicted)

        classsification_metric = ClassificationMetricArtifact(
            f1_score=float(model_f1_score),
            precision_score=float(model_precision_score),
            recall_score=float(model_recall_score),
        )
        return classsification_metric
    except Exception as e:
        raise SensorException(e, sys)
