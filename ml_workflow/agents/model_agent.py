import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, r2_score, mean_absolute_error
)
from sklearn.model_selection import GridSearchCV
import logging

logger = logging.getLogger(__name__)

class ModelAgent:
    def __init__(self):
        self.model = None
        self.model_type = None
        
    def train_and_evaluate(self, data_dict, target_column, model_type='classification'):
        """
        Train and evaluate the machine learning model
        
        Args:
            data_dict (dict): Dictionary containing preprocessed data
            target_column (str): Name of the target column
            model_type (str): Type of ML problem ('classification' or 'regression')
            
        Returns:
            dict: Model evaluation results
        """
        try:
            X_train = data_dict['X_train']
            X_test = data_dict['X_test']
            y_train = data_dict['y_train']
            y_test = data_dict['y_test']
            
            self.model_type = model_type
            
            # Train model with hyperparameter tuning
            self.model = self._train_model_with_tuning(X_train, y_train)
            
            # Make predictions
            y_pred = self.model.predict(X_test)
            
            # Calculate metrics
            metrics = self._calculate_metrics(y_test, y_pred)
            
            return {
                'metrics': metrics,
                'best_params': self.model.best_params_,
                'feature_importance': self._get_feature_importance(data_dict['feature_names'])
            }
            
        except Exception as e:
            logger.error(f"Error in model training and evaluation: {str(e)}")
            raise
            
    def _train_model_with_tuning(self, X_train, y_train):
        """Train model with hyperparameter tuning using GridSearchCV"""
        if self.model_type == 'classification':
            base_model = RandomForestClassifier(random_state=42)
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5],
                'min_samples_leaf': [1, 2]
            }
        else:
            base_model = RandomForestRegressor(random_state=42)
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5],
                'min_samples_leaf': [1, 2]
            }
            
        grid_search = GridSearchCV(
            base_model,
            param_grid,
            cv=5,
            scoring='accuracy' if self.model_type == 'classification' else 'r2',
            n_jobs=-1
        )
        
        grid_search.fit(X_train, y_train)
        return grid_search
        
    def _calculate_metrics(self, y_true, y_pred):
        """Calculate evaluation metrics based on model type"""
        if self.model_type == 'classification':
            return {
                'accuracy': accuracy_score(y_true, y_pred),
                'precision': precision_score(y_true, y_pred, average='weighted'),
                'recall': recall_score(y_true, y_pred, average='weighted'),
                'f1': f1_score(y_true, y_pred, average='weighted')
            }
        else:
            return {
                'mse': mean_squared_error(y_true, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
                'mae': mean_absolute_error(y_true, y_pred),
                'r2': r2_score(y_true, y_pred)
            }
            
    def _get_feature_importance(self, feature_names):
        """Get feature importance from the trained model"""
        importance_scores = self.model.best_estimator_.feature_importances_
        feature_importance = dict(zip(feature_names, importance_scores))
        
        # Sort features by importance
        sorted_features = sorted(
            feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return dict(sorted_features) 