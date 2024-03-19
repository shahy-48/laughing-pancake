import numpy as np
import os
import pandas as pd
import sys

# Modeling
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, Ridge,Lasso
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from catboost import CatBoostRegressor
from xgboost import XGBRegressor

# Logging, config & exception
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from src.utils import save_object, evaluate_model

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self)->None:
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self, X_train:np.array, y_train:np.array, X_test:np.array, y_test:np.array)->str:
        """Initiates the model training process, chooses the best model and saves it to the specified file path"""
        try:
            logging.info('Initiating the model training process')
            models = {
                "Linear Regression": LinearRegression(),
                "Lasso": Lasso(),
                "Ridge": Ridge(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest Regressor": RandomForestRegressor(),
                "XGBRegressor": XGBRegressor(), 
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor()
            }
            model_list = []
            r2_list =[]
            mae_list = []
            rmse_list = []
            for model_name, model in models.items():
                logging.info(f'Training the model: {model_name}')
                model.fit(X_train, y_train)
                y_test_pred = model.predict(X_test)
                model_test_mae , model_test_rmse, model_test_r2 = evaluate_model(y_test, y_test_pred)
                model_list.append(model_name)
                r2_list.append(model_test_r2)
                mae_list.append(model_test_mae)
                rmse_list.append(model_test_rmse)
                logging.info(f'Model: {model_name} trained successfully')
            model_evaluation_df = pd.DataFrame({'Model':model_list, 'R2':r2_list, 'MAE':mae_list, 'RMSE':rmse_list})
            logging.info(f'Model evaluation report: \n{model_evaluation_df.sort_values(by = ["R2"], ascending=False)}')
            if max(model_evaluation_df['R2']) < 0.5:
                raise CustomException('No model has R2 score greater than 0.5',sys)
            else:
                logging.info('At least one model has R2 score greater than 0.5')
                best_model = model_evaluation_df[model_evaluation_df['R2'] == model_evaluation_df['R2'].max()]['Model'].values[0]
                logging.info(f'Best model: {best_model}')
                chosen_model = models[best_model]
                logging.info(f'Saving the best model: {best_model}')
                save_object(
                    self.model_trainer_config.trained_model_file_path, 
                    chosen_model)
                logging.info(f'Best model saved successfully at the file path: {self.model_trainer_config.trained_model_file_path}')
                return self.model_trainer_config.trained_model_file_path
        except Exception as e:
            raise CustomException(e,sys)