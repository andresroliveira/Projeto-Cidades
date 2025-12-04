import pandas as pd
import folium
import os


def main():
    file_name = "cidades_geo.csv"
    if not os.path.exists(file_name):
        print(f"Erro: O arquivo '{file_name}' não foi encontrado.")
        print("Rode o script de coleta primeiro.")
        return
    df = pd.read_csv(file_name)
    print(f"Carregadas {len(df)} cidades.")
    if df.empty:
        print("O arquivo CSV está vazio.")
        return
    centro_lat = float(df['lat'].mean())
    centro_lon = float(df['lon'].mean())

    mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=9)

    for _, row in df.iterrows():
        name = str(row["name"])
        tipe = str(row["type"])
        lat = float(row["lat"])
        lon = float(row["lon"])

        info_popup = f"<b>{name}</b><br>{tipe}</br>"

        folium.Marker(location=[lat, lon],
                      popup=info_popup,
                      tooltip=name,
                      icon=folium.Icon(color="blue",
                                       icon="info-sign")).add_to(mapa)

    arquivo_saida = "mapa_cidades.html"
    mapa.save(arquivo_saida)

    print(f"Mapa salvo em '{arquivo_saida}'!")


main()
