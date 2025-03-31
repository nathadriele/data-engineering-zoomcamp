#!/bin/bash

# Welcome message
echo "==================================================="
echo "     Mental Health Data Pipeline Setup"
echo "==================================================="
echo

# Create virtual environment
echo "Creating Python virtual environment..."
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate     # Linux/Mac

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create project directories
echo "Setting up project structure..."
mkdir -p data/duckdb
mkdir -p mage_project/data_loaders
mkdir -p mage_project/data_exporters
mkdir -p mage_project/pipelines
mkdir -p dbt_project/models/staging
mkdir -p dbt_project/models/marts
mkdir -p streamlit

# Initialize infrastructure with Terraform
echo "Initializing infrastructure with Terraform..."
cd terraform
terraform init
terraform apply -auto-approve
cd ..

echo
echo "==================================================="
echo "Initial setup complete!"
echo
echo "Next steps:"
echo "1. Configure Mage: cd mage_project && mage start"
echo "2. Run DBT transformations: cd dbt_project && dbt run"
echo "3. Start the dashboard: cd streamlit && streamlit run app.py"
echo "==================================================="
