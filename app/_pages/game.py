"""Contain the main logic of the animal guessing game app."""

import streamlit as st
import random
import yaml
from openai import OpenAI
from typing import List

st.title("Animal guessing game")


class Game:
    """Manage the animal guessing game.

    Set up the game, evaluate user input, and manage game state.
    """

    def __init__(self):
        """Initialize the game."""
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
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

    @st.cache_data
    def get_animals(_self) -> List[str]:
        """Read animals from yaml file.

        Returns:
            List[str]: animals

        """
        with open("app/guessing_config.yaml", "r") as stream:
            data = yaml.load(stream, Loader=yaml.Loader)
            return data["animals"]

    def random_animal(self) -> str:
        """Return a randomly selected animal from a predefined list.

        Returns:
            str: The name of the randomly chosen animal.

        """
        return random.choice(self.get_animals())

    def evaluate_input(self, guess):
        """Evaluate the player's guess against the selected animal.

        Update the game state based on whether the guess is correct or incorrect.
        """
        st.session_state.chat_history.append({"role": "user", "content": guess})
        with st.chat_message("user"):
            st.markdown(guess)
        st.session_state.game_history[-1]["number_of_guesses"] += 1

        with st.chat_message("assistant"):
            stream = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.chat_history,
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        self.get_quality_of_guess()
        if response == "Correct! You won.":
            st.session_state.state = "win"
            st.rerun()

    def get_quality_of_guess(self):
        """Calculate the quality of the last guess and add it to the history."""
        system_prompt = f"""In the context of an animal guessing game: Your job is to evaluate the quality of the user's last question from 0 (bad question) - 10 (good question). Keeping the history of this chat in mind and the knowledge the user has obtained before, a good question is a question that drastically decreases the number of remaining animals from the animals that are still possible. It does not matter if the answer would be yes or no but instead what fraction of remaining animals are ruled out. Similar to information gain. Please answer with the number only."""
        new_history = [
            {"role": "system", "content": system_prompt}
        ] + st.session_state.chat_history[1:-1]
        new_history += [
            {
                "role": "user",
                "content": f"The question to evaluate is: '{new_history[-1]["content"]}'. Please only answer with a number from 1-10.",
            }
        ]
        quality = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=new_history,
        )
        quality = quality.choices[0].message.content
        st.session_state.game_history[-1]["quality_of_guesses"].append(int(quality))

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
        return {"animal": animal, "number_of_guesses": 0, "quality_of_guesses": []}

    def initial_message(self) -> List[dict]:
        """Get initital message.

        Returns:
            dict: initial message that should be displayed at the top of the chat

        """
        return [
            {
                "role": "system",
                "content": f"You are a game master of an animal guessing game. The user asks questions. You answer with yes or no. The animal is '{st.session_state.animal}'. Never tell the name of the animal before the user guessed it! If you think the user is right answer 'Correct! You won.'",
            },
            {"role": "assistant", "content": "What is your first guess or question?"},
        ]

    def main(self):
        """Set up the game layout in the Streamlit app.

        Display instructions, an input box for guessing the animal,
        and the output message.
        """
        print(st.session_state["animal"])
        st.write("Your goal is to guess a randomly picked animal.")

        for message in st.session_state.chat_history:
            if message["role"] == "system":
                continue
            st.chat_message(message["role"]).write(message["content"])

        if guess := st.chat_input(
            "Enter animal or question:", disabled=(st.session_state.state == "win")
        ):
            self.evaluate_input(guess)
            st.write(
                f"Your last question/guess was of quality: {st.session_state.game_history[-1]["quality_of_guesses"][-1]}"
            )

        if st.session_state.state == "win":
            st.write(
                f"Your last question/guess was of quality: {st.session_state.game_history[-1]["quality_of_guesses"][-1]}"
            )
            st.button("Play again", on_click=self.reset_game)


# Instantiate and start the game
game = Game()
game.main()
