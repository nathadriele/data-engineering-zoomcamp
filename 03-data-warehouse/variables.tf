variable "credentials" {
  description = "My Credentials"
  default     = "./secrets/zoomcamp-week-3-9cfd78e84128.json"
}

variable "project" {
  description = "Project"
  default     = "zoomcamp-week-3"

}

variable "region" {
  description = "Region"
  default     = "us-central1"

}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "zoomcamp_week_3_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "zoomcamp-week-3-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}