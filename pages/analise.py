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


def filter_dataframe(df, parlamentar, data_hora):
    filtered_df = df[(df.orador == parlamentar) & (df.dataHoraInicio == data_hora)]
    return filtered_df[["dataHoraInicio","tipoDiscurso","transcricao","contagemPalavras","faseEvento_titulo","orador","topicos","similar_topics","similarity","topic_1","topic_2","topic_3"]]


def filter_deputados(df, parlamentar):
    #df['nome'] = df['nome'].str.lower()
    exclude_names = ['presidente', ' ']
    df['nome'] = df['nome'].apply(lambda x: x.lower() if x not in exclude_names else x)
    filtered_deputados = df[(df.nome == parlamentar)]
    return filtered_deputados[["urlFoto"]]

DATA_DEPUTADOS = ('deputados2023.csv')


def load_data_deputados():
    data_deputados = pd.read_csv(DATA_DEPUTADOS)
    return data_deputados
   
df_deputados = load_data_deputados()

DATE_COLUMN = 'dataHoraInicio'
DATA = ("discursos_2023_stream.csv")


def load_data():
    data = pd.read_csv(DATA)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
df = load_data()
    
parlamentares = sorted(df['orador'].unique())
selecao_parlamentares = st.sidebar.selectbox(
    "Selecione um parlamentar", options=parlamentares
)

data_hora = [x for x, y in zip(df.dataHoraInicio, df.orador) if y == selecao_parlamentares]
selecao_data_hora = st.sidebar.selectbox(
    "Selecione uma data / hora", options=data_hora
)

filtered_df = filter_dataframe(df, selecao_parlamentares, selecao_data_hora)
filtered_deputados = filter_deputados(df_deputados, selecao_parlamentares)
foto = filtered_deputados["urlFoto"].tolist()[0]
discurso = filtered_df["transcricao"].tolist()[0]

st.subheader("Parlamentar")
st.write(filtered_df["orador"].tolist()[0])
st.markdown(f'<img src="{foto}" alt="Alt Text" width=100 height=130>', unsafe_allow_html=True)
st.subheader("Data / hora")
st.write(filtered_df["dataHoraInicio"].tolist()[0])
st.subheader("Contagem de palavras")
st.write(filtered_df["contagemPalavras"].tolist()[0])
st.subheader("Tipo")
st.write(filtered_df["tipoDiscurso"].tolist()[0])
st.subheader("Discurso")
st.write(discurso)

df_topicos1 = pd.DataFrame(columns=['Tópico 1', 'Probabilidades 1'])
pattern = r"\('(.*?)', (.*?)\)"
for index, row in filtered_df.iterrows():
    tuples = re.findall(pattern, row['topic_1'])
    for tuple in tuples:
        df_topicos1 = df_topicos1.append({'Tópico 1': tuple[0], 'Probabilidades 1': float(tuple[1])}, ignore_index=True)

df_topicos2 = pd.DataFrame(columns=['Tópico 2', 'Probabilidades 2'])
pattern = r"\('(.*?)', (.*?)\)"
for index, row in filtered_df.iterrows():
    tuples = re.findall(pattern, row['topic_2'])
    for tuple in tuples:
        df_topicos2 = df_topicos2.append({'Tópico 2': tuple[0], 'Probabilidades 2': float(tuple[1])}, ignore_index=True)

df_topicos3 = pd.DataFrame(columns=['Tópico 3', 'Probabilidades 3'])
pattern = r"\('(.*?)', (.*?)\)"
for index, row in filtered_df.iterrows():
    tuples = re.findall(pattern, row['topic_3'])
    for tuple in tuples:
        df_topicos3 = df_topicos3.append({'Tópico 3': tuple[0], 'Probabilidades 3': float(tuple[1])}, ignore_index=True)

combined_df = pd.concat([df_topicos1, df_topicos2, df_topicos3], axis=1)
st.write(combined_df)