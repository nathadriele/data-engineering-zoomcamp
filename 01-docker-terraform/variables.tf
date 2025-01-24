variable "credentials" {
  description = "Service Account Credentials"
  default     = "./keys/service-account.json"
}

variable "project_id" {
  description = "Project ID"
  type        = string
  default     = "copper-diorama-448706-a3"
}

variable "region" {
  description = "Project Region"
  type        = string
  default     = "us-central1"
}

variable "locaiton" {
  description = "Project Location"
  type        = string
  default     = "US"
}

variable "bq_dataset_name" {
  description = "BigQuery dataset name"
  type        = string
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "Bucket Name"
  type        = string
  default     = "copper-diorama-448706-a3_terraform_demo_bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  type        = string
  default     = "STANDARD"
}