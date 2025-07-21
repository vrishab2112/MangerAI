import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import logging

logger = logging.getLogger(__name__)

class DataAgent:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def load_data(self, file_path):
        """
        Load data from CSV or Excel file
        
        Args:
            file_path (str): Path to the data file
            
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format. Please use CSV or Excel files.")
            
            logger.info(f"Successfully loaded data from {file_path}")
            return df
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
            
    def preprocess_data(self, df, target_column):
        """
        Preprocess the data for machine learning
        
        Args:
            df (pd.DataFrame): Input dataframe
            target_column (str): Name of the target column
            
        Returns:
            dict: Preprocessed data including train and test sets
        """
        try:
            # Handle missing values
            df = self._handle_missing_values(df)
            
            # Encode categorical variables
            df = self._encode_categorical_variables(df, target_column)
            
            # Split features and target
            X = df.drop(columns=[target_column])
            y = df[target_column]
            
            # Scale numerical features
            X = self._scale_features(X)
            
            # Split into train and test sets
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            return {
                'X_train': X_train,
                'X_test': X_test,
                'y_train': y_train,
                'y_test': y_test,
                'feature_names': X.columns.tolist()
            }
            
        except Exception as e:
            logger.error(f"Error preprocessing data: {str(e)}")
            raise
            
    def _handle_missing_values(self, df):
        """Handle missing values in the dataset"""
        # For numerical columns, fill with median
        numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
        df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())
        
        # For categorical columns, fill with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])
        
        return df
        
    def _encode_categorical_variables(self, df, target_column):
        """Encode categorical variables using Label Encoding"""
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            if col != target_column:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                self.label_encoders[col] = le
                
        return df
        
    def _scale_features(self, X):
        """Scale numerical features using StandardScaler"""
        numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
        X[numerical_cols] = self.scaler.fit_transform(X[numerical_cols])
        return X 