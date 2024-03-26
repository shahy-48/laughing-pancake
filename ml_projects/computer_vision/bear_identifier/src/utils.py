import os
import sys
import dill
import pickle
from src.exception import CustomException
from src.logger import logging

def save_object(file_path:str, object_to_save:object)->None:
    """Saves the object to the specified file path"""
    try:
        logging.info(f'Saving the object to the file path: {file_path}')
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        logging.info(f'Directory created at the file path: {dir_path}')

        with open(file_path, 'wb') as file:
            dill.dump(object_to_save, file)
    
    except Exception as e:
        raise CustomException(e,sys)

def load_object(file_path):
    """Loads the object from the specified file path"""
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)