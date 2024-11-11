"""Contains the main logic of our guessing game app."""

import streamlit as st
from pathlib import Path
from scipy.ndimage import uniform_filter
import yaml

st.title("Stats")

stream = open("app/guessing_config.yaml", 'r')
data = yaml.load(stream, Loader=yaml.Loader)
animals = data["animals"]
animals.insert(0, "All")
option = st.selectbox("Animals", animals)

if "game_history" in st.session_state and len(st.session_state.game_history) > 2:
    print(st.session_state.game_history)
    relevant_games = st.session_state.game_history[:-1]
    if option != "All":
        relevant_games = list(filter(lambda game: (game["animal"] == option), relevant_games))
    if len(relevant_games) > 0:
        print(relevant_games)
        st.bar_chart(data=relevant_games, x="animal", y="number_of_guesses", y_label="Number of guesses")
        guesses = [game["number_of_guesses"] for game in relevant_games]
        print(guesses)
        averages = uniform_filter(guesses, size=2, mode="nearest", output=float)
        print(averages)
        st.line_chart(averages)
    else:
        pass #Print text if no data available
