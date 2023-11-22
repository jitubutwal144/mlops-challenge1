import sys

import pandas as pd

from src.exceptions.exception import SensorException


class SensorData:
    """
    This class helps to read data from the data source(csv) and convert it to pandas DataFrame
    """

    def __init__(self):
        try:
            self.historical_sensor_data_path = (
                "notebooks/data/historical_sensor_data.csv"
            )
        except Exception as e:
            raise SensorException(e, sys)

    def get_historical_data_as_dataframe(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.historical_sensor_data_path)
            return df
        except Exception as e:
            raise SensorException(e, sys)
