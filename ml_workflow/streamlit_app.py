import streamlit as st
import pandas as pd
from app import MLWorkflowOrchestrator
from agents.dashboard_agent import DashboardAgent
import os

# Set page config
st.set_page_config(
    page_title="ML Workflow Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize agents
@st.cache_resource
def get_agents():
    return MLWorkflowOrchestrator(), DashboardAgent()

orchestrator, dashboard_agent = get_agents()

# Title
st.title("🤖 Machine Learning Workflow Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.header("Configuration")

# File upload
uploaded_file = st.sidebar.file_uploader(
    "Upload your dataset (CSV or Excel)",
    type=['csv', 'xlsx', 'xls']
)

if uploaded_file is not None:
    # Save uploaded file temporarily
    file_path = os.path.join("temp_data", uploaded_file.name)
    os.makedirs("temp_data", exist_ok=True)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Load data preview
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        st.sidebar.success("File uploaded successfully!")
        
        # Display data preview
        st.subheader("Data Preview")
        st.dataframe(df.head())
        
        # Configuration options
        target_column = st.sidebar.selectbox(
            "Select target column",
            df.columns.tolist()
        )
        
        model_type = st.sidebar.selectbox(
            "Select model type",
            ["classification", "regression"]
        )
        
        # Run analysis button
        if st.sidebar.button("Run Analysis"):
            with st.spinner("Running ML workflow..."):
                # Run the workflow
                results = orchestrator.run_workflow(
                    data_path=file_path,
                    target_column=target_column,
                    model_type=model_type
                )
                
                # Create visualizations
                figures = dashboard_agent.create_visualizations(
                    results['analysis_results'],
                    results['feature_importance'],
                    results['model_results']
                )
                
                # Display results in tabs
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "Feature Importance",
                    "Correlation Analysis",
                    "Feature Distributions",
                    "Model Metrics",
                    "Target Distribution"
                ])
                
                with tab1:
                    st.plotly_chart(figures['feature_importance'], use_container_width=True)
                    
                with tab2:
                    st.plotly_chart(figures['correlation_heatmap'], use_container_width=True)
                    
                with tab3:
                    st.plotly_chart(figures['feature_distributions'], use_container_width=True)
                    
                with tab4:
                    st.plotly_chart(figures['metrics'], use_container_width=True)
                    # Display best parameters
                    st.subheader("Best Model Parameters")
                    st.json(results['model_results']['best_params'])
                    
                with tab5:
                    st.plotly_chart(figures['target_distribution'], use_container_width=True)
                
                # Clean up
                os.remove(file_path)
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
        if os.path.exists(file_path):
            os.remove(file_path)
            
else:
    # Instructions
    st.info("👈 Please upload your dataset using the sidebar to get started!")
    
    st.markdown("""
    ### How to use this dashboard:
    
    1. Upload your dataset (CSV or Excel file)
    2. Select the target column for prediction
    3. Choose the model type (classification or regression)
    4. Click 'Run Analysis' to start the ML workflow
    
    ### Features:
    
    - **Automated Data Preprocessing**: Handles missing values, encoding, and scaling
    - **Exploratory Data Analysis**: Visualizes data distributions and correlations
    - **Feature Importance**: Identifies most influential features
    - **Model Performance**: Displays key metrics and best parameters
    - **Interactive Visualizations**: Explore results through interactive plots
    
    ### Supported File Formats:
    - CSV (.csv)
    - Excel (.xlsx, .xls)
    """) 