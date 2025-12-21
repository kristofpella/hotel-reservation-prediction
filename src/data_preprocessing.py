import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import load_data, read_yaml_file
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config_path = config_path

        self.config = read_yaml_file(self.config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
        
    
    def preprocess_data(self, df):
        try:
            logger.info(f"Starting data preprocessing step")

            logger.info(f"Dropping unique identifier columns and duplicate rows")
            df.drop(columns=['Unnamed: 0', 'Booking_ID'], inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']

            logger.info(f"Applying label encoding")

            label_encoder = LabelEncoder()
            mappings = {}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {label: code for label, code in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))}

            logger.info(f"Label mappings are:")

            for col, mapping in mappings.items():
                logger.info(f"{col}: {mapping}")

            logger.info(f"Doing Skewness Handling")

            skew_threshold = self.config['data_processing']['skewness_threshold']
            skewness = df[num_cols].apply(lambda x: x.skew())

            for column in skewness[skewness > skew_threshold].index:
                df[column] = np.log1p(df[column])
            
            return df
        
        except Exception as e:
            logger.error(f"Error in data preprocessing: {e}")
            raise CustomException(f"Error in data preprocessing: {e}", e)
    
    def balance_data(self, df):
        try:
            logger.info(f"Balancing data")
            X = df.drop(columns=['booking_status'])
            y = df['booking_status']

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)
            
            balanced_df = pd.DataFrame(X_resampled, columns = X.columns)
            balanced_df['booking_status'] = y_resampled

            logger.info(f"Balance data step completed")

            return balanced_df
        
        except Exception as e:
            logger.error(f"Error in balancing data: {e}")
            raise CustomException(f"Error in balancing data: {e}", e)

    def select_features(self, df):
        try:
            logger.info(f"Selecting features")
            X = df.drop(columns=['booking_status'])
            y = df['booking_status']

            model = RandomForestClassifier(random_state = 42)
            model.fit(X, y)

            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({'feature': X.columns, 'importance': feature_importance})

            top_features_by_importance_df = feature_importance_df.sort_values('importance', ascending = False)

            num_features_to_select = self.config['data_processing']['no_of_features']

            top_10_features = top_features_by_importance_df['feature'].head(num_features_to_select).values

            top_10_df = df[top_10_features.tolist() + ['booking_status']]

            logger.info(f"Selected {top_10_features} features successfully")

            return top_10_df

        except Exception as e:
            logger.error(f"Error in selecting features: {e}")
            raise CustomException(f"Error in selecting features: {e}", e)

    def save_data(self, df, file_path):
        try:
            logger.info(f"Saving data to processed directory {file_path}")

            df.to_csv(file_path, index=False)

            logger.info(f"Data saved successfully to {file_path}")
        
        except Exception as e:
            logger.error(f"Error in saving data: {e}")
            raise CustomException(f"Error in saving data: {e}", e)

    
    def process(self):
        try:
            logger.info(f"Loading data from RAW directory")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info(f"Data processing completed successfully")

        except Exception as e:
            logger.error(f"Error in data processing: {e}")
            raise CustomException(f"Error in data processing: {e}", e)


if __name__ == "__main__":
    data_processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_FILE_PATH)
    data_processor.process()
            
