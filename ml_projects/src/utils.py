import os
import sys
import numpy as np
import pandas as pd
import dill
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
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

def evaluate_model(true, predicted):
    """Evaluates the model using the true and predicted values"""
    mae = mean_absolute_error(true, predicted)
    mse = mean_squared_error(true, predicted)
    rmse = np.sqrt(mean_squared_error(true, predicted))
    r2_square = r2_score(true, predicted)
    return mae, rmse, r2_square