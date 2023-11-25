import os
import pickle
import sys

import numpy as np
import yaml
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exceptions.exception import SensorException


def save_object(file_path, obj):
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise SensorException(e, sys)


def evaluate_model(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}
        for i in range(len(list(models))):
            # Among multiple models, get current model
            model = list(models.values())[i]
            model_name = list(models.keys())[i]
            hyperparameter = params[model_name]

            # For each model train and get best parameters and finally get r2 score
            gs = GridSearchCV(model, hyperparameter, cv=3)
            gs.fit(X_train, y_train)

            # Get best parameters from above and train current model
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_test_predicted = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_predicted)

            report[model_name] = test_model_score

        return report

    except Exception as e:
        raise SensorException(e, sys)


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SensorException(e, sys) from e


def write_yaml_file(
    file_path: str, content: object, replace: bool = False
) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise SensorException(e, sys)


def save_numpy_array_data(file_path: str, array: np.array) -> None:
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise SensorException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e


def load_object(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exists")
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e
