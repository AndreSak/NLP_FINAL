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
def filter_dataframe(df, parlamentar, data_hora):
    filtered_df = df[(df.orador == parlamentar) & (df.dataHoraInicio == data_hora)]
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
    
st.sidebar.subheader("Escolha um parlamentar")

parlamentares = df.orador.unique()
selecao_parlamentares = st.sidebar.selectbox(
    "Selecione um parlamentar", options=parlamentares
)

st.sidebar.subheader("Escolha uma data / hora")

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
st.subheader("Tópico 1")
st.write(filtered_df["topic_1"].tolist()[0])
st.subheader("Tópico 2")
st.write(filtered_df["topic_2"].tolist()[0])
st.subheader("Tópico 3")
st.write(filtered_df["topic_3"].tolist()[0])
#for i in range(filtered_df["topic_1"]):
#    df_topicos = pd.DataFrame(topic_model.get_topic(similar_topics[i]), columns=["Tópico", "Probabilidade"])
#    st.write(df_topicos)




#st.write(filtered_df["topic_1"])


#df_topicos = pd.DataFrame(filtered_df["topics_details"], columns=['Tópico', 'Probabilidade'])
#df_topicos = df_topicos.explode('Tópico')
#df_topicos['Probabilidade'] = df_topicos['Tópico'].apply(lambda x: x[1])
#df_topicos['Tópico'] = df_topicos['Tópico'].apply(lambda x: x[0])

#df_topicos = pd.DataFrame(filtered_df["topics_details"].tolist()[0], columns=["Tópico", "Probabilidade"])
#st.write(df_topicos)
#for i in range(num_of_topics):
#    st.write(f'As palavras-chave para o tópico {similar_topics[i]} são:')
#    df_topicos = pd.DataFrame(topic_model.get_topic(similar_topics[i]), columns=["Tópico", "Probabilidade"])
#    st.write(df_topicos)
