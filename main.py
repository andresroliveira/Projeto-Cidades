import time

import pandas as pd
import requests
from tqdm import tqdm

URL_BASE = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "ProjetoCidadesPesquisa/1.0"
CIDADES = [
    "Campinas",  
    "Guaxupe",
    "Muzambinho",
    "Guaranesia",
    "Juruaia",
    "Monte Belo",
    "Sao Pedro da Uniao",
    "Nova Resende",
    "Cabo Verde",
    "Botelhos",
    "Monte Santo de Minas",
    "Arceburgo",
    "Areado",
    "Alterosa",
    "Machado",
    "Pocos de Caldas",
]


def main():
    print("Iniciando a coleta de dados geográficos das cidades...")
    headers = {"User-Agent": USER_AGENT}
    dados = []
    for cidade in tqdm(CIDADES, desc="Coletando dados"):
        # https://nominatim.openstreetmap.org/search?q=Campinas,Brazil&format=json&polygon_geojson=1
        url = f"{URL_BASE}?q={cidade},Brazil&format=json"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if data:
                item = data[0]
                registro = {
                    "place_id": item.get("place_id"),
                    "name": item.get("name"),
                    "type": item.get("type"),
                    "lat": item.get("lat"),
                    "lon": item.get("lon"),
                    "display_name": item.get("display_name"),
                }
                dados.append(registro)
        except Exception as e:
            tqdm.write(f"Erro ao coletar dados para {cidade}: {e}")
        time.sleep(1)
    if dados:
        df = pd.DataFrame(dados)
        print("\n--- Prévia dos dados ---")
        print(df.head())
        output_file = "cidades_geo.csv"
        df.to_csv(output_file, index=False, encoding="utf-8")
        print(f"\nArquivo '{output_file}' salvo com sucesso com {len(df)} registros!")
    else:
        print("\nNenhum dado foi coletado.")


main()
