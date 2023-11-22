import os
import sys
from dataclasses import dataclass

from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.metrics import r2_score

from src.exceptions.exception import CustomException
from src.logger import logging
from src.utils import evaluate_model
from src.utils import save_object


@dataclass
class ModelTrainerConfig:
    # TODO: dynamic model versioning
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self) -> None:
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_arr, test_arr):
        try:
            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],  # all rows, exclude last column
                train_arr[:, -1],  # all rows, last column
                test_arr[:, :-1],  # all rows, exclude last column
                test_arr[:, -1],  # all rows, last column
            )

            logging.info("Prepared X_train, y_train, X_test, y_test data")

            # Algorithms to tryout
            models = {
                "Gaussian Classifier": GaussianProcessClassifier(
                    1.0 * RBF(1.0)
                ),
            }

            # Pramas for hyprparameter tunning
            params = {
                "Gaussian Classifier": {},
            }
            model_report: dict = evaluate_model(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                params=params,
            )

            logging.info(f"Model report: {model_report}")
            model_score_list = list(model_report.values())
            best_model_score = max(sorted(model_score_list))

            model_names_list = list(models.keys())
            best_model_name = model_names_list[
                model_score_list.index(best_model_score)
            ]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("Best model not found")

            logging.info(f"Found best model: {best_model_name}")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model,
            )
            y_test_predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, y_test_predicted)

            return r2_square

        except Exception as e:
            raise CustomException(e, sys)
