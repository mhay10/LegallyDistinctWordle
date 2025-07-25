from collections import Counter
from guess import NUM_LETTERS
from constants import *


def score_guess(answer: str, guess: str):
    # Keep track of found letters in answer
    answer_counter = Counter(answer)
    colors = [None] * NUM_LETTERS

    # Mark all exact matches
    for i, letter in enumerate(guess):
        if letter == answer[i]:
            colors[i] = GREEN
            answer_counter[letter] -= 1

    # Mark rest of letters in word
    for i, letter in enumerate(guess):
        # Skip already matched colors
        if colors[i] == GREEN:
            continue

        if answer_counter[letter] > 0:
            colors[i] = YELLOW
            answer_counter[letter] -= 1
        else:
            colors[i] = LIGHT_GREY

    return colors
