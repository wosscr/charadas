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
    if "game_active" not in st.session_state:
        st.session_state.game_active = False
    if "round_active" not in st.session_state:
        st.session_state.round_active = False
    if "all_results" not in st.session_state:
        st.session_state.all_results = []
    if "round_time" not in st.session_state:
        st.session_state.round_time = 0

    if st.button("Reiniciar"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()

    st.header("Crear Equipos")
    num_teams = st.number_input("Número de equipos", min_value=2, value=2, step=1, disabled=st.session_state.teams_configured if "teams_configured" in st.session_state else False)

    if st.button("Crear Equipos", disabled=st.session_state.teams_configured if "teams_configured" in st.session_state else False):
        st.session_state.teams = [f"Equipo {i+1}" for i in range(num_teams)]
        st.session_state.teams_configured = True
        st.success("Equipos creados con éxito")

    st.header("Equipos")
    if st.session_state.teams:
        for team in st.session_state.teams:
            st.write(team)

    # Load words/phrases
    st.header("Cargar Palabras o Frases")
    uploaded_file = st.file_uploader("Sube un archivo CSV con palabras o frases y categorías", type=["csv"], disabled=st.session_state.words_uploaded if "words_uploaded" in st.session_state else False)

    if uploaded_file is not None and not st.session_state.get("words_uploaded", False):
        df = pd.read_csv(uploaded_file)
        if "Palabra" in df.columns and "Categoria" in df.columns:
            st.session_state.words = df.to_dict('records')
            random.shuffle(st.session_state.words)  # Shuffle words
            st.session_state.words_uploaded = True
            st.success("Palabras o frases cargadas con éxito")
        else:
            st.error("El archivo CSV debe contener las columnas 'Palabra/Frase' y 'Categoria'")

    # Set timer
    st.header("Configuraciones del Juego")
    round_time = st.number_input("Tiempo por ronda (minutos)", min_value=1, value=1, step=1)
    st.session_state.round_time = round_time

    # Start game
    if st.button("Comenzar Juego", disabled=st.session_state.game_active or not (st.session_state.get("teams_configured", False) and st.session_state.get("words_uploaded", False))):
        st.session_state.current_word_index = 0
        st.session_state.results = []
        st.session_state.current_team = 0
        st.session_state.game_active = True
        st.session_state.round_active = True
        start_round()

    # Placeholder for further steps
    st.header("Juego en Progreso")
    if st.session_state.round_active and "current_word" in st.session_state:
        st.write(f"Equipo Actual: {st.session_state.teams[st.session_state.current_team]}")
        st.write(f"Palabra/Frase: {st.session_state.current_word['Palabra/Frase']} (Categoría: {st.session_state.current_word['Categoria']})")
        if st.button("Saltar"):
            st.session_state.results.append({"word": st.session_state.current_word['Palabra/Frase'], "result": "Saltar"})
            next_word()
        if st.button("Correcto"):
            st.session_state.results.append({"word": st.session_state.current_word['Palabra/Frase'], "result": "Correcto"})
            next_word()

        # Display the countdown timer using JavaScript
        st.write(f"<div id='timer'></div>", unsafe_allow_html=True)
        st.write(f"""
            <script>
                var timer = document.getElementById('timer');
                var timeLeft = {st.session_state.round_time * 60};

                function updateTimer() {{
                    var minutes = Math.floor(timeLeft / 60);
                    var seconds = timeLeft % 60;
                    timer.innerHTML = 'Tiempo restante: ' + minutes + ' minutos ' + seconds + ' segundos';
                    if (timeLeft > 0) {{
                        timeLeft--;
                        setTimeout(updateTimer, 1000);
                    }} else {{
                        timer.innerHTML = '¡Tiempo terminado!';
                        document.getElementById('endRound').click();
                    }}
                }}
                updateTimer();
            </script>
        """, unsafe_allow_html=True)

    # Button to end the round (hidden)
    st.button("End Round", key="endRound", on_click=end_round, args=(round_time,), disabled=not st.session_state.round_active, use_container_width=True)

    if not st.session_state.round_active and st.session_state.game_active and "current_word" in st.session_state:
        summarize_round()

    # Button to start the next team's round
    if not st.session_state.round_active and st.session_state.game_active and st.session_state.get("teams_configured", False) and st.session_state.get("words_uploaded", False):
        if st.session_state.current_team < len(st.session_state.teams) - 1:
            if st.button("Siguiente Equipo"):
                st.session_state.current_team += 1
                st.session_state.current_word_index = 0  # Reset word index for next team
                st.session_state.results = []  # Reset results for next team
                st.session_state.round_active = True
                start_round()
                st.experimental_rerun()  # Force rerun to update the state
        else:
            st.write("El juego ha terminado.")
            st.session_state.game_active = False
            display_final_summary()

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

def end_round(round_time):
    st.session_state.round_active = False
    st.session_state.all_results.append((st.session_state.teams[st.session_state.current_team], st.session_state.results))
    summarize_round()

def summarize_round():
    st.write("Resumen de la Ronda")
    for result in st.session_state.results:
        st.write(f"Palabra: {result['word']}, Resultado: {result['result']}")
    total_correct = sum(1 for result in st.session_state.results if result['result'] == "Correcto")
    st.write(f"Puntos Totales: {total_correct}")

def display_final_summary():
    st.write("Resumen Final del Juego")
    all_results = []
    for team, results in st.session_state.all_results:
        correct_words = [result['word'] for result in results if result['result'] == "Correcto"]
        skipped_words = [result['word'] for result in results if result['result'] == "Saltar"]
        all_results.append({"Equipo": team, "Correctas": len(correct_words), "Saltadas": len(skipped_words)})

    df = pd.DataFrame(all_results)
    st.table(df)

if __name__ == "__main__":
    main()
