from data_ingestion import DataIngestion
from data_transformation import DataTransformation
from model_trainer import ModelTrainer

di = DataIngestion()
train_data_path, test_data_path = di.initiate_data_ingestion()
df = DataTransformation()
X_train, X_test, y_train, y_test, preprocessor_object_file_path = df.initiate_data_transformation(train_data_path, test_data_path, 'math_score')
chose_model_filepath = ModelTrainer().initiate_model_trainer(X_train, y_train, X_test, y_test)