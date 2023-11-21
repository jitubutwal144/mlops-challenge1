import sys
import os
import numpy as np
import pandas as pd
from src.logger import logging
from src.exceptions.exception import CustomException
from dataclasses import dataclass

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from src.utils import save_object


@dataclass
class DataTransformationConfig:
  ''' 
    Holds configs required for data transformation steps.
  '''
  # TODO: preprocessor with parquet file
  preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
  def __init__(self):
    self.data_transformation_config = DataTransformationConfig()

  def get_data_transformer_object(self):
    '''
      - Check numerical values vs categorical values(does not exist)
      - Handle missing values using simple imputer
      - Handle categorical features using one hot encoding and scaling feature values if reuqired
    '''
    try:
      numerical_columns = ['sensor_1', 'sensor_2']

      # Data transformation for numerical features
      numerical_pipeline = Pipeline(
        steps = [
          ('imputer', SimpleImputer(strategy='median')),
          ('scaler', StandardScaler())
        ]
      )

      logging.info(f"Numerical features: {numerical_columns}")

      preprocessor = ColumnTransformer(
        [
          ('num_pipeline', numerical_pipeline, numerical_columns),
        ]
      )

      return preprocessor
    except Exception as e:
      raise CustomException(e, sys)

  def initiate_data_transformation(self, train_path, test_path):
    try:
      traget_column_name = 'label'
      preprocessing_obj = self.get_data_transformer_object()

      train_df = pd.read_csv(train_path)
      test_df = pd.read_csv(test_path)

      input_feature_train_df = train_df.drop(columns=[traget_column_name], axis=1)
      target_feature_train_df = train_df[traget_column_name]

      input_feature_test_df = test_df.drop(columns=[traget_column_name], axis=1)
      target_feature_test_df = test_df[traget_column_name]
      

      input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
      input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

      # Convert to numpy array
      train_arr = np.c_[
        input_feature_train_arr, np.array(target_feature_train_df),
      ]

      test_arr = np.c_[
        input_feature_test_arr, np.array(target_feature_test_df)
      ]

      save_object(
        file_path = self.data_transformation_config.preprocessor_obj_file_path,
        obj = preprocessing_obj
      )

      return (
        train_arr,
        test_arr,
        self.data_transformation_config.preprocessor_obj_file_path
      )  

    except Exception as e:
      raise CustomException(e, sys)
      