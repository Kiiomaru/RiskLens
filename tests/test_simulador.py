import pytest
import pandas as pd
from src.simulation.simulator import SimuladorCarteira


def test_simulador_ativo_inexistente():
    # Cria um DF simples
    df = pd.DataFrame({"VALE3.SA": [10, 11]}, index=[0, 1])
    simulador = SimuladorCarteira(dic_carteira={"ITUB4.SA": 100})

    # Testa se levanta erro quando ITUB4.SA não está no DF
    with pytest.raises(ValueError, match="não foi encontrado no DataFrame"):
        simulador.calcular_evolucao_patrimonial(df)
