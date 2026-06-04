import pandas as pd
import pytest

from src.data.extractor import ExtratorDados


@pytest.fixture
def mock_df_raw():
    colunas = pd.MultiIndex.from_tuples(
        [
            ("Adj Close", "ITUB4.SA"),
        ]
    )

    return pd.DataFrame(
        [[10.0], [10.5], [11.0]],
        columns=colunas,
    )


def test_baixar_cotacoes_empty_download(mocker):
    """Deve lançar erro quando o yfinance não retorna dados."""
    print("TESTE NOVO EXECUTANDO")

    mocker.patch("yfinance.download", return_value=None)

    extrator = ExtratorDados(
        tickers=["ITUB4.SA"],
        qtde_dias=30,
    )

    with pytest.raises(
        ValueError,
        match="O yfinance não retornou dados",
    ):
        extrator.baixar_cotacoes()


def test_baixar_cotacoes_remove_multiindex(mocker, mock_df_raw):
    """Deve transformar MultiIndex em Index simples."""

    mocker.patch(
        "yfinance.download",
        return_value=mock_df_raw,
    )

    extrator = ExtratorDados(
        tickers=["ITUB4.SA"],
        qtde_dias=30,
    )

    df = extrator.baixar_cotacoes()

    assert not isinstance(df.columns, pd.MultiIndex)
    assert isinstance(df.columns, pd.Index)


def test_baixar_cotacoes_retorna_colunas_esperadas(
    mocker,
    mock_df_raw,
):
    mocker.patch(
        "yfinance.download",
        return_value=mock_df_raw,
    )

    extrator = ExtratorDados(
        tickers=["ITUB4.SA"],
        qtde_dias=30,
    )

    df = extrator.baixar_cotacoes()

    assert list(df.columns) == ["ITUB4.SA"]
