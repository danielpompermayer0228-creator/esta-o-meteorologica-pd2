import csv
import re
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Estação Meteorológica Inteligente - PD-II",
    page_icon="🌦️",
    layout="wide"
)

arquivo_csv = "/Users/yukiwatanabe/dados_estacao.csv"

registros = []

with open(arquivo_csv, "r", encoding="utf-8") as arquivo:
    leitor = csv.reader(arquivo)

    for linha in leitor:
        if len(linha) < 2:
            continue

        horario = linha[0]
        dados = ",".join(linha[1:])

        try:
            registros.append({
                "Horário": datetime.strptime(
                    horario, "%Y-%m-%d %H:%M:%S"
                ),
                "Temperatura (°C)": float(
                    re.search(r"TempDHT:([\d.]+)", dados).group(1)
                ),
                "Umidade (%)": float(
                    re.search(r"Umidade:([\d.]+)", dados).group(1)
                ),
                "Pressão (hPa)": float(
                    re.search(r"Pressao:([\d.]+)", dados).group(1)
                ),
                "Luminosidade (ADC)": int(
                    re.search(r"LDR:(\d+)", dados).group(1)
                ),
                "Chuva (básculas)": int(
                    re.search(r"Chuva:(\d+)", dados).group(1)
                )
            })

        except (AttributeError, ValueError):
            continue

if not registros:
    st.error("Nenhum dado válido encontrado.")
    st.stop()

df = pd.DataFrame(registros)
df = df.set_index("Horário")

st.title("🌦️ Estação Meteorológica Inteligente - PD-II")
st.caption("Monitoramento ambiental urbano com ESP32 e sensores IoT")

ultimo = df.iloc[-1]

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Temperatura", f"{ultimo['Temperatura (°C)']:.1f} °C")
col2.metric("Umidade", f"{ultimo['Umidade (%)']:.1f} %")
col3.metric("Pressão", f"{ultimo['Pressão (hPa)']:.1f} hPa")
col4.metric("Luminosidade", f"{int(ultimo['Luminosidade (ADC)'])} ADC")
col5.metric("Chuva", f"{int(ultimo['Chuva (básculas)'])} básculas")

st.subheader("Temperatura e umidade")
st.line_chart(df[["Temperatura (°C)", "Umidade (%)"]])

st.subheader("Pressão atmosférica")
st.line_chart(df[["Pressão (hPa)"]])

st.subheader("Luminosidade")
st.line_chart(df[["Luminosidade (ADC)"]])

st.subheader("Pluviômetro")
st.line_chart(df[["Chuva (básculas)"]])

st.subheader("Dados coletados")
st.dataframe(df, use_container_width=True)

st.caption(
    "Protótipo acadêmico desenvolvido para o Projeto Integrado Multidisciplinar PD-II."
)