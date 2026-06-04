import pytest
import pandas as pd
from src.processing.processor import AnalisadorPerformance


def test_ajustar_benchmark_falta_colunas():
    # DF sem as colunas obrigatórias
    df_errado = pd.DataFrame({"ITUB4.SA": [1, 2]})

    with pytest.raises(ValueError, match="Faltam colunas necessárias"):
        AnalisadorPerformance.ajustar_benchmark_cambio(df_errado)


def test_ajustar_benchmark_sucesso(mock_df_cleaned):
    # Com as colunas presentes, não deve levantar erro
    resultado = AnalisadorPerformance.ajustar_benchmark_cambio(mock_df_cleaned)
    assert resultado is not None
