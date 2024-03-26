from dataclasses import dataclass
import os
import sys
from src.logger import logging
from src.exception import CustomException
from fastbook import search_images_ddg
from fastdownload import download_url
from fastai.vision.all import *
from time import sleep

@dataclass
class DataIngestionConfig:
    train_data_path = os.path.join('artifacts','data','train_data')
    test_data_path = os.path.join('artifacts','data','test_data')
    raw_data_path = os.path.join('artifacts','data','raw_data')

class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info("Starting data ingestion")
        try:
            logging.info("Searching for images through duckduckgo...")
            black_bear_images = search_images_ddg('Black Bear photos')
            grizzly_bear_images = search_images_ddg('Grizzly Bear photos')
            teddy_bear_images = search_images_ddg('Teddy Bear photos')

            logging.info("Downloading the images...")
            searches = ['Black Bear','Grizzly Bear','Teddy Bear']
            url_list = [black_bear_images, grizzly_bear_images, teddy_bear_images]
            # saving the raw data in the artifcacts folder
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            for search, url in zip(searches,url_list):
                destination = os.path.join(self.ingestion_config.raw_data_path,search)
                os.makedirs(destination, exist_ok = True)
                download_images(destination, urls = url)
                sleep(10)  # Pause between searches to avoid over-loading server
                download_images(destination, urls=search_images_ddg(f'{search} sun photo'))
                sleep(10)
                download_images(destination, urls=search_images_ddg(f'{search} shade photo'))
                sleep(10)
                resize_images(destination, max_size=400, destination=destination)
            logging.info("Images downloaded successfully")
        except Exception as e:
            raise CustomException(e,sys)





