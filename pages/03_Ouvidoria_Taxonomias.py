# Streamlit
import streamlit as st
from st_aggrid import AgGrid

# Outras
from utils import *
import pandas as pd
import json
from langchain.prompts import PromptTemplate
from datetime import datetime, timedelta


################################################################################################################################
# UX
################################################################################################################################
# Início da aplicação
st.set_page_config(
    page_title="Classificador taxonomias",
    page_icon=":black_medium_square:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# Leitura do arquivo CSS de estilização
with open("./styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "processado" not in st.session_state:
    st.session_state.processado = False
if "arquivo_gerado" not in st.session_state:
    st.session_state.arquivo_gerado = None

################################################################################################################################
# FUNÇÕES
################################################################################################################################
PROMPT = """
Você analisa comentários feitos por clientes e os categoriza como:
- ATENDIMENTO
- CANAIS
- PRODUTO
- PROCESSOS

Um comentário pode se enquadrar em duas categorias, nesse caso responda as duas.

Depois você informa se o comentário foi positivo, neutro ou negativo

Formato de saída esperado, SOMENTE:
    "cliente": cd_cli,
    "verbatim": comentario,
    "pilar": categorização,
    "avaliacao": satisfação

Context:
{context}

Human: {question}
"""


# Função para atualizar o estado após clique do botão de download. Objetivo é limpar a tela e remover anexo para não reprocessar
def update_key():
    st.session_state["uploader_key"] += 1


# Função para formatar o prompt e obter a resposta para um cliente
def obter_classificacao(cliente):
    prompt_template = PromptTemplate.from_template(PROMPT)
    prompt_formatado = prompt_template.format(
        context=cliente.to_dict(), question="Classifique o comentário do cliente"
    )

    # Chamada ao modelo LLM
    response = llm.invoke(input=prompt_formatado)
    return response.content


def main():
    st.header("Classificação taxonomias")

    if "uploader_key" not in st.session_state:
        st.session_state["uploader_key"] = 0

    if "uploaded" not in st.session_state:
        st.session_state["uploaded"] = []

    uploaded_file = st.file_uploader(
        "Anexe uma ligação abaixo",
        type=["xlsx"],
        key=st.session_state["uploader_key"],
    )

    if uploaded_file is not None:
        with open(PASTA_ARQUIVOS / uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
            save_path = PASTA_ARQUIVOS / uploaded_file.name
        st.session_state["uploaded"] = uploaded_file

        # Tratamento do Dataframe
        with st.spinner("Analisando planilha..."):
            df = pd.read_excel(save_path)
            df["CD CLI"] = df["CD CLI"].dropna().apply(lambda x: str(int(x)))
            df = df[["CD CLI", "VERBATIM"]]

        with st.spinner("Processando planilha..."):
            # Lista para armazenar as respostas
            respostas = []

            # Loop para iterar sobre todas as linhas do dataframe (Deixar o head(X) para homologar)
            # for idx, cliente in df.head(5).iterrows():
            for idx, cliente in df.iterrows():
                resposta = obter_classificacao(cliente)
                respostas.append(resposta)

            # Limpa as strings para manter apenas o JSON válido
            cleaned_data = [
                item.replace("```json\n", "").replace("\n```", "").strip()
                for item in respostas
            ]

            # Converte as strings JSON em dicionários
            parsed_data = [json.loads(item) for item in cleaned_data]

            # Cria o DataFrame com os dados e salva o excel
            df_parsed = pd.DataFrame(parsed_data)

            # Exibe o DataFrame com streamlit (AgGrid)
            AgGrid(df_parsed)

            data_processamento = datetime.now().strftime("%Y-%m-%d")
            hora_processamento = (datetime.now() - timedelta(hours=3)).strftime("%H-%M")
            arquivo_excel = f"taxonomias_{data_processamento}_{hora_processamento}.xlsx"
            df_parsed.to_excel(arquivo_excel, index=False)

        # Exporta para um arquivo Excel
        with open(f"{arquivo_excel}", "rb") as f:
            st.download_button(
                "Download Excel", f, f"{arquivo_excel}", on_click=update_key
            )


if __name__ == "__main__":
    main()
