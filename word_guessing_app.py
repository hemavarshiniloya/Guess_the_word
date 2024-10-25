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
        self.setup_game()

    def setup_game(self):
        if 'game_state' not in st.session_state:
            st.session_state['leaderboard'] = []
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
        word = st.session_state.game_state['word']
        st.session_state.game_state['hint_index'] = random.randint(0, len(word) - 1)
        st.session_state.game_state['hint_letter'] = word[st.session_state.game_state['hint_index']]
        st.session_state.game_state['revealed_letters'] = [
            '_' if i != st.session_state.game_state['hint_index'] else st.session_state.game_state['hint_letter'] 
            for i in range(len(word))
        ]

    def guess_letter(self, guess):
        state = st.session_state.game_state
        if guess == state['word']:
            state['score'] += 10
            self.game_won()
        elif len(guess) == 1 and guess.isalpha():
            if guess in state['guessed_letters']:
                st.warning("🚨 You've already guessed that letter.")
            else:
                state['guessed_letters'].add(guess)
                if guess in state['word']:
                    state['score'] += 1
                    for i, letter in enumerate(state['word']):
                        if letter == guess:
                            state['revealed_letters'][i] = guess
                    st.success(f"🎉 Good guess! '{guess}' is in the word.")
                    if "_" not in state['revealed_letters']:
                        self.game_won()
                else:
                    state['attempts_left'] -= 1
                    if state['attempts_left'] <= 2:
                        self.show_hint()
                    if state['attempts_left'] == 0:
                        self.game_lost()
                    else:
                        st.error(f"❌ Oops! '{guess}' is not in the word. Attempts left: {state['attempts_left']}")
        else:
            st.warning("⚠️ Please enter a single letter or the entire word.")

    def game_won(self):
        st.success(f"🏆 Congratulations! You've guessed the word '{st.session_state.game_state['word']}'. Your score is {st.session_state.game_state['score']}.")
        self.show_meaning(st.session_state.game_state['word'])
        self.update_leaderboard()
        self.reset_game()

    def game_lost(self):
        st.error(f"💔 Game over! The word was '{st.session_state.game_state['word']}'. Final score: {st.session_state.game_state['score']}.")
        self.show_meaning(st.session_state.game_state['word'])
        self.update_leaderboard()
        self.reset_game()

    def show_hint(self):
        hidden_indices = [i for i, letter in enumerate(st.session_state.game_state['revealed_letters']) if letter == '_']
        if hidden_indices:
            reveal_index = random.choice(hidden_indices)
            st.session_state.game_state['revealed_letters'][reveal_index] = st.session_state.game_state['word'][reveal_index]
            st.info(f"💡 Hint: Another letter revealed - {st.session_state.game_state['word'][reveal_index]}")

    def show_meaning(self, word):
        meaning, example = self.definitions.get(word, ("Meaning not found.", "No example available."))
        st.info(f"📖 Meaning: {meaning}\n💬 Example: {example}")

    def update_leaderboard(self):
        leaderboard = st.session_state['leaderboard']
        leaderboard.append((st.session_state.game_state['score'], st.session_state.game_state['word']))
        leaderboard.sort(reverse=True, key=lambda x: x[0])
        st.session_state['leaderboard'] = leaderboard[:5]  # Keep top 5 scores

    def display_leaderboard(self):
        st.subheader("🏅 Leaderboard")
        for i, (score, word) in enumerate(st.session_state['leaderboard'], 1):
            st.text(f"{i}. Word: {word} - Score: {score}")

    def display(self):
        st.title("🎲 Word Guessing Game")
        st.text(f"🔠 Word: {' '.join(st.session_state.game_state['revealed_letters'])}")
        st.text(f"💥 Attempts left: {st.session_state.game_state['attempts_left']}")
        st.text(f"⭐ Score: {st.session_state.game_state['score']}")

        guess = st.text_input("🔍 Enter a letter or the whole word:")
        if st.button("🎯 Guess"):
            self.guess_letter(guess.lower())

        if st.button("🏆 Show Leaderboard"):
            self.display_leaderboard()

        if st.button("🔄 Reset Game"):
            self.reset_game()

if __name__ == "__main__":
    app = WordGuessingApp()
    app.display()
