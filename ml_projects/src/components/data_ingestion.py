from dataclasses import dataclass
import os
import pandas as pd
import sys
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts','data','train.csv')
    test_data_path: str = os.path.join('artifacts','data','test.csv')
    raw_data_path: str = os.path.join('artifacts','data','raw_data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Initiating data ingestion through data ingestion component')
        try:
            students_data = pd.read_csv('Notebook/stud.csv')
            logging.info('Reading csv data initiated')

            # saving the raw data in the artifcacts folder
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            students_data.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info('raw data artifact completed')

            logging.info('Splitting the data into train and test initiated')
            train_data, test_data = train_test_split(students_data, test_size=0.2, random_state=48)
            train_data.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info('Splitting the data into train and test completed & artifacts saved')
            logging.info('Data ingestion completed')

            return self.ingestion_config.train_data_path, self.ingestion_config.test_data_path
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == '__main__':
    di = DataIngestion()
    train_data_path, test_data_path = di.initiate_data_ingestion()
    df = DataTransformation()
    X_train, X_test, y_train, y_test, preprocessor_object_file_path = df.initiate_data_transformation(train_data_path, test_data_path, 'math_score')
    chose_model_filepath = ModelTrainer().initiate_model_trainer(X_train, y_train, X_test, y_test)
    print(chose_model_filepath)