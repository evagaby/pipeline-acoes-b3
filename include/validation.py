from sqlalchemy.ext.asyncio import result
import pprint
from include.api_conection import api_conection
def validation():
    success = []
    erros = []
    resposta = api_conection()
    for item in resposta['results']:
        symbol = item.get("symbol")
        data = item.get("data")
        preco_regular = data.get("regularMarketPrice")
        if symbol is None:
            dicionario_symbol = {
                    "codigo_de_erro": "400",
                    "mensagem": "sem symbol",
                    "task_origem": "validação"
                }
            erros.append(dicionario_symbol)
            continue

        if preco_regular is None:
            dicionario_preco = {
                    "codigo_de_erro": "400",
                    "mensagem": "sem preco",
                    "task_origem": "validação"
                }
            erros.append(dicionario_preco)
            continue

        dicionario_success = {
            "symbol": symbol,
            "nome_da_empresa": data.get("longName"),
            "moeda": data.get('currency'),
            "preco_regular": preco_regular,
            "preco_mais_alto": data.get('regularMarketDayHigh'),
            "preco_mais_baixo": data.get('regularMarketDayLow'),
            "variacao_de_preco": data.get('regularMarketChange'),
            "percentual_variacao_de_preco": data.get('regularMarketChangePercent')}
        success.append(dicionario_success)
    return success,erros



