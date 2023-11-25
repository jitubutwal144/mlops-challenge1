import sys

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.constants.training_pipeline import TARGET_COLUMN
from src.entities.artifact_entity import DataTransformationArtifact
from src.entities.artifact_entity import DataValidationArtifact
from src.entities.config_entity import DataTransformationConfig
from src.exceptions.exception import SensorException
from src.logger import logging
from src.utils import save_numpy_array_data
from src.utils import save_object


class DataTransformation:
    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        """
        :param1 data_validation_artifact: Output reference of data ingestion artifact stage
        :param2 data_transformation_config: configuration for data transformation
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)

    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        try:
            standard_scaler = StandardScaler()
            simple_imputer = SimpleImputer(strategy="median")
            preprocessor = Pipeline(
                steps=[
                    (
                        "Imputer",
                        simple_imputer,
                    ),
                    (
                        "StandardScaler",
                        standard_scaler,
                    ),  # keep every feature in same range and handle outlier
                ]
            )

            return preprocessor

        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_data_transformation(
        self,
    ) -> DataTransformationArtifact:
        try:
            train_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_train_file_path
            )
            test_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_test_file_path
            )
            preprocessor = self.get_data_transformer_object()

            # training dataframe
            input_feature_train_df = train_df.drop(
                columns=[TARGET_COLUMN], axis=1
            )
            target_feature_train_df = train_df[TARGET_COLUMN]

            # testing dataframe
            input_feature_test_df = test_df.drop(
                columns=[TARGET_COLUMN], axis=1
            )
            target_feature_test_df = test_df[TARGET_COLUMN]

            # fit training feature data into data preprocssor
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(
                input_feature_train_df
            )
            transformed_input_test_feature = preprocessor_object.transform(
                input_feature_test_df
            )

            train_arr = np.c_[
                transformed_input_train_feature,
                np.array(target_feature_train_df),
            ]
            test_arr = np.c_[
                transformed_input_test_feature, np.array(target_feature_test_df)
            ]

            # save numpy array data
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                array=train_arr,
            )
            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                array=test_arr,
            )
            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor_object,
            )

            # preparing artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
            logging.info(
                f"Data transformation artifact: {data_transformation_artifact}"
            )
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
