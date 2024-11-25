"""Contains the main logic of our guessing game app."""

import streamlit as st
from scipy.ndimage import uniform_filter
import numpy as np
import yaml
import altair as alt
import pandas as pd

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
    print(relevant_games)

    st.caption(f"Total games played: {len(relevant_games)}")
    if len(relevant_games) > 0:
        st.caption(f"Average guesses: {average}")
        data = pd.DataFrame(relevant_games)
        data["i"] = data.index + 1
        chart = (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x=alt.X("i:N", scale=alt.Scale(padding=0.1), title="Round"),
                y=alt.Y("number_of_guesses", title="Number of guesses and questions"),
                tooltip=[
                    alt.Tooltip("animal", title="animal"),
                    alt.Tooltip("number_of_guesses", title="number of guesses"),
                ],
            )
        )
        # st.bar_chart(
        #    data=relevant_games,
        #    y="number_of_guesses",
        #    x_label="Round",
        #    y_label="Number of guesses and questions",
        # )
        st.altair_chart(chart, use_container_width=True)
        st.caption(
            f"Average quality (last game): {np.average(relevant_games[-1]["quality_of_guesses"])}"
        )
        data = pd.DataFrame(
            {
                "quality": relevant_games[-1]["quality_of_guesses"],
                "chat": relevant_games[-1]["user_chat"],
            }
        )
        data["i"] = data.index + 1
        chart = (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x=alt.X(
                    "i:N",
                    scale=alt.Scale(padding=0.1),
                    title="Number of Guess/Question",
                ),
                y=alt.Y("quality", title="Quality of guess/question"),
                tooltip=[
                    alt.Tooltip("chat", title="guess/question"),
                    alt.Tooltip("quality", title="quality"),
                ],
            )
        )
        st.altair_chart(chart, use_container_width=True)
        # st.bar_chart(
        #    data=data,
        #    x = "i",
        #    x_label="number of question/guess",
        #    y_label="quality of guess",
        # )

        avg_qualities = [
            {
                "animal": game["animal"],
                "quality": np.average(game["quality_of_guesses"]),
                "guesses": game["number_of_guesses"],
            }
            for game in relevant_games
        ]
        quality = np.concatenate(
            [game["quality_of_guesses"] for game in relevant_games]
        )
        st.caption(f"Average quality (overall): {np.average(quality)}")
        data = pd.DataFrame(avg_qualities)
        data["i"] = data.index + 1
        chart = (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x=alt.X("i:N", scale=alt.Scale(padding=0.1), title="Round"),
                y=alt.Y("quality", title="Average quality"),
                tooltip=[
                    alt.Tooltip("animal", title="animal"),
                    alt.Tooltip("quality", title="average quality"),
                    alt.Tooltip("guesses", title="number of guesses and questions"),
                ],
            )
        )
        st.altair_chart(chart, use_container_width=True)
        # st.bar_chart(
        #    data=avg_qualities,
        #    x_label="round",
        #    y_label="average quality of guess"
        # )
        # moving_averages = uniform_filter(guesses, size=5, mode="nearest", output=float)
        # print(guesses)
        # print(moving_averages)
        # st.line_chart(moving_averages)
