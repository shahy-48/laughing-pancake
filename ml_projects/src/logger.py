import logging
import os
from datetime import datetime

# Create the standard format for logs
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# Define standard path for logs
LOG_PATH = os.path.join(os.path.join(os.getcwd(), 'logs', LOG_FILE))
# Create the logs directory if it does not exist
os.makedirs(LOG_PATH, exist_ok=True)
# Create the log file path
LOG_FILE_PATH = os.path.join(LOG_PATH, LOG_FILE)
# Set the logging configuration
logging.basicConfig(
    filename=LOG_FILE_PATH, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )
