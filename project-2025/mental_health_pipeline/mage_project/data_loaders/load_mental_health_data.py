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
    Loads data from the mental health CSV file.
    """
    filepath = path.join(get_repo_path(), '..', 'data', 'mental_health_dataset.csv')
    
    df = pd.read_csv(filepath)
    
    # Convert timestamp column to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Fill missing values
    df['self_employed'] = df['self_employed'].fillna('Unknown')
    
    # Ensure text columns are lowercase for standardization
    for col in df.select_dtypes(include=['object']).columns:
        if col != 'Timestamp':
            df[col] = df[col].str.lower() if not df[col].isna().all() else df[col]
    
    print(f"Data loaded: {len(df)} records")
    return df


@test
def test_output(df) -> None:
    """
    Tests if the DataFrame was loaded correctly.
    """
    assert df is not None, 'DataFrame was not loaded'
    assert len(df) > 0, 'DataFrame is empty'
    assert 'Timestamp' in df.columns, 'Timestamp column not found'
    assert 'Gender' in df.columns, 'Gender column not found'
