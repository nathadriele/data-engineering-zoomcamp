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
    Transforma e limpa os dados para análise.
    
    Args:
        data: O DataFrame com os dados brutos carregados anteriormente.
        
    Returns:
        DataFrame: O DataFrame transformado.
    """
    print(f"Transformando dados com {len(data)} registros")
    
    # Criar uma cópia para trabalhar
    df = data.copy()
    
    # 1. Padronização de valores
    # Converter para capitalizar Country e Gender
    df['Country'] = df['Country'].str.title()
    df['Gender'] = df['Gender'].str.title()
    
    # 2. Criar indicador binário para tratamento de saúde mental
    df['has_treatment'] = df['treatment'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    # 3. Criar indicador binário para histórico familiar
    df['has_family_history'] = df['family_history'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    # 4. Extrair número aproximado de dias em casa (média de cada faixa)
    def extract_days(days_range):
        if pd.isna(days_range) or days_range == '':
            return None
        elif days_range == '1-14 days':
            return 7  # média da faixa 1-14
        elif days_range == '15-30 days':
            return 22  # média da faixa 15-30
        elif days_range == '31-60 days':
            return 45  # média da faixa 31-60
        elif days_range == '60+ days':
            return 75  # valor estimado para 60+
        else:
            return None
    
    df['days_indoors_numeric'] = df['Days_Indoors'].apply(extract_days)
    
    # 5. Criar índice de estresse baseado em várias colunas
    df['stress_index'] = (
        (df['Growing_Stress'] == 'Yes').astype(int) * 3 +  # Peso 3 para estresse crescente
        (df['Changes_Habits'] == 'Yes').astype(int) * 2 +  # Peso 2 para mudanças de hábitos
        (df['Mood_Swings'] == 'High').astype(int) * 3 +    # Peso 3 para oscilações de humor altas
        (df['Mood_Swings'] == 'Medium').astype(int) * 2 +  # Peso 2 para oscilações médias
        (df['Coping_Struggles'] == 'Yes').astype(int) * 2  # Peso 2 para dificuldades de enfrentamento
    )
    
    # 6. Agrupar ocupações similares
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
    
    # 7. Criar flag para casos que precisam de atenção imediata
    df['needs_attention'] = (
        (df['stress_index'] >= 6) &  # Índice de estresse alto
        (df['Social_Weakness'] == 'Yes') &  # Sinais de fraqueza social
        (df['Work_Interest'] == 'No')  # Perda de interesse no trabalho
    ).astype(int)
    
    print(f"Transformação concluída, resultando em {len(df)} registros")
    
    return df


@test
def test_output(output, *args) -> None:
    """
    Testa se a transformação foi aplicada corretamente.
    """
    assert output is not None, 'A saída é nula'
    assert isinstance(output, DataFrame), 'A saída não é um DataFrame'
    assert 'has_treatment' in output.columns, 'A coluna has_treatment está ausente'
    assert 'stress_index' in output.columns, 'A coluna stress_index está ausente'
    assert 'occupation_group' in output.columns, 'A coluna occupation_group está ausente'
    print('Testes de transformação concluídos com sucesso!')