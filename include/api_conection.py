import requests
import os

def api_conection():
    api_key = os.environ.get("BRAPI_API_KEY")
    api_url = "https://brapi.dev/api/v2/stocks/quote"
    resposta = requests.get(api_url,  headers={"Authorization": f"Bearer {api_key}"},
            params={"symbols": "PETR4,VALE3,MGLU3"})
    if resposta.status_code != 200:
       raise Exception(f'Algo deu errado com a requisição {resposta.status_code}')
    return resposta.json()
