from datetime import datetime, timedelta

# Listas de Ativos
ACOES = ["ITUB4.SA", "PETR4.SA", "VALE3.SA", "IVVB11.SA"]
# IBOVESPA -> ^BVSP
# SP500 -> ^GSPC
# DÓLAR -> BRL=X
# OURO (DOLARIZADO) -> GC=F
INDICES = ["^BVSP", "^GSPC", "BRL=X", "GC=F"]
TODOS_TICKERS = ACOES + INDICES

# Dicionário da Carteira
CARTEIRA = {
    "ITUB4.SA": 5000,
    "VALE3.SA": 3000,
    "PETR4.SA": 4000,
    "IVVB11.SA": 6000,
}

# Configurações de Data
DIAS_HISTORICO = 730
DATA_FIM = datetime.now()
DATA_INICIO = DATA_FIM - timedelta(days=DIAS_HISTORICO)

# Pastas
PASTA_LOGS = "logs"
PASTA_OUTPUT = "Output"

# Nomes de arquivos
DF_EXTRACAO = "lista_api"
