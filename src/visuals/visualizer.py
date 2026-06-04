import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from loguru import logger
from src import config


class VisualizacaoGraficas:
    """Responsavel por gerar graficos onde pode comparar o resultado das analises"""

    def __init__(self, df: pd.DataFrame | pd.Series):
        self.df = df

    def grafico_comparacao(self, df_carteira) -> go.Figure:
        self.df_carteira = df_carteira
        self.df_comparacao = self.df.drop(columns=config.ACOES)
        print(type(self.df))
        print(type(self.df_comparacao))
        self.df_comparacao["Carteira"] = df_carteira["Total"]
        self.df_comparacao = (self.df_comparacao / self.df_comparacao.iloc[0] - 1) * 100

        # Criação do gráfico
        grafico = px.line(
            self.df_comparacao,
            x=self.df_comparacao.index,
            y=self.df_comparacao.columns,
            labels={"Index": "Data", "value": "Valor"},
            title="Evolução comprativa de ativos",
        )

        # Melhoria de layout e interatividade
        grafico.update_layout(
            template="plotly_dark",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            hovermode="x unified",
        )

        grafico.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1a", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
        )
        logger.success("Gráfico gerado com sucesso")
        return grafico

    def grafico_correlacao(self, df_carteira: pd.DataFrame | pd.Series) -> go.Figure:
        self.df_carteira = df_carteira
        self.df["Carteira"] = self.df_carteira["Total"]
        # correlação
        tabela_rentabilidade_diaria = self.df / self.df.shift(1)
        tabela_rentabilidade_diaria = np.log(tabela_rentabilidade_diaria).dropna()  # type: ignore
        tabela_correlacao = tabela_rentabilidade_diaria.corr()

        # criação do gráfico
        grafico_correlacao = px.imshow(
            tabela_correlacao,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            labels=dict(x="Ativo", y="Ativo", color="Correlação"),
        )

        # Melhoria de layout e interatividade
        grafico_correlacao.update_layout(
            template="plotly_dark",
            title={
                "text": "Matriz de Correlação dos Ativos",
                "y": 0.95,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            coloraxis_colorbar=dict(
                title="Correlação",
                thicknessmode="pixels",
                thickness=20,
                lenmode="pixels",
                len=300,
            ),
        )

        grafico_correlacao.update_traces(
            hovertemplate="Ativo X: %{x}<br>Ativo Y: %{y}<br>Correlação: %{z:.3f}<extra></extra>"
        )
        grafico_correlacao.update_xaxes(tickangle=-45)

        return grafico_correlacao

    def grafico_especializado(self) -> go.Figure:
        # media movel 50 dias
        self.df["MM50"] = self.df["Close"].rolling(50).mean()  # type: ignore

        # media movel 200 dias
        self.df["MM200"] = self.df["Close"].rolling(200).mean()  # type: ignore

        # criação da figura
        grafico = go.Figure()

        # adiciona o Candlestick
        print(self.df.columns)
        grafico.add_trace(
            go.Candlestick(
                x=self.df.index,
                open=self.df["Open"],
                close=self.df["Close"],
                high=self.df["High"],
                low=self.df["Low"],
                name="Preço",
                increasing_line_color="#26a69a",
                decreasing_line_color="#ef5350",
            )
        )

        # adicionar as médias
        grafico.add_trace(
            go.Scatter(
                x=self.df.index,
                y=self.df["MM50"],
                name="MM50",
                line={"color": "#ffffff", "width": 1.5},
            )
        )

        # adicionar a serie da MM200
        grafico.add_trace(
            go.Scatter(
                x=self.df.index,
                y=self.df["MM200"],
                name="MM200",
                line={"color": "#ffeb3b", "width": 1.5},
            )
        )

        grafico.update_layout(
            template="plotly_dark",
            title="Análise Técnica: Preço e Médias Móveis",
            xaxis_rangeslider_visible=False,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )

        return grafico
