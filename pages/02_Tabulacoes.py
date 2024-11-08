# Streamlit
import streamlit as st

# Libs AI
from pydub import AudioSegment
import pandas as pd
from pandasai import SmartDataframe

# Outras
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
    audio.export("./audios/temp.wav", format="wav")

    with open("./audios/temp.wav", "rb") as audio_file:
        # response = whisper.transcribe(file=audio_file)
        response = whisper.audio.transcriptions.create(
            file=audio_file,
            model=AZURE_OPENAI_DEPLOYMENT_WHISPER,
            response_format="text",
        )

    texto_transcrito = response
    return texto_transcrito


def similarity_search(texto):
    """Função para buscar o texto da coluna 'Quando Usar' por similaridade"""
    df = pd.read_excel("./Taxonomias-CLIENTE-A-31-10-2024_12_06.xlsx")
    sdf = SmartDataframe(
        df,
        name="Taxonomias da central de atendimento",
        description="Tabela de taxonomias para classificação da ligação de acordo com a coluna 'Quando usar'",
        config={
            "llm": llm,
            "enable_cache": False,
            "enforce_privacy": False,
            "verbose": False,
            "allow_dangerous_code": True,
        },
    )
    query = f"""
    Seu papel é localizar no dataframe qual seria a categoria ideal para o problema do meu cliente.

    Busque na coluna 'Quando usar' o termo que melhor se assemelha ao motivo da ligação.
    Pode ser que não se enquadre 100%, mas sempre categorize de alguma forma.

    Resumo da ligação:
    {texto}

    
    Forma de saída:
    'Origem' > 'Tipo' > 'Motivo' > 'Submotivo'
    """
    response = sdf.chat(query)
    return response


def resumo_consolidado_ligacao(texto):
    response = llm.invoke(
        f"""
        Identifique no contexto os pontos abaixo:
            - Motivo da ligação
            - Solução proposta
            - Se o problema foi resolvido
        
        Contexto:
        {texto}

        Saída no formato:
            - Motivo da ligação: motivo
            - Solução proposta: solução
            - Problema resolvido? Sim ou não, se teve alinhamento de novas ações ou retorno da ligação
        """
    )
    return response.content


def main():
    st.header("Avaliação ligações")
    uploaded_file = st.file_uploader(
        "Anexe uma ligação abaixo", type=["wav", "mp3", "m4a", "mp4"]
    )
    if uploaded_file is not None:
        with st.spinner("Transcrevendo áudio"):
            with open(PASTA_AUDIOS / uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
                save_path = PASTA_AUDIOS / uploaded_file.name
            transcricao = transcrever_audio(save_path)

        st.write("Transcrição:")
        st.write(transcricao)
        st.write("")

        with st.spinner("Resumindo..."):
            resumo_ligacao = resumo_consolidado_ligacao(transcricao)
            st.write("Descrição:")
            st.write(resumo_ligacao)
            st.write("")

        with st.spinner("Tabulando..."):
            tabulacao = similarity_search(resumo_ligacao)
            st.write("Tabulação:")
            st.write(tabulacao)
            st.write("")


if __name__ == "__main__":
    main()
