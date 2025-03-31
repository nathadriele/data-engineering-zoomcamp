variable "project_name" {
  description = "Project name"
  default     = "mental-health-de-zoomcamp"
}

variable "azurite_container_name" {
  description = "Name of the Azurite container"
  default     = "raw-data"
}

variable "duckdb_path" {
  description = "Path to the DuckDB file"
  default     = "../data/duckdb/mental_health.db"
}
