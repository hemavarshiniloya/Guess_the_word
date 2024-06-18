import streamlit as st
import random

class WordGuessingApp:
    def __init__(self):
        self.words = ["Chiten", "nooter", "program", "gaming", "Zyzzyx", "Quirky", "Gizmoz", "Xyloid", "Jibber", "Krabby", "Zephyr", "Jigsaw", "Xanadu", "Glitch", "sujeto", "ostrea", "correa", "dinero", "pulgar", "moneda"]
        if 'game_state' not in st.session_state:
            self.reset_game()

    def reset_game(self):
        st.session_state.game_state = {
            'word': random.choice(self.words).lower(),
            'hint_index': 0,
            'hint_letter': '',
            'revealed_letters': [],
            'guessed_letters': set(),
            'attempts_left': random.randint(8, 10),
            'score': 0
        }
        st.session_state.game_state['hint_index'] = random.randint(0, len(st.session_state.game_state['word']) - 1)
        st.session_state.game_state['hint_letter'] = st.session_state.game_state['word'][st.session_state.game_state['hint_index']]
        st.session_state.game_state['revealed_letters'] = [
            '_' if i != st.session_state.game_state['hint_index'] else st.session_state.game_state['hint_letter'] 
            for i in range(len(st.session_state.game_state['word']))
        ]

    def guess_letter(self, guess):
        if guess == st.session_state.game_state['word']:
            st.session_state.game_state['score'] += 10
            st.success(f"Congratulations!. Your final score is {st.session_state.game_state['score']}.")
            self.show_word()
            self.reset_game()
        elif len(guess) == 1 and guess.isalpha():
            if guess in st.session_state.game_state['guessed_letters']:
                st.warning("You've already guessed that letter.")
            else:
                st.session_state.game_state['guessed_letters'].add(guess)
                if guess in st.session_state.game_state['word']:
                    st.session_state.game_state['score'] += 1
                    for i in range(len(st.session_state.game_state['word'])):
                        if st.session_state.game_state['word'][i] == guess:
                            st.session_state.game_state['revealed_letters'][i] = guess
                    st.success(f"Good guess! '{guess}' is in the word.")
                    if "_" not in st.session_state.game_state['revealed_letters']:
                        st.success(f"Congratulations! . Your final score is {st.session_state.game_state['score']}.")
                        self.show_word()
                        self.reset_game()
                else:
                    st.session_state.game_state['attempts_left'] -= 1
                    st.error(f"Oops! '{guess}' is not in the word.")
                    if st.session_state.game_state['attempts_left'] == 0:
                        st.error(f"Game over!. Your final score is {st.session_state.game_state['score']}.")
                        self.show_word()
                        self.reset_game()
        else:
            st.warning("Please enter a single letter or the entire word.")

    def show_word(self):
        st.info(f"The word was: {st.session_state.game_state['word']}")

    def display(self):
        st.title("Word Guessing Game")
        st.text(f"Word: {' '.join(st.session_state.game_state['revealed_letters'])}")
        st.text(f"Attempts left: {st.session_state.game_state['attempts_left']}")
        st.text(f"Score: {st.session_state.game_state['score']}")

        guess = st.text_input("Enter a letter or the whole word:")
        if st.button("Guess"):
            self.guess_letter(guess)

        if st.button("Show Score"):
            st.info(f"Your current score is: {st.session_state.game_state['score']}")

        if st.button("Reset Game"):
            self.reset_game()

if __name__ == "__main__":
    app = WordGuessingApp()
    app.display()
