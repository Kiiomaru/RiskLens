import pandas as pd
from loguru import logger


class SimuladorCarteira:
    """Responsável por gerenciar a composição financeira e evolução da carteira de ativos."""

    def __init__(self, dic_carteira: dict) -> None:
        self.dic_carteira = dic_carteira
        self.total_investido_inicial = sum(self.dic_carteira.values())

    def calcular_evolucao_patrimonial(
        self, df: pd.DataFrame | pd.Series
    ) -> pd.DataFrame | pd.Series:
        logger.info("Calculando evolução patrimonial da carteira de investimentos")
        df_carteira = pd.DataFrame(index=df.index)
        try:
            for ativo, valor_inicial in self.dic_carteira.items():
                if ativo not in df.columns:
                    logger.error(
                        "O ativo está na carteira, mas não no banco de dados do mercado"
                    )
                    raise ValueError(
                        f"O ativo {ativo} está na carteira, mas não foi encontrado no DataFrame."
                    )

                preco_inicial_ativo = df[ativo].iloc[0]
                qtde_acoes = self.dic_carteira[ativo] / preco_inicial_ativo
                df_carteira[ativo] = df[ativo] * qtde_acoes

            df_carteira["Total"] = df_carteira.sum(axis=1)
            logger.success(
                f"Simulção iniciada com sucesso com patrimonio inicial de {self.total_investido_inicial:.2f}"
            )
            return df_carteira
        except Exception as e:
            logger.exception(
                "Erro ao processar calculo financeiro da carteira da carteira"
            )
            raise e
