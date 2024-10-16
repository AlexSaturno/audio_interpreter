# Streamlit
import streamlit as st

# Libs AI
from langchain_openai import AzureChatOpenAI
from openai import AzureOpenAI
from pydub import AudioSegment

# Outras
import json
import os
from pathlib import Path
from utils import *


################################################################################################################################
# UX
################################################################################################################################
# Início da aplicação
st.set_page_config(
    page_title="Avaliador de ligações",
    page_icon=":black_medium_square:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# Leitura do arquivo CSS de estilização
with open("./styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


################################################################################################################################
# FUNÇÕES
################################################################################################################################
def transcrever_audio(audio_path):
    # Carregar arquivo de áudio e converter para formato compatível, como wav
    audio = AudioSegment.from_file(audio_path)
    audio.export("temp.wav", format="wav")

    with open("temp.wav", "rb") as audio_file:
        # response = whisper.transcribe(file=audio_file)
        response = whisper.audio.transcriptions.create(
            file=audio_file,
            model=AZURE_OPENAI_DEPLOYMENT_WHISPER,
            response_format="text",
        )

    texto_transcrito = response
    return texto_transcrito


def analise_sentimento(texto):
    response = llm.invoke(
        f"Faça uma análise de sentimento do seguinte texto identificando Raiva, Alegria, Indiferença, Felicidade:\n\n{texto}"
    )
    return response.content


def identificar_motivo(texto):
    response = llm(f"Identifique o motivo do contato no seguinte texto:\n\n{texto}")
    return response.content


def identificar_solucao(texto):
    response = llm(
        f"Identifique se o problema foi solucionado no seguinte texto:\n\n{texto}"
    )
    return response.content


def verificar_satisfacao(texto):
    response = llm(
        f"Identifique se o usuário está satisfeito com a ação tomada pelo operador no seguinte texto:\n\n{texto}"
    )
    return response.content


def calcular_tempos(texto):
    # Este é um exemplo fictício, na prática você precisaria calcular os tempos a partir de marcas no texto.
    response = llm(
        f"Calcule os seguintes tempos do seguinte texto: TMA - tempo médio de atendimento, TME - tempo médio de espera, TMS - tempo médio em silêncio por parte do operador:\n\n{texto}"
    )
    return response.content


def main():
    st.header("Avaliação ligações")
    uploaded_file = st.file_uploader("Anexe uma ligação no formato .wav", type="wav")
    if uploaded_file is not None:
        with st.spinner("Transcrevendo áudio"):
            with open(PASTA_RAIZ / uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
                save_path = PASTA_RAIZ / uploaded_file.name
            transcricao = transcrever_audio(save_path)

        with st.spinner("Avaliando motivo da ligação"):
            motivo = identificar_motivo(transcricao)
            st.write("Motivo:")
            st.write(motivo)
            st.write("")

        with st.spinner("Avaliando solução proposta"):
            solucao = identificar_solucao(transcricao)
            st.write("Solução:")
            st.write(solucao)
            st.write("")

        with st.spinner("Verificando satisfação do cliente"):
            satisfacao = verificar_satisfacao(transcricao)
            st.write("Satisfação:")
            st.write(satisfacao)
            st.write("")


if __name__ == "__main__":
    main()
