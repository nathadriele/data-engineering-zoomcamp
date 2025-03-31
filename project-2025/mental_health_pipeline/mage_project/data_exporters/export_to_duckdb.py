import pandas as pd
import duckdb
from mage_ai.data_preparation.repo_manager import get_repo_path
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_duckdb(df: pd.DataFrame, **kwargs) -> None:
    """
    Exporta os dados para o DuckDB para posterior transformação com DBT
    """
    # Caminho para o arquivo DuckDB
    db_path = path.join(get_repo_path(), '..', 'data', 'duckdb', 'mental_health.db')
    
    # Conectar ao DuckDB
    con = duckdb.connect(db_path)
    
    # Criar tabela raw se não existir
    con.execute("""
    CREATE TABLE IF NOT EXISTS raw_mental_health (
        Timestamp TIMESTAMP,
        Gender VARCHAR,
        Country VARCHAR,
        Occupation VARCHAR,
        self_employed VARCHAR,
        family_history VARCHAR,
        treatment VARCHAR,
        Days_Indoors VARCHAR,
        Growing_Stress VARCHAR,
        Changes_Habits VARCHAR,
        Mental_Health_History VARCHAR,
        Mood_Swings VARCHAR,
        Coping_Struggles VARCHAR,
        Work_Interest VARCHAR,
        Social_Weakness VARCHAR,
        mental_health_interview VARCHAR,
        care_options VARCHAR
    )
    """)
    
    # Limpar dados anteriores
    con.execute("DELETE FROM raw_mental_health")
    
    # Inserir dados
    con.register('temp_df', df)
    con.execute("INSERT INTO raw_mental_health SELECT * FROM temp_df")
    
    # Verificar registros
    count = con.execute("SELECT COUNT(*) FROM raw_mental_health").fetchone()[0]
    
    # Fechar conexão
    con.close()
    
    print(f"Dados exportados para DuckDB: {count} registros na tabela raw_mental_health")