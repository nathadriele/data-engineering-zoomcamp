import io
import pandas as pd
from mage_ai.data_preparation.repo_manager import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.file import FileIO
from os import path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_file(*args, **kwargs):
    """
    Carrega dados do arquivo CSV de saúde mental.
    """
    filepath = path.join(get_repo_path(), '..', 'data', 'mental_health_dataset.csv')
    
    # Carregar o dataset
    df = pd.read_csv(filepath)
    
    # Converter timestamp para datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Preencher valores vazios
    df['self_employed'] = df['self_employed'].fillna('Unknown')
    
    # Garantir que colunas de texto estejam em minúsculas para padronização
    for col in df.select_dtypes(include=['object']).columns:
        if col != 'Timestamp':
            df[col] = df[col].str.lower() if not df[col].isna().all() else df[col]
    
    print(f"Dados carregados: {len(df)} registros")
    return df


@test
def test_output(df) -> None:
    """
    Testa se o DataFrame foi carregado corretamente
    """
    assert df is not None, 'O DataFrame não foi carregado'
    assert len(df) > 0, 'O DataFrame está vazio'
    assert 'Timestamp' in df.columns, 'Coluna Timestamp não encontrada'
    assert 'Gender' in df.columns, 'Coluna Gender não encontrada'