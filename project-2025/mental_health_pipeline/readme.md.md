# 🧬 Data Pipeline for Mental Health Analysis

This project implements a complete data engineering pipeline to analyze mental health patterns using modern technologies.

---

## Technologies Used

- **IaC**: Terraform  
- **Environment**: Local Windows  
- **Workflow Orchestration**: Mage  
- **Data Lake**: Azurite  
- **Data Warehouse**: DuckDB  
- **Data Transformation**: DBT  
- **Visualization**: Streamlit  

---

## Prerequisites

Make sure you have the following installed:

- Python 3.8+
- Docker
- Terraform
- Git

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/nathadriele/data-engineering-zoomcamp/tree/main/project-2025
cd mental_health_pipeline
```

## 2. Create a Python virtual environment

```bash
python -m venv venv
.\.venv\Scripts\activate
```

## 3. Install required dependencies

```bash
pip install -r requirements.txt
```

## 4. Initialize infrastructure with Terraform

```bash
cd terraform
terraform init
terraform apply -auto-approve
cd ..
```

#### This will:

- Start Azurite (via Docker) as the Data Lake
- Create necessary project folders
- Download the example dataset
- Install and configure Mage, DBT, and Streamlit

## Configure and Run the Pipeline

```bash
cd mage_project
mage start
```

#### Open the Mage web UI (usually at http://localhost:6789) and:

1. Click "New pipeline" → Select "Data Pipeline"
2. Name it: mental_health_pipeline
3. Import the following files:
   - `load_mental_health_data.py`
   - `export_to_azurite.py`
   - `export_to_duckdb.py`
   - `mental_health_pipeline.py`
4. Run the full pipeline

## 6. Run DBT transformations

```bash
cd ../dbt_project
dbt deps
dbt run
dbt test
```

This will:

- Transform raw data in DuckDB
- Create dimension and fact tables
- Run quality tests

## 7. Launch the Streamlit Dashboard

```bash
cd ../streamlit
streamlit run app.py
```

#### Access the dashboard at: http://localhost:8501

## Pipeline Overview

1. Extraction: Load raw mental health data  
2. Data Lake: Store in Azurite  
3. Data Warehouse: Load into DuckDB  
4. Transformation: DBT normalization and enrichment  
5. Visualization: Interactive dashboard using Streamlit  

## Dataset Details

The dataset includes:

- Demographics (gender, country, occupation)
- Family and mental health history
- Stress and well-being indicators
- Treatment information and care options

## Customization

To use your own dataset:

- Replace data/mental_health_dataset.csv
- Adjust DBT transformation scripts
- Customize the Streamlit dashboard as needed

## Troubleshooting

### Azurite not working?

Check if Docker is running and the Azurite container is active:

```bash
docker ps | grep azurite
```

### To restart Azurite:

```bash
docker restart azurite
```

## Mage errors?

#### Check logs in:

```bash
mage_project/logs/
```

## DBT issues?

#### Run:

```bash
dbt debug
```

🤝 Contributions

Contributions are welcome!

📌 Project created as part of the Data Engineering Zoomcamp (2025 Edition)
