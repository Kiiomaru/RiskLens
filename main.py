import os
from src import config
from loguru import logger
from src.data.extractor import ExtratorDados
from src.simulation.simulator import SimuladorCarteira
from src.processing.processor import AnalisadorPerformance
from src.visuals.visualizer import VisualizacaoGraficas


# 1. Preparação do Ambiente (O Maestro faz isso)
if not os.path.exists(config.PASTA_LOGS):
    os.makedirs(config.PASTA_LOGS)
    logger.success(f"A pasta {config.PASTA_LOGS} foi criada com sucesso")
else:
    logger.info(f"Diretório de logs já existente: {config.PASTA_LOGS}")

# 2. Configuração do Logging
logger.add(f"{config.PASTA_LOGS}/file_{{time}}.log", rotation="5 MB", level="INFO")


def principal():
    # 3. Execução
    logger.info("Iniciando o sistema...")
    extrator = ExtratorDados(tickers=config.TODOS_TICKERS, qtde_dias=730)
    df = extrator.baixar_cotacoes()
    ExtratorDados.salvar_dados(df, config.DF_EXTRACAO, config.PASTA_OUTPUT)
    logger.success("Dados baixados com sucesso!")
    logger.success("Pasta criada com sucesso")

    simulador = SimuladorCarteira(config.CARTEIRA)
    df_carteira = simulador.calcular_evolucao_patrimonial(df)

    df_ajustado = AnalisadorPerformance.ajustar_benchmark_cambio(df)
    retorno = AnalisadorPerformance.calcular_retorno_percentual(df_ajustado)
    logger.info(retorno)

    graficos = VisualizacaoGraficas(df_ajustado)
    graficos_comparacao = graficos.grafico_comparacao(df_carteira)
    graficos_comparacao.show()
    logger.success("Grafico de comparação criado com sucesso")

    grafico_correlacao = graficos.grafico_correlacao(df_carteira)
    grafico_correlacao.show()
    logger.success("Grafico de correlação criado com sucesso")

    extrator = ExtratorDados(tickers="VALE3.SA", qtde_dias=730)
    df_cotacao = extrator.baixar_cotacoes_full()
    visualizador = VisualizacaoGraficas(df_cotacao)
    grafico_especializado = visualizador.grafico_especializado()
    grafico_especializado.show()
    logger.success("Grafico de especialização criado com sucesso")


if __name__ == "__main__":
    principal()
