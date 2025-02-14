import pandas as pd
import requests
import time

INPUT_CSV = "data/ceps_lista_30.csv"
OUTPUT_CSV = "data/resultados.csv"

# Função para buscar o endereço na API ViaCEP
def buscar_endereco(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "erro" not in data:
            return {
                "cep": data["cep"],
                "logradouro": data["logradouro"],
                "bairro": data["bairro"],
                "cidade": data["localidade"],
                "estado": data["uf"]
            }
    return None

df = pd.read_csv(INPUT_CSV, dtype=str)

resultados = []

for cep in df["CEP"]:
    endereco = buscar_endereco(cep)
    if endereco:
        resultados.append(endereco)
    else:
        print(f" Erro ao buscar o CEP {cep}")
    time.sleep(1) 

df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv(OUTPUT_CSV, index=False)

print(f" Consulta finalizada! Resultados salvos em {OUTPUT_CSV}")
