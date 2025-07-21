from agents.data_agent import DataAgent
from agents.analysis_agent import AnalysisAgent
from agents.model_agent import ModelAgent
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLWorkflowOrchestrator:
    def __init__(self):
        self.data_agent = DataAgent()
        self.analysis_agent = AnalysisAgent()
        self.model_agent = ModelAgent()
        
    def run_workflow(self, data_path, target_column, model_type='classification'):
        """
        Orchestrate the complete ML workflow
        
        Args:
            data_path (str): Path to the data file (CSV/Excel)
            target_column (str): Name of the target column
            model_type (str): Type of ML problem ('classification' or 'regression')
        """
        try:
            # Step 1: Data Loading and Preprocessing
            logger.info("Starting data loading and preprocessing...")
            df = self.data_agent.load_data(data_path)
            processed_data = self.data_agent.preprocess_data(df, target_column)
            
            # Step 2: Data Analysis
            logger.info("Starting data analysis...")
            analysis_results = self.analysis_agent.analyze_data(processed_data)
            feature_importance = self.analysis_agent.get_feature_importance(processed_data, target_column)
            
            # Step 3: Model Training and Evaluation
            logger.info("Starting model training and evaluation...")
            model_results = self.model_agent.train_and_evaluate(
                processed_data,
                target_column,
                model_type=model_type
            )
            
            return {
                'analysis_results': analysis_results,
                'feature_importance': feature_importance,
                'model_results': model_results
            }
            
        except Exception as e:
            logger.error(f"Error in ML workflow: {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage
    orchestrator = MLWorkflowOrchestrator()
    results = orchestrator.run_workflow(
        data_path="data/example.csv",
        target_column="target",
        model_type="classification"
    ) 