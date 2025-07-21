import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger(__name__)

class AnalysisAgent:
    def __init__(self):
        pass
        
    def analyze_data(self, data_dict):
        """
        Perform exploratory data analysis on the preprocessed data
        
        Args:
            data_dict (dict): Dictionary containing preprocessed data
            
        Returns:
            dict: Analysis results
        """
        try:
            X_train = data_dict['X_train']
            y_train = data_dict['y_train']
            feature_names = data_dict['feature_names']
            
            analysis_results = {
                'basic_stats': self._get_basic_stats(X_train),
                'correlation_matrix': self._get_correlation_matrix(X_train),
                'feature_distributions': self._analyze_feature_distributions(X_train),
                'target_distribution': self._analyze_target_distribution(y_train)
            }
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in data analysis: {str(e)}")
            raise
            
    def get_feature_importance(self, data_dict, target_column):
        """
        Calculate feature importance using Random Forest
        
        Args:
            data_dict (dict): Dictionary containing preprocessed data
            target_column (str): Name of the target column
            
        Returns:
            dict: Feature importance scores
        """
        try:
            X_train = data_dict['X_train']
            y_train = data_dict['y_train']
            feature_names = data_dict['feature_names']
            
            # Determine if it's a classification or regression problem
            unique_values = len(np.unique(y_train))
            if unique_values < 10:  # Classification if less than 10 unique values
                model = RandomForestClassifier(n_estimators=100, random_state=42)
            else:
                model = RandomForestRegressor(n_estimators=100, random_state=42)
                
            model.fit(X_train, y_train)
            
            # Get feature importance
            importance_scores = model.feature_importances_
            feature_importance = dict(zip(feature_names, importance_scores))
            
            # Sort features by importance
            sorted_features = sorted(
                feature_importance.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            return {
                'feature_importance': dict(sorted_features),
                'top_features': dict(sorted_features[:5])
            }
            
        except Exception as e:
            logger.error(f"Error calculating feature importance: {str(e)}")
            raise
            
    def _get_basic_stats(self, X):
        """Calculate basic statistics for numerical features"""
        return X.describe().to_dict()
        
    def _get_correlation_matrix(self, X):
        """Calculate correlation matrix for features"""
        return X.corr().to_dict()
        
    def _analyze_feature_distributions(self, X):
        """Analyze the distribution of each feature"""
        distributions = {}
        for column in X.columns:
            distributions[column] = {
                'mean': X[column].mean(),
                'median': X[column].median(),
                'std': X[column].std(),
                'skew': X[column].skew(),
                'kurtosis': X[column].kurtosis()
            }
        return distributions
        
    def _analyze_target_distribution(self, y):
        """Analyze the distribution of the target variable"""
        return {
            'mean': y.mean(),
            'median': y.median(),
            'std': y.std(),
            'unique_values': len(np.unique(y)),
            'value_counts': dict(y.value_counts().to_dict())
        } 