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
        if st.session_state["guess"] == st.session_state["animal"]:
            self.win()
        else:
            self.wrong()

    def win(self):
        """Update session state to indicate a winning guess."""
        st.session_state["state"] = "win"

    def wrong(self):
        """Update session state to indicate an incorrect guess."""
        st.session_state["state"] = "wrong_answer"

    def output(self):
        """Display a message based on the game state.

        Show a winning message if the guess is correct; otherwise, prompt the
        user to try again.
        """
        if "state" not in st.session_state:
            return
        if st.session_state["state"] == "win":
            st.write("YOU WON!!")
        elif st.session_state["state"] == "wrong_answer":
            st.write("Wrong answer :( try again)")

    def layout(self):
        """Set up the game layout in the Streamlit app.

        Display instructions, an input box for guessing the animal,
        and the output message.
        """
        st.write("Your goal is to guess a randomly picked animal.")
        st.text_input("Enter animal:", on_change=self.evaluate_input, key="guess")
        self.output()


# Instantiate and start the game
game = Game()
