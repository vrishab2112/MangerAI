import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class DashboardAgent:
    def __init__(self):
        pass
        
    def create_visualizations(self, analysis_results, feature_importance, model_results):
        """
        Create interactive visualizations for the ML workflow results
        
        Args:
            analysis_results (dict): Results from analysis agent
            feature_importance (dict): Feature importance scores
            model_results (dict): Model evaluation results
            
        Returns:
            dict: Dictionary containing plotly figures
        """
        try:
            figures = {
                'feature_importance': self._plot_feature_importance(feature_importance),
                'correlation_heatmap': self._plot_correlation_heatmap(analysis_results),
                'feature_distributions': self._plot_feature_distributions(analysis_results),
                'metrics': self._plot_metrics(model_results),
                'target_distribution': self._plot_target_distribution(analysis_results)
            }
            
            return figures
            
        except Exception as e:
            logger.error(f"Error creating visualizations: {str(e)}")
            raise
            
    def _plot_feature_importance(self, feature_importance):
        """Create feature importance plot"""
        df = pd.DataFrame(list(feature_importance['feature_importance'].items()),
                         columns=['Feature', 'Importance'])
        fig = px.bar(df, x='Importance', y='Feature', orientation='h',
                    title='Feature Importance',
                    labels={'Importance': 'Importance Score', 'Feature': 'Feature Name'})
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        return fig
        
    def _plot_correlation_heatmap(self, analysis_results):
        """Create correlation heatmap"""
        corr_matrix = pd.DataFrame(analysis_results['correlation_matrix'])
        fig = px.imshow(corr_matrix,
                       title='Feature Correlation Matrix',
                       labels=dict(color="Correlation"),
                       color_continuous_scale='RdBu')
        return fig
        
    def _plot_feature_distributions(self, analysis_results):
        """Create feature distribution plots"""
        distributions = analysis_results['feature_distributions']
        df = pd.DataFrame(distributions).T
        
        fig = go.Figure()
        for col in df.columns:
            if col not in ['skew', 'kurtosis']:
                fig.add_trace(go.Box(y=df[col], name=col))
                
        fig.update_layout(title='Feature Distributions',
                         yaxis_title='Value',
                         showlegend=False)
        return fig
        
    def _plot_metrics(self, model_results):
        """Create model metrics visualization"""
        metrics = model_results['metrics']
        df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
        
        fig = px.bar(df, x='Metric', y='Value',
                    title='Model Performance Metrics',
                    labels={'Value': 'Score', 'Metric': 'Metric Name'})
        return fig
        
    def _plot_target_distribution(self, analysis_results):
        """Create target distribution plot"""
        target_dist = analysis_results['target_distribution']['value_counts']
        df = pd.DataFrame(list(target_dist.items()), columns=['Class', 'Count'])
        
        fig = px.pie(df, values='Count', names='Class',
                    title='Target Distribution',
                    hole=0.3)
        return fig 