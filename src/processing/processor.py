import pandas as pd
from loguru import logger


class AnalisadorPerformance:
    """Responsável por aplicar cálculos matemáticos, transformações cambiais e métricas."""

    @staticmethod
    def ajustar_benchmark_cambio(
        df: pd.DataFrame | pd.Series,
    ) -> pd.DataFrame | pd.Series:
        logger.info("Iniciando conversão de ativos dolarizados para reais")

        df_ajustado = df.copy()
        if isinstance(df_ajustado, pd.Series):
            df_ajustado = df_ajustado.to_frame()

        colunas_obrigatorias = ["^GSPC", "BRL=X", "GC=F"]

        if not all(col in df_ajustado.columns for col in colunas_obrigatorias):
            raise ValueError(
                f"Faltam colunas necessárias. Esperado {colunas_obrigatorias}"
            )

        try:
            df_ajustado["SP500 (R$)"] = df_ajustado["^GSPC"] * df_ajustado["BRL=X"]
            df_ajustado["Ouro (R$)"] = df_ajustado["GC=F"] * df_ajustado["BRL=X"]
            df_ajustado["Dólar"] = df_ajustado["BRL=X"]

            df_ajustado = df_ajustado.drop(columns=["BRL=X", "GC=F", "^GSPC"])
            logger.info("Ajuste de moeda estrangeira finalizada com sucesso")
            return df_ajustado
        except Exception:
            logger.exception("Erro ao fazer a conversão")
            raise

    @staticmethod
    def calcular_retorno_percentual(
        df: pd.DataFrame | pd.Series,
    ) -> pd.DataFrame | pd.Series:
        if df.empty:
            logger.warning(
                '"Tentativa de calcular o retorno sobre um DataFrame sem registros."'
            )
            return pd.Series()
        return (df.iloc[-1] / df.iloc[0]) - 1
