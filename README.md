# Multi-Agent Code Generation and ML Workflow System

## Overview

This project is a multi-agent system for automated code generation, deployment, and machine learning workflow orchestration. It leverages large language models (LLMs) and specialized agents to transform high-level user prompts into fully functional applications and ML dashboards, with minimal manual intervention.

## Features
- **Multi-Agent Pipeline:** Requirements analysis, design specification, code generation, and deployment, each handled by a dedicated agent.
- **Automated Deployment:** Generated code is saved and optionally launched as a web application.
- **Combined Agent Reports:** Outputs from all agents are compiled into a downloadable Word document.
- **ML Workflow Dashboard:** Upload datasets, run automated ML pipelines, and visualize results interactively using Streamlit.
- **Flexible Model Selection:** Choose from multiple LLMs for each agent.

## Architecture

```
User Prompt → Requirements Agent → Design Agent → Coder Agent → Deployment Agent
                                            ↓
                                 [ML Workflow (optional)]
```

- **Agents:**
  - `requirements_agent.py`: Extracts functional and non-functional requirements from user prompts, using LLMs and web search context.
  - `design_agent.py`: Produces a detailed design specification (components, architecture, file structure) from requirements.
  - `coder_agent.py`: Generates all necessary code files (HTML, CSS, JS, Python, etc.) from the design specification.
  - `deploy_agent.py` / `deployment_agent.py`: Parses generated code, saves files, installs dependencies, and launches the application.

- **ML Workflow (ml_workflow/):**
  - `data_agent.py`: Loads and preprocesses data (missing values, encoding, scaling, splitting).
  - `analysis_agent.py`: Performs exploratory data analysis and feature importance.
  - `model_agent.py`: Trains and evaluates ML models with hyperparameter tuning.
  - `dashboard_agent.py`: Creates interactive visualizations using Plotly.
  - `streamlit_app.py`: User interface for uploading data and running the ML workflow.

## Directory Structure

```
multiagentapp/
├── agents/
│   ├── coder_agent.py
│   ├── deploy_agent.py
│   ├── design_agent.py
│   └── requirements_agent.py
├── app.py                # Main Streamlit app for code generation pipeline
├── deployed_app/         # Output directory for generated apps
│   ├── index.html
│   ├── styles/
│   ├── scripts/
│   └── ...
├── deployment_agent.py   # Utility for parsing, saving, and launching code
├── model_api.py          # LLM API utility
├── requirements.txt      # Core dependencies
├── ml_workflow/
│   ├── agents/
│   ├── app.py
│   ├── requirements.txt
│   └── streamlit_app.py
└── README.md
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd multiagentapp
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # For ML workflow:
   pip install -r ml_workflow/requirements.txt
   ```
3. **Set up environment variables:**
   - Create a `.env` file with your LLM API keys (e.g., `GROQ_API_KEY`).

## Usage

### Code Generation & Deployment
1. Run the main Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Enter a high-level prompt (e.g., "Build me a website for guitars").
3. Select models for each agent and click **Generate**.
4. Download the generated code or combined agent report.
5. If the app is launched, access it at the provided local URL.

### ML Workflow Dashboard
1. Run the ML dashboard:
   ```bash
   cd ml_workflow
   streamlit run streamlit_app.py
   ```
2. Upload your dataset (CSV/Excel), select the target column and model type, and run the analysis.
3. Explore feature importance, correlations, model metrics, and more via interactive tabs.

## Agent Descriptions

- **Requirements Agent:**
  - Extracts detailed requirements from user prompts, using LLMs and web search (Tavily).
  - Outputs functional and non-functional requirements, plus referenced sources.
- **Design Agent:**
  - Converts requirements into a structured design (components, file structure, data flow).
- **Coder Agent:**
  - Generates all code files needed for the application, formatted in code blocks with filenames.
- **Deployment Agent:**
  - Parses code output, saves files to `deployed_app/`, installs dependencies, and launches the app (supports static HTML, Flask, Node.js, Streamlit).

## ML Workflow Details
- **DataAgent:** Loads and preprocesses data (missing values, encoding, scaling, splitting).
- **AnalysisAgent:** Performs EDA, computes feature importance, and analyzes distributions.
- **ModelAgent:** Trains and evaluates models (classification/regression) with hyperparameter tuning.
- **DashboardAgent:** Generates interactive visualizations (feature importance, correlations, metrics, etc.).

## Example Output Structure

After running the pipeline, the generated app will be saved in `deployed_app/`:

```
deployed_app/
├── index.html
├── styles/
│   └── styles.css
├── scripts/
│   └── scripts.js
└── ...
```

## Dependencies

- **Core:**
  - streamlit
  - groq
  - python-dotenv
  - python-docx
- **ML Workflow:**
  - numpy
  - pandas
  - scikit-learn
  - matplotlib
  - seaborn
  - openpyxl
  - plotly

## License

MIT License (or specify your license here)

## Acknowledgments
- Powered by LLMs (Groq, OpenAI, etc.)
- Uses Tavily for web search context
- Built with Streamlit, scikit-learn, and Plotly
