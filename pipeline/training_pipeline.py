from config.paths_config import *
from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml_file


if __name__ == "__main__":
    ### DATA INGESTION ###
    config = read_yaml_file(CONFIG_FILE_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.initiate_data_ingestion()

    ### DATA PROCESSING ###
    data_processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_FILE_PATH)
    data_processor.process()

    ### MODEL TRAINING ###
    model_training = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    model_training.run()