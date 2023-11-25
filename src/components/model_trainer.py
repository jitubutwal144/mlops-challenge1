import os
import sys

from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF

from src.entities.artifact_entity import DataTransformationArtifact
from src.entities.artifact_entity import ModelTrainerArtifact
from src.entities.config_entity import ModelTrainerConfig
from src.exceptions.exception import SensorException
from src.logger import logging
from src.ml.metrics.classification_metric import get_classification_score
from src.ml.model.estimator import SensorModel
from src.utils import load_numpy_array_data
from src.utils import load_object
from src.utils import save_object


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact,
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def perform_hyper_parameter_tuning(self):
        pass

    def train_model(self, X_train, y_train):
        try:
            # Algorithm to tryout
            model = GaussianProcessClassifier(1.0 * RBF(1.0))
            model.fit(X_train, y_train.ravel())
            return model
        except Exception as e:
            raise e

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = (
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_file_path = (
                self.data_transformation_artifact.transformed_test_file_path
            )

            # Loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model = self.train_model(X_train, y_train)
            y_train_pred = model.predict(X_train)

            # Get standard classification metrics, f1_score, precision, recall
            classification_train_metric = get_classification_score(
                y_actual=y_train, y_predicted=y_train_pred
            )

            if (
                classification_train_metric.f1_score
                <= self.model_trainer_config.expected_accuracy
            ):
                raise Exception(
                    "Trained model is not good to provide expected accuracy"
                )

            # Use test data
            y_test_pred = model.predict(X_test)
            classification_test_metric = get_classification_score(
                y_actual=y_test, y_predicted=y_test_pred
            )

            # Overfitting and Underfitting evaluation
            diff = abs(
                classification_train_metric.f1_score
                - classification_test_metric.f1_score
            )

            if (
                diff
                > self.model_trainer_config.overfitting_underfitting_threshold
            ):
                raise Exception(
                    "Model is not good try to do more experimentation."
                )

            preprocessor = load_object(
                file_path=self.data_transformation_artifact.transformed_object_file_path
            )

            model_dir_path = os.path.dirname(
                self.model_trainer_config.trained_model_file_path
            )
            os.makedirs(model_dir_path, exist_ok=True)
            sensor_model = SensorModel(preprocessor=preprocessor, model=model)
            save_object(
                self.model_trainer_config.trained_model_file_path,
                obj=sensor_model,
            )

            # model trainer artifact

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric,
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)
