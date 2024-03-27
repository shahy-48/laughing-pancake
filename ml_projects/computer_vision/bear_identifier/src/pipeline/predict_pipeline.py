import sys
from src.exception import CustomException
from src.utils import load_object
from PIL import Image
from fastai.vision.all import *

# Function to make predictions
def classify_bear(image):
    try:
        categories = ['Black Bear','Grizzly Bear','Teddy Bear']
        model_path = "artifacts/model.pkl"
        model = load_object(model_path)
        # Make prediction using the model
        _,_,probs = model.predict(image)
        # Return predicted class
        return dict(zip(categories,map(float,probs)))
    except Exception as e:
        raise CustomException(e,sys)
        
    