from constants import NUM_LETTERS


class Guess:
    def __init__(self):
        self.guess = [" " for _ in range(NUM_LETTERS)]
        self.current_letter = 0

    def add_letter(self, letter: str):
        if self.current_letter < NUM_LETTERS:
            self.guess[self.current_letter] = letter
            self.current_letter += 1

    def del_letter(self):
        if self.current_letter > 0:
            self.current_letter -= 1
            self.guess[self.current_letter] = " "

    def is_full(self):
        return self.current_letter == NUM_LETTERS

    def get_word(self):
        return "".join(self.guess)
