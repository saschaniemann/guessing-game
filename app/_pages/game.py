"""Contain the main logic of the animal guessing game app."""

import streamlit as st
import random
import yaml
from openai import OpenAI

st.title("Animal guessing game")

stream = open("app/guessing_config.yaml", 'r')
data = yaml.load(stream, Loader=yaml.Loader)
all_animals = data["animals"]

class Game:
    """Manage the animal guessing game.

    Set up the game, evaluate user input, and manage game state.
    """

    def __init__(self):
        self.client = OpenAI(api_key="")
        """Initialize the game."""
        if "animal" not in st.session_state:
            st.session_state["animal"] = self.random_animal()
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = self.initial_message()
        if "game_history" not in st.session_state:
            st.session_state["game_history"] = [
                self.empty_game(st.session_state.animal)
            ]
        if "state" not in st.session_state:
            st.session_state["state"] = "guessing"
        self.layout()

    def random_animal(self) -> str:
        """Return a randomly selected animal from a predefined list.

        Returns:
            str: The name of the randomly chosen animal.

        """
        return random.choice(all_animals)

    def evaluate_input(self):
        """Evaluate the player's guess against the selected animal.

        Update the game state based on whether the guess is correct or incorrect.
        """
        st.session_state.chat_history.append(
            {"role": "user", "content": st.session_state.guess}
        )
        st.session_state.game_history[-1]["number_of_guesses"] += 1
        if st.session_state.guess == st.session_state.animal:
            self.win()
        else:
            self.wrong()

    def win(self):
        """Update session state to indicate a winning guess."""
        st.session_state.chat_history.append(
            {"role": "assistant", "content": "Correct! You won."}
        )
        st.session_state.state = "win"

    def wrong(self):
        """Update session state to indicate an incorrect guess."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.chat_history
        )

        st.session_state.chat_history.append(
            {"role": "assistant", "content": response}
        )

    def reset_game(self):
        """Reset game and initialize all necessary variables."""
        st.session_state.animal = self.random_animal()
        st.session_state.game_history.append(self.empty_game(st.session_state.animal))
        st.session_state.chat_history = self.initial_message()
        st.session_state.state = "guessing"

    def empty_game(self, animal: str) -> dict:
        """Get a new game history entry.

        Args:
            animal (str): the new animal to guess

        Returns:
            dict: game history entry

        """
        return {"animal": animal, "number_of_guesses": 0}

    def initial_message(self) -> list[dict]:
        """Get initital message.

        Returns:
            dict: initial message that should be displayed at the top of the chat

        """

        return [{"role": "system", "content": f"You are a game master of an animal guessing game. The user asks questions. You answer with yes or no. The animal is '{st.session_state.animal}'."},
                {"role": "assistant", "content": "What is your first guess?"}]

    def layout(self):
        """Set up the game layout in the Streamlit app.

        Display instructions, an input box for guessing the animal,
        and the output message.
        """
        st.write("Your goal is to guess a randomly picked animal.")

        print(st.session_state.chat_history)
        for message in st.session_state.chat_history:
            print(message)
            st.chat_message(message["role"]).write(message["content"])

        st.chat_input(
            "Enter animal:",
            on_submit=self.evaluate_input,
            key="guess",
            disabled=(st.session_state.state == "win"),
        )
        if st.session_state.state == "win":
            st.button("Play again", on_click=self.reset_game)


# Instantiate and start the game
game = Game()
