import os
import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from utils.common_functions import read_yaml_file
from config.paths_config import *

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.bucket_file_name = self.config['bucket_file_name']
        self.train_ratio = self.config['train_ratio']
        self.credentials_path = self.config.get('credentials_path', None)

        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"Data ingestion started with {self.bucket_name} and file is {self.bucket_file_name}")

    def download_csv_from_gcp(self):
        try:
            # Use service account credentials if provided
            if self.credentials_path and os.path.exists(self.credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                client = storage.Client(credentials=credentials)
            else:
                # Try to use default credentials
                client = storage.Client()
            
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"CSV file downloaded successfully from {self.bucket_name} and file is {self.bucket_file_name}")
        
        except Exception as e:
            logger.error(f"Error downloading CSV file from {self.bucket_name} and file is {self.bucket_file_name}: {e}")
            raise CustomException(f"Error downloading CSV file from {self.bucket_name} and file is {self.bucket_file_name}", e)


    def split_data_into_train_test(self):
        try:
            logger.info(f"Splitting data into train and test with {self.train_ratio}")
            data = pd.read_csv(RAW_FILE_PATH)
            train_data , test_data =train_test_split(data, test_size=1-self.train_ratio, random_state=42)

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)

            logger.info(f"Data split into train and test successfully to {TRAIN_FILE_PATH} and {TEST_FILE_PATH}")

        except Exception as e:
            logger.error(f"Error splitting data into train and test: {e}")
            raise CustomException(f"Error splitting data into train and test", e)
    
    def initiate_data_ingestion(self):
        try:
            logger.info(f"Initiating data ingestion")
            self.download_csv_from_gcp()
            self.split_data_into_train_test()

        except Exception as e:
            logger.error(f"Error initiating data ingestion: {e}")
            raise CustomException(f"Error initiating data ingestion", e)

        finally:
            logger.info(f"Data ingestion completed successfully")

if __name__ == "__main__":
    config = read_yaml_file(CONFIG_FILE_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.initiate_data_ingestion()