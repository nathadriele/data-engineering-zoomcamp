terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
  skip_provider_registration = true
}

# Run Azurite locally for local storage emulation
resource "null_resource" "azurite_container" {
  provisioner "local-exec" {
    command = <<EOT
      docker run -d --name azurite -p 10000:10000 -p 10001:10001 -p 10002:10002 mcr.microsoft.com/azure-storage/azurite
    EOT
  }
}

# Create directory for DuckDB storage
resource "null_resource" "create_duckdb_dir" {
  provisioner "local-exec" {
    command = "mkdir -p ${path.module}/../data/duckdb"
  }
}

# Download example dataset
resource "null_resource" "download_dataset" {
  provisioner "local-exec" {
    command = <<EOT
      echo "Timestamp,Gender,Country,Occupation,self_employed,family_history,treatment,Days_Indoors,Growing_Stress,Changes_Habits,Mental_Health_History,Mood_Swings,Coping_Struggles,Work_Interest,Social_Weakness,mental_health_interview,care_options
2014-08-27 11:29:31,Female,United States,Corporate,,No,Yes,1-14 days,Yes,No,Yes,Medium,No,No,Yes,No,Not sure
2014-08-27 11:31:50,Female,United States,Corporate,,Yes,Yes,1-14 days,Yes,No,Yes,Medium,No,No,Yes,No,No
2014-08-27 11:32:39,Female,United States,Corporate,,Yes,Yes,1-14 days,Yes,No,Yes,Medium,No,No,Yes,No,Yes
2014-08-27 11:37:59,Female,United States,Corporate,No,Yes,Yes,1-14 days,Yes,No,Yes,Medium,No,No,Yes,Maybe,Yes
2014-08-27 11:43:36,Female,United States,Corporate,No,Yes,Yes,1-14 days,Yes,No,Yes,Medium,No,No,Yes,No,Yes
2014-08-27 11:49:51,Female,Poland,Corporate,No,No,Yes,1-14 days,Yes,No,Yes,Medium,No,No,Yes,Maybe,Not sure" > ${path.module}/../data/mental_health_dataset.csv
    EOT
  }
}

# Install and configure Mage
resource "null_resource" "setup_mage" {
  depends_on = [null_resource.azurite_container, null_resource.create_duckdb_dir]
  
  provisioner "local-exec" {
    command = <<EOT
      pip install mage-ai
      mkdir -p ${path.module}/../mage_project
      cd ${path.module}/.. && mage start mage_project
    EOT
  }
}

# Install DBT for DuckDB
resource "null_resource" "setup_dbt" {
  provisioner "local-exec" {
    command = <<EOT
      pip install dbt-core dbt-duckdb
      mkdir -p ${path.module}/../dbt_project
      cd ${path.module}/../dbt_project && dbt init .
    EOT
  }
}

# Install Streamlit and supporting libraries
resource "null_resource" "setup_streamlit" {
  provisioner "local-exec" {
    command = "pip install streamlit pandas matplotlib seaborn plotly"
  }
}

output "setup_complete" {
  value = "Infrastructure successfully configured. Azurite is running on localhost:10000-10002, Mage is installed, DuckDB is configured, and DBT and Streamlit are installed."
}
