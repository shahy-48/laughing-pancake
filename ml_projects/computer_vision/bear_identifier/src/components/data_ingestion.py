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
    raw_data_path = os.path.join('artifacts','data','raw_data')

class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info("Starting data ingestion")
        try:
            logging.info("Searching for images through duckduckgo...")
            logging.info("Downloading the images...")
            searches = ['Black Bear','Grizzly Bear','Teddy Bear']
            # saving the raw data in the artifacts folder
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            path = Path(self.ingestion_config.raw_data_path)
            for search in searches:
                destination = (path/search)
                destination.mkdir(exist_ok = True, parents = True)
                download_images(destination, urls=search_images_ddg(f'{search} photo'))
                sleep(10)  # Pause between searches to avoid over-loading server
                download_images(destination, urls=search_images_ddg(f'{search} sun photo'))
                sleep(10)
                download_images(destination, urls=search_images_ddg(f'{search} shade photo'))
                sleep(10)
                resize_images(destination, max_size=400, dest=destination)
            logging.info("Images downloaded successfully")
            # remove failed image downloads
            failed = verify_images(get_image_files(path))
            failed.map(Path.unlink)
            logging.info("Got rid of corrupted/failed images successfully")

        except Exception as e:
            raise CustomException(e,sys)





