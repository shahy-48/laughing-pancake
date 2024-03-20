from dataclasses import dataclass
import os
import pandas as pd
import sys
from src.logger import logging
from src.exception import CustomException
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_object_file_path: str = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self)->None:
        self.transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        
        """Transforms the features and creates a preprocessor object to be used in the model training process"""
        
        try:
            numerical_features = [
                'writing_score',
                'reading_score'
            ]
            categorical_features = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course',
            ]
            logging.info(f'Numerical features identified : {numerical_features}')
            logging.info(f'Categorical features identified : {categorical_features}')
            logging.info(f'Creating the preprocessor object using the identified features')
            numerical_pipleline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])

            categorical_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent', fill_value='missing')),
                ('onehot', OneHotEncoder(handle_unknown='ignore')),
                ('scaler', StandardScaler(with_mean=False))
            ])

            preprocessor = ColumnTransformer(
                transformers=[
                    ('numerical_pipeline', numerical_pipleline, numerical_features),
                    ('categorical_pipeline', categorical_pipeline, categorical_features)
                ]
            )
            logging.info('Preprocessor object created successfully')
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self, train_data_path:str, test_data_path:str, to_predict:str)->tuple:
        """Initiates the data transformation process"""
        logging.info('Initiating data transformation through data transformation component')
        try:
            train_data = pd.read_csv(train_data_path)
            test_data = pd.read_csv(test_data_path)
            logging.info('Reading csv data into dataframes')

            logging.info('Data transformation initiated using the preprocessor object')
            preprocessor_object = self.get_data_transformer_object()
            X_train, X_test = preprocessor_object.fit_transform(train_data.drop(columns=to_predict, axis=1)), preprocessor_object.fit_transform(test_data.drop(columns=to_predict, axis=1))
            y_train, y_test = train_data[to_predict], test_data[to_predict]
            logging.info('Data transformation completed')
            save_object(
                file_path = self.transformation_config.preprocessor_object_file_path,
                object_to_save = preprocessor_object
            )
            logging.info('Preprocessor object saved successfully')
            return X_train, X_test, y_train, y_test, self.transformation_config.preprocessor_object_file_path
        
        except Exception as e:
            raise CustomException(e,sys)


        

        
        
        
