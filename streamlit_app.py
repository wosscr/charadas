import streamlit as st
import pandas as pd

def main():
    st.title("Juego de Charadas")

    # Create teams
    if "teams" not in st.session_state:
        st.session_state.teams = []

    st.header("Crear Equipos")
    num_teams = st.number_input("Número de equipos", min_value=2, value=2, step=1)

    if st.button("Crear Equipos"):
        st.session_state.teams = [f"Equipo {i+1}" for i in range(num_teams)]
        st.success("Equipos creados con éxito")

    st.header("Equipos")
    if st.session_state.teams:
        for team in st.session_state.teams:
            st.write(team)

    # Load words/phrases
    st.header("Cargar Palabras o Frases")
    uploaded_file = st.file_uploader("Sube un archivo CSV con palabras o frases", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if "words" in df.columns:
            st.session_state.words = df["words"].tolist()
            st.success("Palabras o frases cargadas con éxito")
        else:
            st.error("El archivo CSV debe contener una columna llamada 'words'")

    # Placeholder for further steps
    st.header("Configuraciones del Juego")
    # Load words/phrases, set timer, start game, etc. will go here

if __name__ == "__main__":
    main()
