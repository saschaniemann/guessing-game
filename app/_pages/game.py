"""Contain the main logic of the animal guessing game app."""

import streamlit as st
import random

st.title("Animal guessing game")


class Game:
    """Manage the animal guessing game.

    Set up the game, evaluate user input, and manage game state.
    """

    def __init__(self):
        """Initialize the game."""
        if "animal" not in st.session_state:
            st.session_state["animal"] = self.random_animal()
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = [
                {"role": "assistant", "content": "What is your first guess?"}
            ]
        self.layout()

    def random_animal(self) -> str:
        """Return a randomly selected animal from a predefined list.

        Returns:
            str: The name of the randomly chosen animal.

        """
        return random.choice(
            ["fox", "goose", "bear", "camel", "lama", "cow", "dog", "cat"]
        )

    def evaluate_input(self):
        """Evaluate the player's guess against the selected animal.

        Update the game state based on whether the guess is correct or incorrect.
        """
        st.session_state.chat_history.append(
            {"role": "user", "content": st.session_state["guess"]}
        )
        if st.session_state["guess"] == st.session_state["animal"]:
            self.win()
        else:
            self.wrong()

    def win(self):
        """Update session state to indicate a winning guess."""
        st.session_state.chat_history.append(
            {"role": "assistant", "content": "Correct! You won."}
        )

    def wrong(self):
        """Update session state to indicate an incorrect guess."""
        st.session_state.chat_history.append(
            {"role": "assistant", "content": "Wrong! Do you have another idea?"}
        )

    def layout(self):
        """Set up the game layout in the Streamlit app.

        Display instructions, an input box for guessing the animal,
        and the output message.
        """
        st.write("Your goal is to guess a randomly picked animal.")

        for message in st.session_state.chat_history:
            st.chat_message(message["role"]).write(message["content"])

        st.chat_input("Enter animal:", on_submit=self.evaluate_input, key="guess")


# Instantiate and start the game
game = Game()
