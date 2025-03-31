import io
import pandas as pd
from azure.storage.blob import BlobServiceClient
from mage_ai.data_preparation.repo_manager import get_repo_path
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_azurite(df: pd.DataFrame, **kwargs) -> None:
    """
    Exporta os dados para o Azurite local
    """
    # Configurações do Azurite
    connect_str = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    container_name = "raw-data"
    
    # Criar cliente de serviço Blob
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    
    # Criar container se não existir
    try:
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client = blob_service_client.create_container(container_name)
    except Exception as e:
        container_client = blob_service_client.create_container(container_name)
    
    # Converter DataFrame para CSV
    csv_data = io.StringIO()
    df.to_csv(csv_data, index=False)
    csv_data.seek(0)
    csv_bytes = csv_data.getvalue().encode('utf-8')
    
    # Enviar para o Azurite
    blob_client = blob_service_client.get_blob_client(container=container_name, blob="mental_health_data.csv")
    blob_client.upload_blob(csv_bytes, overwrite=True)
    
    print(f"Dados exportados para Azurite: container={container_name}, blob=mental_health_data.csv")