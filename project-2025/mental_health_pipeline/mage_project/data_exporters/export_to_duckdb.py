import pandas as pd
import duckdb
from mage_ai.data_preparation.repo_manager import get_repo_path
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_duckdb(df: pd.DataFrame, **kwargs) -> None:
    """
    Exports the data to DuckDB for further transformation using DBT.
    """
    # Path to the DuckDB file
    db_path = path.join(get_repo_path(), '..', 'data', 'duckdb', 'mental_health.db')
    
    # Connect to DuckDB
    con = duckdb.connect(db_path)
    
    # Create raw table if it doesn't exist
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
    
    # Clean up previous data
    con.execute("DELETE FROM raw_mental_health")
    
    # Insert new data
    con.register('temp_df', df)
    con.execute("INSERT INTO raw_mental_health SELECT * FROM temp_df")
    
    # Check record count
    count = con.execute("SELECT COUNT(*) FROM raw_mental_health").fetchone()[0]
    
    # Close connection
    con.close()
    
    print(f"Data exported to DuckDB: {count} records in table raw_mental_health")
