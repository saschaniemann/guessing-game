"""Contains the main logic of our guessing game app."""

import streamlit as st
from scipy.ndimage import uniform_filter
import numpy as np
import yaml

st.title("Stats")

stream = open("app/guessing_config.yaml", "r")
data = yaml.load(stream, Loader=yaml.Loader)
animals = data["animals"]
animals.insert(0, "All")
option = st.selectbox("Animals", animals)

if "game_history" in st.session_state and len(st.session_state.game_history) > 0:
    relevant_games = st.session_state.game_history[:-1]
    if option != "All":
        relevant_games = list(
            filter(lambda game: (game["animal"] == option), relevant_games)
        )
    guesses = [game["number_of_guesses"] for game in relevant_games]
    average = np.average(guesses) if len(guesses) > 0 else np.nan

    st.caption(f"Total games played: {len(relevant_games)}")
    st.caption(f"Average guesses: {average}")
    if len(relevant_games) > 0:
        st.bar_chart(
            data=relevant_games,
            x="animal",
            y="number_of_guesses",
            y_label="Number of guesses",
        )
        moving_averages = uniform_filter(guesses, size=5, mode="nearest", output=float)
        print(guesses)
        print(moving_averages)
        st.line_chart(moving_averages)
