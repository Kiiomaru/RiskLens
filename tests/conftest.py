import pytest
import pandas as pd


@pytest.fixture
def mock_df_raw():
    # Simulando um DataFrame MultiIndex vindo do yfinance
    data = {
        ("Adj Close", "ITUB4.SA"): [10.0, 10.5, 11.0],
        ("Adj Close", "VALE3.SA"): [20.0, 20.2, 20.5],
    }
    idx = pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"])
    return pd.DataFrame(data, index=idx)


@pytest.fixture
def mock_df_cleaned():
    # DataFrame já limpo para testar simulador/analisador
    data = {
        "ITUB4.SA": [10.0, 10.5, 11.0],
        "VALE3.SA": [20.0, 20.2, 20.5],
        "^GSPC": [4000, 4010, 4020],
        "BRL=X": [5.0, 5.1, 5.0],
        "GC=F": [1900, 1910, 1920],
    }
    return pd.DataFrame(data)
