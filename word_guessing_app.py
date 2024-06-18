import streamlit as st
import random

class WordGuessingApp:
    def __init__(self):
        self.words = ["Chiten", "nooter", "program", "gaming", "Zyzzyx", "Quirky", "Gizmoz", "Xyloid", "Jibber", "Krabby", "Zephyr", "Jigsaw", "Xanadu", "Glitch", "sujeto", "ostrea", "correa", "dinero", "pulgar", "moneda"]
        self.definitions = {
            "chiten": ("A protective shell or exoskeleton", "The crab's chiten protects it from predators."),
            "nooter": ("A slang term for a noob or novice", "As a nooter, he needed help with the game."),
            "program": ("A set of instructions that a computer follows", "She wrote a program to automate the task."),
            "gaming": ("The action or practice of playing video games", "He spends hours gaming every day."),
            "zyzzyx": ("A rare or invented word often used in puzzles", "Zyzzyx is a tricky word in crossword puzzles."),
            "quirky": ("Characterized by peculiar or unexpected traits", "Her quirky personality made her stand out."),
            "gizmoz": ("A slang term for gadgets or devices", "He loves collecting the latest gizmoz."),
            "xyloid": ("Of or resembling wood", "The sculpture had a xyloid texture."),
            "jibber": ("To talk rapidly and unintelligibly", "The child began to jibber excitedly."),
            "krabby": ("Cranky or irritable", "He was feeling krabby after a long day."),
            "zephyr": ("A gentle, mild breeze", "A zephyr cooled the warm evening."),
            "jigsaw": ("A puzzle consisting of many pieces", "She completed the jigsaw puzzle in a day."),
            "xanadu": ("An idyllic, exotic, or luxurious place", "The resort was a real-life Xanadu."),
            "glitch": ("A sudden, usually temporary malfunction", "There was a glitch in the software."),
            "sujeto": ("Subject (Spanish: sujeto)", "The subject of the experiment was a volunteer. (Spanish: El sujeto del experimento era un voluntario.)"),
            "ostrea": ("Genus of oysters (Spanish: género de ostras)", "Ostrea is a genus comprising the true oysters. (Spanish: Ostrea es un género que comprende las verdaderas ostras.)"),
            "correa": ("Belt (Spanish: correa)", "The belt of my watch is broken. (Spanish: La correa de mi reloj está rota.)"),
            "dinero": ("Money (Spanish: dinero)", "I need money to buy food. (Spanish: Necesito dinero para comprar comida.)"),
            "pulgar": ("Thumb (Spanish: pulgar)", "The thumb is an important finger for gripping. (Spanish: El pulgar es un dedo importante para agarrar.)"),
            "moneda": ("Coin (Spanish: moneda)", "I found an old coin on the ground. (Spanish: Encontré una moneda antigua en el suelo.)")
        }
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
            st.success(f"Congratulations! You've guessed the word. Your final score is {st.session_state.game_state['score']}.")
            self.show_word()
            self.show_meaning(st.session_state.game_state['word'])
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
                        st.success(f"Congratulations! You've revealed the word. Your final score is {st.session_state.game_state['score']}.")
                        self.show_word()
                        self.show_meaning(st.session_state.game_state['word'])
                        self.reset_game()
                else:
                    st.session_state.game_state['attempts_left'] -= 1
                    st.error(f"Oops! '{guess}' is not in the word.")
                    if st.session_state.game_state['attempts_left'] == 0:
                        st.error(f"Game over!. Your final score is {st.session_state.game_state['score']}.")
                        self.show_word()
                        self.show_meaning(st.session_state.game_state['word'])
                        self.reset_game()
        else:
            st.warning("Please enter a single letter or the entire word.")

    def show_word(self):
        st.info(f"The word was: {st.session_state.game_state['word']}")

    def show_meaning(self, word):
        meaning, example = self.definitions.get(word, ("Meaning not found.", "No example available."))
        st.info(f"Meaning: {meaning}\nExample: {example}")

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
