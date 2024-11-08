# Streamlit
import streamlit as st

# Libs AI
from pydub import AudioSegment

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

        with st.spinner("Verificando satisfação do cliente"):
            resumo_ligacao = resumo_consolidado_ligacao(transcricao)
            st.write("Resumo da ligação:")
            st.write(resumo_ligacao)
            st.write("")


if __name__ == "__main__":
    main()
