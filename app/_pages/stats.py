"""Contains the main logic of our guessing game app."""

import streamlit as st
import numpy as np
import altair as alt
import pandas as pd


def alt_chart(
    data: pd.DataFrame, x_title: str, y_var: str, y_title: str, tooltips: dict
) -> None:
    """Generate and display an Altair bar chart using the provided data and specifications.

    Args:
        data (pd.DataFrame): Data to be visualized.
        x_title (str): Title for the x-axis.
        y_var (str): Variable for the y-axis.
        y_title (str): Title for the y-axis.
        tooltips (dict): Dictionary containing the variables and their respective titles for tooltips.

    """
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("i:N", scale=alt.Scale(padding=0.1), title=x_title),
            y=alt.Y(y_var, title=y_title),
            tooltip=[alt.Tooltip(var, title=title) for var, title in tooltips.items()],
        )
    )
    st.altair_chart(chart, use_container_width=True)


def number_of_guesses(relevant_games: list) -> None:
    """Calculate and display the number of guesses made in the relevant games.

    Args:
        relevant_games (list): List of game dictionaries with the number of guesses.

    Returns:
        None

    """
    guesses = [game["number_of_guesses"] for game in relevant_games]
    average = np.average(guesses) if len(guesses) > 0 else np.nan

    st.header("Number of guesses", divider="gray")
    st.write(f"Average: {average}")
    st.subheader("Number of guesses per round:")

    data = pd.DataFrame(relevant_games)
    data["i"] = data.index + 1
    alt_chart(
        data=data,
        x_title="Round",
        y_var="number_of_guesses",
        y_title="Number of guesses and questions",
        tooltips={"animal": "animal", "number_of_guesses": "number of guesses"},
    )


def qualities_last_game(relevant_games: list) -> None:
    """Display the quality of guesses for the last game played.

    Args:
        relevant_games (list): List of game dictionaries with the quality of guesses.

    Returns:
        None

    """
    st.header("Your guesses' quality of the last game", divider="gray")
    st.write(f"Average: {np.average(relevant_games[-1]['quality_of_guesses']):.2f}")
    st.subheader("Quality per question/guess:")

    data = pd.DataFrame(
        {
            "quality": relevant_games[-1]["quality_of_guesses"],
            "chat": relevant_games[-1]["user_chat"],
        }
    )
    data["i"] = data.index + 1
    alt_chart(
        data=data,
        x_title="Number of Guess/Question",
        y_var="quality",
        y_title="Quality of guess/question",
        tooltips={"chat": "guess/question", "quality": "quality"},
    )


def qualities_per_game(relevant_games: list) -> None:
    """Display the average quality of guesses across all relevant games.

    Args:
        relevant_games (list): List of game dictionaries with the quality of guesses.

    Returns:
        None

    """
    avg_qualities = [
        {
            "animal": game["animal"],
            "quality": np.average(game["quality_of_guesses"]),
            "guesses": game["number_of_guesses"],
        }
        for game in relevant_games
    ]
    quality = np.concatenate([game["quality_of_guesses"] for game in relevant_games])

    st.header("Your guesses' quality overall", divider="gray")
    st.write(f"Average overall: {np.average(quality):.2f}")
    st.subheader("Average quality per round:")

    data = pd.DataFrame(avg_qualities)
    data["i"] = data.index + 1
    alt_chart(
        data=data,
        x_title="Round",
        y_var="quality",
        y_title="Average quality",
        tooltips={
            "animal": "animal",
            "quality": "average quality",
            "guesses": "number of guesses and questions",
        },
    )


def main():
    """Display the game statistics page.

    Displays the number of games played, the number of guesses, and the quality of
    guesses for the completed games.
    """
    st.title("Stats")
    if (
        not "game_history" in st.session_state
        or len(st.session_state.game_history) <= 1
    ):
        st.write("Finish a game first before you can see any stats.")
        return

    # check for which animal the stats should be calculated (or all)
    animals = list({game["animal"] for game in st.session_state.game_history[:-1]})
    animals.insert(0, "All")
    option = st.selectbox("Animals", animals)

    # filter the games of this animal (or all)
    relevant_games = st.session_state.game_history[:-1]
    if option != "All":
        relevant_games = list(
            filter(lambda game: (game["animal"] == option), relevant_games)
        )
    guesses = [game["number_of_guesses"] for game in relevant_games]
    average = np.average(guesses) if len(guesses) > 0 else np.nan

    # show stats
    st.metric("Total games played", len(relevant_games))
    if len(relevant_games) > 0:
        number_of_guesses(relevant_games)
        qualities_last_game(relevant_games)
        qualities_per_game(relevant_games)


main()
