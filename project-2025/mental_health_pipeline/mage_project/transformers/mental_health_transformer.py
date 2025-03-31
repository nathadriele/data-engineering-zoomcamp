from mage_ai.data_preparation.repo_manager import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.file import FileIO
from pandas import DataFrame
from os import path

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Transforms and cleans the data for analysis.
    
    Args:
        data: The DataFrame with raw data loaded previously.
        
    Returns:
        DataFrame: The transformed DataFrame.
    """
    print(f"Transforming data with {len(data)} records")
    
    df = data.copy()
    
    # Standardize values
    df['Country'] = df['Country'].str.title()
    df['Gender'] = df['Gender'].str.title()
    
    # Create binary indicator for mental health treatment
    df['has_treatment'] = df['treatment'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    # Create binary indicator for family history
    df['has_family_history'] = df['family_history'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    # Approximate number of days indoors (mean value per range)
    def extract_days(days_range):
        if pd.isna(days_range) or days_range == '':
            return None
        elif days_range == '1-14 days':
            return 7
        elif days_range == '15-30 days':
            return 22
        elif days_range == '31-60 days':
            return 45
        elif days_range == '60+ days':
            return 75
        else:
            return None
    
    df['days_indoors_numeric'] = df['Days_Indoors'].apply(extract_days)
    
    # Create a stress index based on several columns
    df['stress_index'] = (
        (df['Growing_Stress'] == 'Yes').astype(int) * 3 +
        (df['Changes_Habits'] == 'Yes').astype(int) * 2 +
        (df['Mood_Swings'] == 'High').astype(int) * 3 +
        (df['Mood_Swings'] == 'Medium').astype(int) * 2 +
        (df['Coping_Struggles'] == 'Yes').astype(int) * 2
    )
    
    # Group similar occupations
    def standardize_occupation(occupation):
        if pd.isna(occupation) or occupation == '':
            return 'Unknown'
        
        occupation = occupation.lower()
        
        if 'software' in occupation or 'developer' in occupation or 'programmer' in occupation or 'engineer' in occupation:
            return 'Tech'
        elif 'hr' in occupation or 'human resources' in occupation:
            return 'HR'
        elif 'corporate' in occupation or 'business' in occupation or 'manager' in occupation or 'executive' in occupation:
            return 'Corporate'
        elif 'health' in occupation or 'doctor' in occupation or 'nurse' in occupation or 'medical' in occupation:
            return 'Healthcare'
        elif 'teacher' in occupation or 'professor' in occupation or 'education' in occupation:
            return 'Education'
        else:
            return 'Other'
    
    df['occupation_group'] = df['Occupation'].apply(standardize_occupation)
    
    # Flag cases that need immediate attention
    df['needs_attention'] = (
        (df['stress_index'] >= 6) &
        (df['Social_Weakness'] == 'Yes') &
        (df['Work_Interest'] == 'No')
    ).astype(int)
    
    print(f"Transformation completed with {len(df)} records")
    
    return df


@test
def test_output(output, *args) -> None:
    """
    Tests if the transformation was applied correctly.
    """
    assert output is not None, 'Output is null'
    assert isinstance(output, DataFrame), 'Output is not a DataFrame'
    assert 'has_treatment' in output.columns, 'Column has_treatment is missing'
    assert 'stress_index' in output.columns, 'Column stress_index is missing'
    assert 'occupation_group' in output.columns, 'Column occupation_group is missing'
    print('Transformation tests passed successfully!')
