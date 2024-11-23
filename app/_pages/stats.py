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
    quality = (
        np.concatenate([game["quality_of_guesses"] for game in relevant_games])
        if len(relevant_games) > 1
        else [game["quality_of_guesses"] for game in relevant_games]
    )
    avg_quality = np.average(quality) if len(quality) > 0 else np.nan

    st.caption(f"Total games played: {len(relevant_games)}")
    if len(relevant_games) > 0:
        st.caption(f"Average guesses: {average}")
        st.bar_chart(
            data=relevant_games,
            y="number_of_guesses",
            x_label="Round",
            y_label="Number of guesses and questions",
        )
        st.caption(
            f"Average quality (last game): {np.average(relevant_games[-1]["quality_of_guesses"])}"
        )
        st.bar_chart(
            data=relevant_games[-1]["quality_of_guesses"],
            x_label="number of question/guess",
            y_label="quality of guess",
        )
    if len((relevant_games)) > 1:
        st.caption(f"Average quality (overall): {avg_quality}")
        st.line_chart(
            data=quality, x_label="number of question/guess", y_label="quality of guess"
        )
        # moving_averages = uniform_filter(guesses, size=5, mode="nearest", output=float)
        # print(guesses)
        # print(moving_averages)
        # st.line_chart(moving_averages)
