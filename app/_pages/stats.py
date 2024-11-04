"""Contains the main logic of our guessing game app."""

import streamlit as st

st.title("Stats")

if "game_history" in st.session_state and len(st.session_state.game_history) > 2:
    data = [game["number_of_guesses"] for game in st.session_state.game_history[:-1]]
    st.line_chart(data=data, y_label="Number of guesses")
