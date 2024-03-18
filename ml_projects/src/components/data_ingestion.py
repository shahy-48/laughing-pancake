from dataclasses import dataclass
import os
import pandas as pd
import sys
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split

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
            students_data = pd.read_csv('data/stud.csv')
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
