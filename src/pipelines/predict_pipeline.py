import os
import sys

import pandas as pd

from src.exceptions.exception import SensorException
from src.utils import load_object


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            # TODO: get laster model and preprocessor from another responsible class
            # TODO: Remove harcoded artifacts name, inject them as a configs
            model_path = os.path.join("artifacts", "model.pkl")
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            X_inference = pd.DataFrame(features).values
            data_scaled = preprocessor.transform(X_inference)
            y_predictions = model.predict_proba(data_scaled)
            return y_predictions

        except Exception as e:
            raise SensorException(e, sys)


class InferenceData:
    def __init__(self):
        pass

    def get_data_as_data_frame(self):
        try:
            inference_data_path = os.path.join(
                "artifacts", "inference_sensor_data.csv"
            )
            # TODO: optimize all read file operations using Adapter pattern. Eg
            # create Reader.read(new CSVReader() OR new ParquetReader() or new JSONReader())
            inference_df = pd.read_csv(inference_data_path)
            return inference_df
        except Exception as e:
            raise SensorException(e, sys)
