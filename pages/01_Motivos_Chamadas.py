# Streamlit
import streamlit as st

# Libs AI
from pydub import AudioSegment

# Outras
from utils import *
import io
from datetime import datetime, timedelta


################################################################################################################################
# UX
################################################################################################################################
# Início da aplicação
st.set_page_config(
    page_title="Avaliação de ligações",
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
    if "desativa_download" not in st.session_state:
        st.session_state.desativa_download = True

    st.header("Avaliação de ligações")
    uploaded_files = st.file_uploader(
        "Anexe uma ligação abaixo",
        type=["wav", "mp3", "m4a", "mp4"],
        accept_multiple_files=True,
    )

    transcricoes = []
    nomes_arquivos = []
    texto_output = ""

    with st.container(border=True):
        if uploaded_files is not None:
            if st.session_state["desativa_download"] == True:
                with st.spinner("Transcrevendo áudios e identificando motivos..."):
                    for uploaded_file in uploaded_files:
                        with open(PASTA_AUDIOS / uploaded_file.name, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                            save_path = PASTA_AUDIOS / uploaded_file.name
                        nomes_arquivos.append(uploaded_file.name)
                        transcricoes.append(transcrever_audio(save_path))
                        st.session_state["desativa_download"] = False

            for i, transcricao in enumerate(transcricoes):
                st.write(f"Transcrição do arquivo: {nomes_arquivos[i]}:")
                st.write(transcricao)
                st.write("")

                resumo_ligacao = resumo_consolidado_ligacao(transcricao)
                st.write("Resumo da ligação:")
                st.write(resumo_ligacao)
                st.write("")
                st.write("")
                st.write("")

                texto_output += f"Transcrição do arquivo {nomes_arquivos[i]}:\n{transcricao}\nResumo:\n{resumo_ligacao}\n\n\n\n"

    with st.container(border=False):
        buf = io.StringIO()
        buf.write(texto_output)
        buf.seek(0)

        def export_result():
            buf.seek(0)

        data_processamento = datetime.now().strftime("%Y-%m-%d")
        hora_processamento = (datetime.now() - timedelta(hours=3)).strftime("%H:%M")
        txt_file_download_name = (
            f"transcricoes_{data_processamento}_{hora_processamento}.txt"
        )
        full_path = os.path.join(PASTA_ARQUIVOS, txt_file_download_name)
        if st.download_button(
            "Download Avaliações",
            buf.getvalue().encode("utf-8"),
            txt_file_download_name,
            "text/plain",
            on_click=export_result,
            disabled=st.session_state["desativa_download"],
        ):
            st.session_state["desativa_download"] = True
            with open(full_path + ".txt", "w") as file:
                file.write(texto_output)

        # with st.spinner("Verificando satisfação do cliente"):
        #     resumo_ligacao = resumo_consolidado_ligacao(transcricao)
        #     st.write("Resumo da ligação:")
        #     st.write(resumo_ligacao)
        #     st.write("")


if __name__ == "__main__":
    main()
