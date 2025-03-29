# Data Engineering Project - Mental Health

![image](https://github.com/user-attachments/assets/5f07e75c-6065-41dc-beb2-17236d74ed97)

This project demonstrates an end-to-end data pipeline built using modern tools and best practices in data engineering. The pipeline extracts, transforms, loads, and visualizes data from a global mental health survey, applying concepts learned in the Data Engineering Zoomcamp.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Project Objectives](#project-objectives)
- [About the Dataset](#about-the-dataset)
- [Pipeline Architecture](#pipeline-architecture)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup and Execution Guide](#setup-and-execution-guide)
  - [1. Environment Setup](#1-environment-setup)
  - [2. Infrastructure Provisioning (Terraform)](#2-infrastructure-provisioning-terraform)
  - [3. Data Ingestion Pipeline (Mage)](#3-data-ingestion-pipeline-mage)
  - [4. Data Transformation (DBT)](#4-data-transformation-dbt)
  - [5. Interactive Dashboard (Streamlit)](#5-interactive-dashboard-streamlit)
- [Potential Improvements and Extensions](#potential-improvements-and-extensions)
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

## About the Dataset

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

## Technologies Used

- **Infrastructure as Code (IaC):**  
  - **Terraform:** For provisioning the local environment and configuring Azurite.

- **Workflow Orchestration & Data Ingestion:**  
  - **Mage:** To create and orchestrate the data ingestion pipeline.

- **Data Lake and Data Warehouse:**  
  - **Azurite:** Local emulator for Azure Storage acting as the data lake.
  - **DuckDB:** Local data warehouse for data storage and querying.

- **Data Transformation:**  
  - **DBT (Data Build Tool):** For transforming, modeling, and testing the data.

- **Visualization:**  
  - **Streamlit:** For developing the interactive dashboard.
  - **Plotly:** For creating dynamic and interactive charts.

- **Languages and Tools:**  
  - Python, SQL, HCL, YAML

---

## Project Structure

The recommended project directory structure is as follows:

```powershell
mental_health_project/
│
├── infrastructure/
│   ├── main.tf                 # Main Terraform configuration file
│   ├── azurite_setup.ps1       # Script to start Azurite via Docker
│   └── azurite-data/           # Persistent data directory for Azurite (created automatically)
│
├── data_pipeline/
│   ├── my_data_project/        # Mage project (created automatically)
│   │   └── ingestion_pipeline.py  # Data ingestion and loading pipeline
│   └── mental_health.duckdb    # DuckDB data warehouse (generated at runtime)
│
├── dbt_project/
│   └── mental_health_transform/  # DBT project
│       ├── models/
│       │   ├── schema.yml        # Schema definition and tests
│       │   └── mental_health_clean.sql  # Data transformation model
│       ├── dbt_project.yml       # DBT project configuration
│       └── profiles.yml          # DBT connection configuration to DuckDB
│
└── visualization/
    └── dashboard.py             # Interactive dashboard code
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
