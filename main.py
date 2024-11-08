################################################################################################################################
# Bibliotecas
################################################################################################################################
import streamlit as st

from utils import *

################################################################################################################################
# UX
################################################################################################################################
# Inicio da aplicação
st.set_page_config(
    page_title="Central",
    page_icon=":black_medium_square:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Leitura do arquivo css de estilização
with open("./styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# List of pages
pages = {
    "01_Motivos_Chamadas": "./pages/01_Motivos_Chamadas.py",
    "02_Tabulacoes": "./pages/02_Tabulacoes.py",
}


################################################################################################################################
# UI
################################################################################################################################
# Inicio da aplicação
def main():
    st.subheader("Página inicial", divider=True)
    motivos_button = st.button("Motivos Chamadas", key="button_motivos")
    tabulacoes_button = st.button("Tabulacoes", key="button_tabulacoes")

    if motivos_button:
        st.switch_page(pages["01_Motivos_Chamadas"])
    if tabulacoes_button:
        st.switch_page(pages["02_Tabulacoes"])


if __name__ == "__main__":
    main()
