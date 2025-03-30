# Data Engineering Project

## Mental Health

![image](https://github.com/user-attachments/assets/5f07e75c-6065-41dc-beb2-17236d74ed97)

This project demonstrates an end-to-end data pipeline built using modern tools and best practices in data engineering. The pipeline extracts, transforms, loads, and visualizes data from a global mental health survey, applying concepts learned in the Data Engineering Zoomcamp.
 
---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Project Objectives](#project-objectives)
- [How to Clone This Project](how-to-clone-this-project)
- [About the Dataset](#about-the-dataset)
- [Pipeline Architecture](#pipeline-architecture)
- [Technologies and Tools Used](#technologies-and-tools-used)
- [Languages Used](languages-used)
- [Project Structure Basic](#project-structure-basic)
- [Setup and Execution Guide](#setup-and-execution-guide)
  - [1. Environment Setup](#1-environment-setup)
  - [2. Infrastructure Provisioning (Terraform)](#2-infrastructure-provisioning-terraform)
  - [3. Data Ingestion Pipeline (Mage)](#3-data-ingestion-pipeline-mage)
  - [4. Data Transformation (DBT)](#4-data-transformation-dbt)
  - [5. Interactive Dashboard (Streamlit)](#5-interactive-dashboard-streamlit)
- [Final Considerations](#final-considerations)
- [References](#references)

---

## Overview

This project focuses on building a robust and modular end-to-end data pipeline that ingests, transforms, and visualizes mental health survey data. The approach supports batch processing and integrates multiple technologies to ensure scalability, reproducibility, and ease of maintenance.

---

## Problem Statement

Mental health is a critical global issue. This project utilizes a dataset that records a global survey on mental health, covering aspects such as stress levels, depression, anxiety, subjective well-being, and the use of mental health services. Analyzing this data helps identify relevant trends and patterns, supporting a better understanding of changes in mental health across different demographics and over time.

---

## Project Objectives

- **Data Extraction and Ingestion:**  
  Select a mental health dataset and ingest the data into a local data lake using Azurite.
- **Data Storage and Loading:**  
  Move the ingested data to a local data warehouse using DuckDB.
- **Data Transformation:**  
  Use DBT to clean, transform, and prepare the data for analysis.
- **Visualization:**  
  Build an interactive dashboard using Streamlit that includes at least two tiles:  
  - A chart showing the distribution of categorical data (e.g., by country or gender).  
  - A chart illustrating the evolution of data over time or another temporal dimension.
- **Workflow Orchestration and Automation:**  
  Organize the complete flow using modern tools, ensuring a scalable and maintainable solution.

---

## How to Clone This Project

To get started with this project locally, follow the steps below:

### 1. Clone the repository

```bash
git clone https://github.com/nathadriele/data-engineering-zoomcamp.git
```

2. Navigate to the project folder

```bash
cd data-engineering-zoomcamp/project-2025
```

3. Explore the structure

You can now explore the complete mental_health_project pipeline, including the infrastructure setup, data pipeline, DBT transformations, and interactive dashboard.


---

## About the Dataset

![image](https://github.com/user-attachments/assets/ca85464a-9278-4a59-a141-47626642668e)

The dataset used in this project is obtained from [Kaggle](https://www.kaggle.com/datasets/divaniazzahra/mental-health-dataset) and contains the results of a global mental health survey.

**Dataset Details:**

- **Context:** A global survey conducted to track trends in mental health.
- **Variables Included:**
  - `Timestamp`: Date and time of the record.
  - `Gender`: Respondent's gender.
  - `Country`: Country of origin.
  - `Occupation`: Professional occupation.
  - `Self_employed`: Indicator whether the respondent is self-employed.
  - `Family_history`: Family history of mental health issues.
  - `Treatment`: Indicator if the respondent is seeking treatment.
  - `Days_Indoors`: Number of days the respondent stayed indoors.
  - `Growing_Stress`: Indicator of increasing stress.
  - `Changes_Habits`: Changes in respondent's habits.
  - `Mental_Health_History`: History of mental health issues.
  - `Mood_Swings`: Mood swings.
  - `Coping_Struggles`: Difficulty coping with situations.
  - `Work_Interest`: Interest in work.
  - `Social_Weakness`: Weakness in social interactions.
  - `Mental_Health_Interview`: Attitude during mental health interviews.
  - `Care_options`: Awareness of available care options.
- **Goal:** Provide insights into global changes in mental health over the survey period.

---

## Pipeline Architecture

The pipeline consists of five main stages:

1. **Infrastructure:**  
   Provision a local environment using Terraform to configure Azurite (Azure Storage emulator) and DuckDB (data warehouse).

2. **Data Ingestion:**  
   A pipeline created with Mage extracts data from the dataset and uploads it to the data lake (Azurite).

3. **Data Loading:**  
   Transfer data from Azurite to the data warehouse (DuckDB).

4. **Data Transformation:**  
   Use DBT to transform and validate the data, preparing it for visualization.

5. **Visualization:**  
   Build an interactive dashboard using Streamlit to display data insights with dynamic charts.

---

## Technologies and Tools Used

![image](https://github.com/user-attachments/assets/7f75cae4-c9a3-4cdf-9e95-564d43ab0fe9)

In this project, a suite of modern and specialized tools was integrated to build a robust end-to-end data pipeline. Each tool plays a critical role in the process of extracting, transforming, loading, and visualizing data. Below is a detailed description of each tool and its purpose within the project:

### Terraform
   - Description: A powerful Infrastructure as Code (IaC) tool that enables the declarative creation, modification, and versioning of infrastructure.
   - Role in the Project: Used to provision and configure the local environment, including the Azure Storage emulator (Azurite) and other infrastructure dependencies. This ensures that the environment is reproducible, scalable, and version-controlled.

### Docker
   - Description: A platform for developing, shipping, and running applications in isolated containers. It provides a lightweight and consistent runtime environment across systems.
   - Role in the Project: Used to run Azurite locally in a containerized environment. This allows the simulation of Azure Blob Storage services without needing access to the cloud, enabling consistent and reproducible development and testing.

### Mage
   - Description: A modern platform for designing and orchestrating data pipelines, making it easier to construct and execute data ingestion flows.
   - Role in the Project: Manages the data ingestion pipeline by extracting data from the source dataset and uploading it to the data lake (Azurite). It ensures smooth and automated data flow from extraction to storage.

### Azurite
   - Description: A local emulator for Azure Storage that simulates the behavior of Azure’s storage services without requiring a cloud environment.
   - Role in the Project: Serves as the local data lake where raw data is initially stored after ingestion. This setup allows for testing and development in a cost-effective and controlled environment.

### DuckDB
   - Description: A high-performance, columnar-oriented relational database optimized for analytical queries. It is designed for efficient local data processing and analysis.
   - Role in the Project: Acts as the data warehouse by storing and enabling efficient querying of the ingested data from Azurite. This facilitates further transformation and analysis steps.

### DBT (Data Build Tool)
   - Description: A transformation tool that enables data modeling, testing, and documentation using SQL. It enforces best practices in data transformation and quality assurance.
   - Role in the Project: Responsible for transforming and modeling the data stored in DuckDB. DBT applies rigorous testing and validation, ensuring that the data is clean and ready for analysis before it is visualized.

### Streamlit
   - Description: An open-source Python framework that simplifies the creation of interactive web applications, particularly dashboards and data visualizations.
   - Role in the Project: Used to build an interactive dashboard that dynamically displays insights from the mental health data. Streamlit offers a user-friendly interface for exploring and interacting with the visualized data.

### Plotly
   - Description: A versatile data visualization library in Python that provides interactive, high-quality charts and graphs.
   - Role in the Project: Integrated with Streamlit to generate dynamic and interactive visualizations. Plotly enhances the dashboard by enabling detailed exploration of data trends and distributions.

---

## Languages Used

| Language       | Purpose                                                                                     |
|----------------|---------------------------------------------------------------------------------------------|
| **Python**     | Development of data ingestion pipelines (Mage), helper scripts, and interactive dashboards using Streamlit and Plotly. |
| **SQL**        | Data transformation and modeling using DBT and analytical queries in DuckDB.               |
| **HCL**        | Infrastructure provisioning using Terraform (Infrastructure as Code).                      |
| **YAML**       | Configuration files for Mage pipelines, DBT models, and environment settings.              |
| **PowerShell** | Automation scripts for Windows environment setup and running local services like Azurite.  |
| **Markdown**   | Project documentation, including this README and additional reference files.               |

---

## Project Structure Basic

```powershell
mental_health_project/
│
├── infrastructure/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── azurite_setup.ps1
│   └── azurite-data/
│
├── data_pipeline/
│   ├── mental-health-project/
│   │   ├── ingestion_pipeline.py
│   │   ├── io_config.yaml
│   │   └── blocks/
│   ├── scripts/
│   │   ├── ingest_data.py
│   │   └── load_to_warehouse.py
│   └── mental_health.duckdb
│
├── dbt_project/
│   └── mental_health_transform/
│       ├── models/
│       │   ├── staging/
│       │   │   └── stg_mental_health.sql
│       │   ├── marts/
│       │   │   └── mental_health_clean.sql
│       │   └── schema.yml
│       ├── snapshots/
│       ├── seeds/
│       ├── dbt_project.yml
│       └── profiles.yml
│
├── visualization/
│   ├── dashboard.py
│   ├── charts/
│   │   ├── distribution_plot.py
│   │   └── temporal_plot.py
│   ├── pages/
│   │   └── about.py
│   └── utils/
│       └── data_loader.py
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_transformation.sql
│   └── test_visualization.py
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
├── requirements.txt
├── pyproject.toml
├── Makefile
├── run_project.ps1
└── README.md
```

---

## Setup and Execution Guide

### 1. Environment Setup

**Prerequisites:**
- Windows 10/11
- Python 3.8+
- Docker Desktop (to run Azurite)
- Azure account (optional for cloud environments)

**Tool Installation:**

Use the script below to install Chocolatey and the required tools:

```powershell
# setup_environment.ps1

# Install Chocolatey (if not already installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; `
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install required tools
choco install -y python terraform docker-desktop git

# Create and activate Python virtual environment0
python -m venv .venv
.\.venv\Scripts\activate

# Install Python packages
pip install mage-ai duckdb dbt-core streamlit pandas pyarrow azure-storage-blob plotly
```

## 2. Infrastructure Provisioning (Terraform) 

1. Navigate to the infrastructure folder:

```powershell
cd infrastructure
```

2. Run the following commands:

```powershell
terraform init
terraform apply -auto-approve
.\azurite_setup.ps1
```

The azurite_setup.ps1 script will start Azurite via Docker, setting up the local data lake.

### 3. Data Ingestion Pipeline (Mage)

1. In the data_pipeline folder, start the Mage project:

```powershell
cd data_pipeline
mage start mental-health
```

2. Inside the mental-health folder, create the ingestion_pipeline.py file (refer to internal documentation for code details).

3. Open your browser and access http://localhost:6789 to monitor the pipeline execution.

### 4. Data Transformation (DBT)

1. Navigate to the DBT project directory:

```powershell
cd dbt_project/mental_health_transform
```

2. Initialize and configure the DBT project:

```powershell
dbt init mental_health_transform
```

3. Create and edit the following files:

- models/schema.yml: Defines the schema and tests.

- models/mental_health_clean.sql: Contains the SQL model for data transformation.

- profiles.yml: Configure the connection to DuckDB using the relative path ../data_pipeline/mental_health.duckdb.

4. Run the transformations and tests:

```powershell
dbt run
dbt test
```

## 5. Interactive Dashboard (Streamlit)

1. Navigate to the visualization folder:

```powershell
cd visualization
```

2. Launch the dashboard:

```powershell
streamlit run dashboard.py
```

The dashboard will display at least two charts:

- A chart showing the distribution of categorical data (e.g., by country, gender).
- A chart depicting the evolution of records over time or another relevant dimension.

## Final Considerations

This project demonstrates a complete Data Engineering solution, covering data ingestion into a data lake, transformation in a data warehouse, and interactive visualization via a dashboard. Its modular design and use of modern tools (Terraform, Mage, DBT, and Streamlit) ensure scalability and adaptability across different environments (local or cloud). Detailed documentation and step-by-step instructions make the project reproducible and easy to maintain.

## References

- [Data Engineering Zoomcamp - Course Projects](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/projects#datasets)
- [Kaggle - Mental Health Dataset](https://www.kaggle.com/datasets/divaniazzahra/mental-health-dataset)
- [Terraform Documentation](https://www.terraform.io/docs)
- [Mage Documentation](https://docs.mage.ai)
- [DBT Documentation](https://docs.getdbt.com)
- [Azure/Azurite](https://github.com/Azure/Azurite)
- [Streamlit Documentation](https://docs.streamlit.io)
