import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from loguru import logger
import os


class ExtratorDados:
    """Responsável estritamente por se conectar à API externa e coletar dados limpos."""

    def __init__(self, tickers: list[str] | str, qtde_dias) -> None:
        self.tickers = tickers
        self.data_inicio = (datetime.now() - timedelta(days=qtde_dias)).strftime(
            "%Y-%m-%d"
        )
        self.data_fim = datetime.now().strftime("%Y-%m-%d")

    def baixar_cotacoes(self) -> pd.DataFrame | pd.Series:
        # yf.download(ticker, data_inicio, data_fim)
        try:
            logger.info("Criando DataFrame")
            df = yf.download(
                self.tickers, self.data_inicio, self.data_fim, auto_adjust=False
            )
            if df is None or df.empty:
                raise ValueError(
                    f"O yfinance não retornou dados. "
                    f"Verifique se os tickers {self.tickers} estão corretos ou se há problemas de conexão."
                )
            elif isinstance(df.columns, pd.MultiIndex):
                df = df["Adj Close"]  # type: ignore
            logger.success("DataFrame filtrado")

            df = df.ffill()  # type: ignore

            df = df.dropna()
            logger.success("DataFrame criado")
            return df

        except Exception as e:
            logger.exception("Falha critica noa extração de dados")
            raise e

    @staticmethod
    def salvar_dados(
        df: pd.DataFrame | pd.Series, nome_arquivo: str, pasta: str
    ) -> None:
        """Salva o DataFrame em uma pasta especifica, se a pasta não existir ele mesmo a cria"""
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            logger.success(f"{pasta} criada com sucesso")
        caminho_completo = os.path.join(pasta, nome_arquivo)
        df.to_csv(caminho_completo)
        logger.success(f"Arquivo criado com sucesso em {caminho_completo}")

    def baixar_cotacoes_full(self) -> pd.DataFrame | pd.Series:
        try:
            logger.info("Criando DataFrame")
            df = yf.download(
                self.tickers, self.data_inicio, self.data_fim, auto_adjust=False
            )
            if df is None or df.empty:
                raise ValueError(
                    f"O yfinance não retornou dados."
                    f"Verifique se os tickers {self.tickers} estão corretos ou se há problemas de conexão."
                )
            elif isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df = df.ffill()  # type: ignore

            df = df.dropna()
            logger.success("DataFrame criado")
            return df

        except Exception as e:
            logger.exception("Falha critica noa extração de dados")
            raise e
