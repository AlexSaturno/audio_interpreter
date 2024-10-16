import streamlit as st
from langchain_openai import AzureChatOpenAI
from openai import AzureOpenAI
from pathlib import Path
import os

# Variáveis de ambiente AI
PASTA_RAIZ = Path(__file__).parent
PASTA_AUDIOS = Path(__file__).parent / "audios"
if not os.path.exists(PASTA_AUDIOS):
    os.makedirs(PASTA_AUDIOS)

AZURE_OPENAI_API_KEY = st.secrets["AZURE_OPENAI_API_KEY"]
AZURE_OPENAI_ENDPOINT = st.secrets["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_API_VERSION = st.secrets["AZURE_OPENAI_API_VERSION"]
AZURE_OPENAI_DEPLOYMENT = st.secrets["AZURE_OPENAI_DEPLOYMENT"]
AZURE_OPENAI_MODEL = st.secrets["AZURE_OPENAI_MODEL"]
AZURE_OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME = st.secrets[
    "AZURE_OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME"
]
AZURE_OPENAI_ADA_EMBEDDING_MODEL_NAME = st.secrets[
    "AZURE_OPENAI_ADA_EMBEDDING_MODEL_NAME"
]
AZURE_OPENAI_DEPLOYMENT_WHISPER = st.secrets["AZURE_OPENAI_DEPLOYMENT_WHISPER"]
AZURE_OPENAI_MODEL_WHISPER = st.secrets["AZURE_OPENAI_MODEL_WHISPER"]
AZURE_OPENAI_API_VERSION_WHISPER = st.secrets["AZURE_OPENAI_API_VERSION_WHISPER"]

# Configurações da API
llm = AzureChatOpenAI(
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    model=AZURE_OPENAI_MODEL,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
    api_key=AZURE_OPENAI_API_KEY,
    openai_api_type="azure",
)
whisper = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION_WHISPER,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)
