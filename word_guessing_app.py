import tkinter as tk
from tkinter import ttk, messagebox
import random

class WordGuessingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Word Guessing Game")
        self.master.configure(bg="lightblue")  # Set background color to light blue

        self.words = ["Chiten", "nooter", "program", "gaming", "Zyzzyx", "Quirky", "Gizmoz", "Xyloid", "Jibber", "Krabby", "Zephyr", "Jigsaw", "Xanadu", "Glitch"]
        self.reset_game()
        self.create_widgets()

    def reset_game(self):
        self.word = random.choice(self.words).lower()
        self.hint_index = random.randint(0, len(self.word) - 1)
        self.hint_letter = self.word[self.hint_index]
        self.revealed_letters = ['_' if i != self.hint_index else self.hint_letter for i in range(len(self.word))]
        self.guessed_letters = set()
        self.attempts_left = random.randint(8, 10)
        self.score = 0

    def create_widgets(self):
        self.word_label = ttk.Label(self.master, text=" ".join(self.revealed_letters), font=("Arial", 18), background="lightblue")
        self.word_label.pack(pady=10)

        self.guess_entry = ttk.Entry(self.master, font=("Arial", 14))
        self.guess_entry.pack(pady=5)

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 14))  # Set the font for all ttk buttons

        self.guess_button = ttk.Button(self.master, text="Guess", command=self.guess_letter, style='TButton')
        self.guess_button.pack(pady=5)

        self.score_button = ttk.Button(self.master, text="Show Score", command=self.show_score, style='TButton')
        self.score_button.pack(pady=5)

        self.quit_button = ttk.Button(self.master, text="Quit", command=self.quit_game, style='TButton')
        self.quit_button.pack(pady=5)

        self.attempts_label = ttk.Label(self.master, text=f"Attempts left: {self.attempts_left}", font=("Arial", 14), background="lightblue")
        self.attempts_label.pack(pady=5)

        self.score_label = ttk.Label(self.master, text=f"Score: {self.score}", font=("Arial", 14), background="lightblue")
        self.score_label.pack(pady=5)

    def guess_letter(self):
        guess = self.guess_entry.get().lower()

        if guess == self.word:
            self.score += 10
            self.show_message(f"Congratulations! You've guessed the word '{self.word}'. Your final score is {self.score}.")
            self.quit_game()
        elif len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters:
                self.show_message("You've already guessed that letter.")
            else:
                self.guessed_letters.add(guess)
                if guess in self.word:
                    self.score += 1
                    for i in range(len(self.word)):
                        if self.word[i] == guess:
                            self.revealed_letters[i] = guess
                    self.update_display()
                    self.show_message(f"Good guess! '{guess}' is in the word.")
                    if "_" not in self.revealed_letters:
                        self.show_message(f"Congratulations! You've guessed the word '{self.word}'. Your final score is {self.score}.")
                        self.quit_game()
                else:
                    self.attempts_left -= 1
                    self.update_display()
                    self.show_message(f"Oops! '{guess}' is not in the word.")
                    if self.attempts_left == 0:
                        self.show_message(f"Game over! The word was '{self.word}'. Your final score is {self.score}.")
                        self.quit_game()
        else:
            self.show_message("Please enter a single letter or the entire word.")

    def update_display(self):
        self.word_label.config(text=" ".join(self.revealed_letters))
        self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
        self.score_label.config(text=f"Score: {self.score}")
        if self.attempts_left == 0:
            self.word_label.configure(background="red")  # Incorrect guess
        elif "_" not in self.revealed_letters:
            self.word_label.configure(background="green")  # Correct guess
        else:
            self.word_label.configure(background="lightblue")  # Reset to default background

    def show_message(self, message):
        messagebox.showinfo("Word Guessing Game", message)

    def quit_game(self):
        # Quit the application
        self.master.quit()

    def show_score(self):
        self.show_message(f"Your current score is: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WordGuessingApp(root)
    root.mainloop()
