import streamlit as st
import pandas as pd
import numpy as np
import re

st.set_page_config(
    "Discurso Parlamentar",
    "📊",
    initial_sidebar_state="expanded",
    layout="wide",
    )

st.header("Análise de discurso parlamentar :classical_building: :bar_chart:")

@st.cache_data
def filter_dataframe(df, parlamentar):
    filtered_df = df[(df.orador == parlamentar)]
    return filtered_df[["dataHoraInicio","tipoDiscurso","transcricao","contagemPalavras","faseEvento_titulo","orador","topicos","similar_topics","similarity","topic_1","topic_2","topic_3"]]

@st.cache_data
def filter_deputados(df, parlamentar):
    df['nome'] = df['nome'].str.lower()
    filtered_deputados = df[(df.nome == parlamentar)]
    return filtered_deputados[["urlFoto"]]

DATA_DEPUTADOS = ('deputados2023.csv')

@st.cache_data
def load_data_deputados():
    data_deputados = pd.read_csv(DATA_DEPUTADOS)
    return data_deputados
   
df_deputados = load_data_deputados()

DATE_COLUMN = 'dataHoraInicio'
DATA = ("discursos_2023_stream.csv")

@st.cache_data
def load_data():
    data = pd.read_csv(DATA)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
df = load_data()
    
#st.sidebar.subheader("Escolha um parlamentar")

parlamentares = df.orador.unique()
selecao_parlamentares = st.sidebar.selectbox(
    "Selecione um parlamentar", options=parlamentares
)


filtered_df = filter_dataframe(df, selecao_parlamentares)
filtered_deputados = filter_deputados(df_deputados, selecao_parlamentares)
foto = filtered_deputados["urlFoto"].tolist()[0]


st.subheader("Parlamentar")
st.markdown(f'<img src="{foto}" alt="Alt Text" width=100 height=130>', unsafe_allow_html=True)
st.write(filtered_df["orador"].tolist()[0])

st.subheader("Discursos realizados em 2023 (contagem de palavras)")

grouped_df = filtered_df.groupby("dataHoraInicio").agg({"contagemPalavras": "sum"})
st.bar_chart(grouped_df)

st.subheader("Discursos por tipo (contagem de palavras)")
grouped_df_2 = filtered_df.groupby("tipoDiscurso").agg({"contagemPalavras": "sum"})
# Create a bar chart using the grouped DataFrame
st.bar_chart(grouped_df_2)

