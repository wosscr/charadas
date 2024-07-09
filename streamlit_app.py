import streamlit as st
import pandas as pd
import random
import time

def main():
    st.title("Juego de Charadas")

    # Create teams
    if "teams" not in st.session_state:
        st.session_state.teams = []
    if "current_team" not in st.session_state:
        st.session_state.current_team = 0
    if "words" not in st.session_state:
        st.session_state.words = []
    if "current_word_index" not in st.session_state:
        st.session_state.current_word_index = 0
    if "results" not in st.session_state:
        st.session_state.results = []

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

    # Set timer
    st.header("Configuraciones del Juego")
    round_time = st.number_input("Tiempo por ronda (minutos)", min_value=1, value=1, step=1)

    # Start game
    if st.button("Comenzar Juego"):
        if not st.session_state.words:
            st.error("Debes cargar una lista de palabras o frases antes de comenzar el juego.")
        else:
            st.session_state.current_word_index = 0
            st.session_state.results = []
            st.session_state.current_team = 0
            start_round(round_time)

    # Placeholder for further steps
    st.header("Juego en Progreso")
    if "current_word" in st.session_state:
        st.write(f"Equipo Actual: {st.session_state.teams[st.session_state.current_team]}")
        st.write(f"Palabra: {st.session_state.current_word}")
        if st.button("Saltar"):
            st.session_state.results.append({"word": st.session_state.current_word, "result": "Saltar"})
            next_word()
        if st.button("Correcto"):
            st.session_state.results.append({"word": st.session_state.current_word, "result": "Correcto"})
            next_word()
        if st.session_state.current_word_index >= len(st.session_state.words):
            st.write("No quedan más palabras. Fin del juego.")

def start_round(round_time):
    st.session_state.current_word = st.session_state.words[st.session_state.current_word_index]
    end_time = time.time() + round_time * 60
    while time.time() < end_time:
        time_left = end_time - time.time()
        st.write(f"Tiempo restante: {int(time_left)} segundos")
        time.sleep(1)
    st.write("¡Tiempo terminado!")
    summarize_round()

def next_word():
    st.session_state.current_word_index += 1
    if st.session_state.current_word_index < len(st.session_state.words):
        st.session_state.current_word = st.session_state.words[st.session_state.current_word_index]
    else:
        st.write("No quedan más palabras. Fin del juego.")
        summarize_round()

def summarize_round():
    st.write("Resumen de la Ronda")
    for result in st.session_state.results:
        st.write(f"Palabra: {result['word']}, Resultado: {result['result']}")
    total_correct = sum(1 for result in st.session_state.results if result['result'] == "Correcto")
    st.write(f"Puntos Totales: {total_correct}")

if __name__ == "__main__":
    main()
