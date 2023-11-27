import os
import sys

import pandas as pd
from sklearn.model_selection import train_test_split

from src.data_clients.sensor_data import SensorData
from src.entities.artifact_entity import DataIngestionArtifact
from src.entities.config_entity import DataIngestionConfig
from src.entities.config_entity import TrainingPipelineConfig
from src.exceptions.exception import SensorException
from src.logger import logging


# from .model_trainer import ModelTrainer
class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)

    def export_data_into_feature_store(self) -> pd.DataFrame:
        """
        Export sensor data record as data frame into feature
        """
        try:
            logging.info("Exporting data from csv to feature store")
            sensor_data = SensorData()
            dataframe = sensor_data.get_historical_data_as_dataframe()
            feature_store_file_path = (
                self.data_ingestion_config.feature_store_file_path
            )

            # creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise SensorException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> None:
        """
        Feature store dataset will be split into train and test file
        """

        try:
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
            )

            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )

            dir_path = os.path.dirname(
                self.data_ingestion_config.training_file_path
            )

            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting train and test file path.")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True,
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True,
            )

            logging.info("Exported train and test file path.")
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_data_into_feature_store()
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)


if __name__ == "__main__":
    train_pipeline_config = TrainingPipelineConfig()
    ingestion_config = DataIngestionConfig(train_pipeline_config)
    ingestion_obj = DataIngestion(ingestion_config)
    ingestion_artifacts = ingestion_obj.initiate_data_ingestion()

    # data_transformer = DataTransformation()
    # train_arr, test_arr, _ = data_transformer.initiate_data_transformation(
    #     train_data_path, test_data_path
    # )

    # model_trainer = ModelTrainer()
    # model_trainer.initiate_model_trainer(train_arr, test_arr)
