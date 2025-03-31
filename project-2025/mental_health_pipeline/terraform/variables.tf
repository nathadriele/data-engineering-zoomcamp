variable "project_name" {
  description = "Nome do projeto"
  default     = "mental-health-de-zoomcamp"
}

variable "azurite_container_name" {
  description = "Nome do container para o Azurite"
  default     = "raw-data"
}

variable "duckdb_path" {
  description = "Caminho para o arquivo DuckDB"
  default     = "../data/duckdb/mental_health.db"
}