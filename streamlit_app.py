import streamlit as st
import pandas as pd
import random
import time

def main():
    st.title("Juego de Charadas")

    # Initialize session state variables
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
    if "timer_end" not in st.session_state:
        st.session_state.timer_end = None
    if "game_active" not in st.session_state:
        st.session_state.game_active = False
    if "time_left" not in st.session_state:
        st.session_state.time_left = 0
    if "teams_configured" not in st.session_state:
        st.session_state.teams_configured = False
    if "words_uploaded" not in st.session_state:
        st.session_state.words_uploaded = False
    if "current_word" not in st.session_state:
        st.session_state.current_word = ""
    if "round_active" not in st.session_state:
        st.session_state.round_active = False

    if st.button("Reiniciar"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()

    st.header("Crear Equipos")
    num_teams = st.number_input("Número de equipos", min_value=2, value=2, step=1, disabled=st.session_state.teams_configured)

    if st.button("Crear Equipos", disabled=st.session_state.teams_configured):
        st.session_state.teams = [f"Equipo {i+1}" for i in range(num_teams)]
        st.session_state.teams_configured = True
        st.success("Equipos creados con éxito")

    st.header("Equipos")
    if st.session_state.teams:
        for team in st.session_state.teams:
            st.write(team)

    # Load words/phrases
    st.header("Cargar Palabras o Frases")
    uploaded_file = st.file_uploader("Sube un archivo CSV con palabras o frases", type=["csv"], disabled=st.session_state.words_uploaded)

    if uploaded_file is not None and not st.session_state.words_uploaded:
        df = pd.read_csv(uploaded_file)
        if "words" in df.columns:
            st.session_state.words = df["words"].tolist()
            random.shuffle(st.session_state.words)  # Shuffle words
            st.session_state.words_uploaded = True
            st.success("Palabras o frases cargadas con éxito")
        else:
            st.error("El archivo CSV debe contener una columna llamada 'words'")

    # Set timer
    st.header("Configuraciones del Juego")
    round_time = st.number_input("Tiempo por ronda (minutos)", min_value=1, value=1, step=1)

    # Start game
    if st.button("Comenzar Juego", disabled=st.session_state.game_active or not (st.session_state.teams_configured and st.session_state.words_uploaded)):
        st.session_state.current_word_index = 0
        st.session_state.results = []
        st.session_state.current_team = 0
        st.session_state.timer_end = time.time() + round_time * 60
        st.session_state.time_left = round_time * 60
        st.session_state.game_active = True
        st.session_state.round_active = True
        start_round()

    # Placeholder for further steps
    st.header("Juego en Progreso")
    if st.session_state.round_active and "current_word" in st.session_state:
        st.write(f"Equipo Actual: {st.session_state.teams[st.session_state.current_team]}")
        st.write(f"Palabra: {st.session_state.current_word}")
        if st.button("Saltar"):
            st.session_state.results.append({"word": st.session_state.current_word, "result": "Saltar"})
            next_word()
        if st.button("Correcto"):
            st.session_state.results.append({"word": st.session_state.current_word, "result": "Correcto"})
            next_word()

        # Display the countdown timer
        if st.session_state.timer_end:
            st.session_state.time_left = int(st.session_state.timer_end - time.time())
            st.write(f"Tiempo restante: {st.session_state.time_left} segundos")
            if st.session_state.time_left > 0:
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.write("¡Tiempo terminado!")
                st.session_state.round_active = False
                summarize_round()

    if not st.session_state.round_active and st.session_state.game_active and "current_word" in st.session_state:
        summarize_round()

    # Button to start the next team's round
    if not st.session_state.round_active and st.session_state.game_active and st.session_state.teams_configured and st.session_state.words_uploaded:
        if st.session_state.current_team < len(st.session_state.teams) - 1:
            if st.button("Siguiente Equipo"):
                st.session_state.current_team += 1
                st.session_state.timer_end = time.time() + round_time * 60
                st.session_state.time_left = round_time * 60
                st.session_state.round_active = True
                start_round()
        else:
            st.write("El juego ha terminado.")
            st.session_state.game_active = False

def start_round():
    if st.session_state.current_word_index < len(st.session_state.words):
        st.session_state.current_word = st.session_state.words[st.session_state.current_word_index]
    else:
        st.session_state.round_active = False
        summarize_round()

def next_word():
    st.session_state.current_word_index += 1
    if st.session_state.current_word_index < len(st.session_state.words):
        st.session_state.current_word = st.session_state.words[st.session_state.current_word_index]
    else:
        st.session_state.round_active = False
        summarize_round()

def summarize_round():
    st.write("Resumen de la Ronda")
    for result in st.session_state.results:
        st.write(f"Palabra: {result['word']}, Resultado: {result['result']}")
    total_correct = sum(1 for result in st.session_state.results if result['result'] == "Correcto")
    st.write(f"Puntos Totales: {total_correct}")

if __name__ == "__main__":
    main()
