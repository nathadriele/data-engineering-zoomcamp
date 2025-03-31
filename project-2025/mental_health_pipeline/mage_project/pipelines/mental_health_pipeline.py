from mage_ai.data_preparation.repo_manager import get_repo_path
from mage_ai.data_preparation.decorators import pipeline
from mage_ai.data_preparation.pipeline_manager import PipelineManager

@pipeline
def mental_health_data_pipeline():
    """
    Pipeline completa para processar os dados de saúde mental
    """
    # Carregar dados
    data = PipelineManager().load_module('data_loaders', 'load_mental_health_data').load_data_from_file()
    
    # Exportar para Azurite
    PipelineManager().load_module('data_exporters', 'export_to_azurite').export_data_to_azurite(data)
    
    # Exportar para DuckDB
    PipelineManager().load_module('data_exporters', 'export_to_duckdb').export_data_to_duckdb(data)
    
    return "Pipeline executada com sucesso"