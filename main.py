from popups import PopupManager
from guess import Guess
from constants import *
from keyboard import *
from keys import *
import pygame_gui
import pygame
import random
import wordle


class Game:
    def __init__(self):
        self._init_pygame()
        self._init_game_resources()
        self._init_game_state()
        self._init_popups()
        self._init_ui_elements()

    def _init_pygame(self):
        # Create window
        pygame.init()
        app_icon = pygame.image.load("app_icon.png")
        pygame.display.set_icon(app_icon)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Legally Distinct Wordle")

        # Create clock and UI manager
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Load UI themes
        self.manager.get_theme().load_theme("themes/main_theme.json")
        self.manager.get_theme().load_theme("themes/popup_theme.json")

    def _init_game_resources(self):
        # Load wordlists
        self.guesswords = self.load_wordlist("wordlists/valid-words.txt")
        self.wordbank = self.load_wordlist("wordlists/word-bank.txt")

        # Create fonts
        self.board_font = pygame.font.SysFont(None, size=50)
        self.lg_title_font = pygame.font.SysFont(None, size=80)
        self.sm_title_font = pygame.font.SysFont(None, size=22)

    def _init_game_state(self):
        # Game Variables
        self.answer = random.choice(self.wordbank)
        self.game_over = False
        self.done = False

        # Guess Variables
        self.num_guesses = 0
        self.guesses = [Guess() for _ in range(MAX_GUESSES)]
        self.current_guess = self.guesses[self.num_guesses]
        self.guess_colors = [
            [DARK_GREY for _ in range(NUM_LETTERS)] for _ in range(MAX_GUESSES)
        ]

        # Keyboard Variables
        self.ui_keyboard = OnScreenKeyboard()

    def _init_popups(self):
        self.popup_mgr = PopupManager(self.screen, self.manager, self.answer)

    def _init_ui_elements(self):
        self.reset_button = pygame_gui.elements.UIButton(
            manager=self.manager,
            text="New Game",
            relative_rect=pygame.Rect(
                0,
                SCREEN_HEIGHT - RESET_BUTTON_HEIGHT - RESET_BUTTON_PADDING,
                RESET_BUTTON_WIDTH,
                RESET_BUTTON_HEIGHT,
            ),
            anchors={"centerx": "centerx"},
        )
        self.reset_button.bind(pygame_gui.UI_BUTTON_PRESSED, self.new_game)

    def new_game(self):
        # Reset game state
        self._init_game_state()
        self._init_popups()

    def load_wordlist(self, file: str):
        results = []
        with open(file, "r") as f:
            for word in f:
                results.append(word.strip())

        return results

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            # Only type if popup not shown
            elif event.type == pygame.KEYDOWN:
                # Handle keys depending on visibility of popups
                if not self.popup_mgr.popup_open() and not self.game_over:
                    if event.key in ALPHABET_KEYS:
                        letter = ALPHABET_KEYS[event.key]
                        self.current_guess.add_letter(letter)

                    elif event.key == pygame.K_BACKSPACE:
                        self.current_guess.del_letter()

                    elif event.key == pygame.K_RETURN:
                        self.submit_guess()
                else:
                    if event.key in POPUP_CONFIRM_KEYS:
                        self.popup_mgr.close_all()

            self.manager.process_events(event)

    def submit_guess(self):
        guess = self.current_guess.get_word()
        if not self.current_guess.is_full():
            self.popup_mgr.show_incomplete_guess()
        elif guess not in self.guesswords:
            self.popup_mgr.show_invalid_guess()
        else:
            # Score and set colors of row
            colors = wordle.score_guess(self.answer, guess)
            for i, color in enumerate(colors):
                self.guess_colors[self.num_guesses][i] = color
                self.ui_keyboard.color_letter(
                    letter=guess[i], color=color if color != LIGHT_GREY else DARK_GREY
                )

            # Show popup if correct answer
            self.num_guesses += 1
            if guess == self.answer:
                self.popup_mgr.show_correct_guess(self.num_guesses, MAX_GUESSES)
                self.game_over = True
            elif self.num_guesses == MAX_GUESSES:
                self.popup_mgr.show_out_of_guesses()
                self.game_over = True
            else:
                # Goto next guess
                self.current_guess = self.guesses[self.num_guesses]

    def run(self):
        while not self.done:
            # Handle game events
            self.handle_events()

            # Update UI elements
            self.manager.update(self.clock.get_fps() / 1000)

            # Draw objects on screen
            self.screen.fill(BLACK)
            self.draw_title()
            self.draw_board()
            self.highlight_active_row()
            self.ui_keyboard.draw(self.screen)
            self.manager.draw_ui(self.screen)

            print(self.clock.get_fps())

            # Update screen
            pygame.display.update()
            self.clock.tick(FPS)

    def draw_board(self):
        # Draw colored boxes
        start_x = (SCREEN_WIDTH - BOARD_WIDTH) // 2
        for y, guess in enumerate(self.guesses):
            for x, letter in enumerate(guess.get_word()):
                # Draw background cell
                cell_rect = pygame.Rect(
                    start_x + x * CELL_SIZE + CELL_PADDING,
                    BOARD_START_Y + y * CELL_SIZE + CELL_PADDING,
                    CELL_SIZE - CELL_PADDING,
                    CELL_SIZE - CELL_PADDING,
                )
                cell_color = self.guess_colors[y][x]
                pygame.draw.rect(self.screen, cell_color, cell_rect)

                # Draw letter
                text = self.board_font.render(letter.upper(), True, WHITE)
                self.screen.blit(
                    text,
                    (
                        cell_rect.x + (cell_rect.width - text.get_width()) // 2,
                        cell_rect.y
                        + TEXT_PADDING_Y
                        + (cell_rect.height - text.get_height()) // 2,
                    ),
                )

    def highlight_active_row(self):
        if self.num_guesses < MAX_GUESSES:
            # Draw line under active row
            start_x = (SCREEN_WIDTH - BOARD_WIDTH) // 2
            pygame.draw.line(
                self.screen,
                LIGHT_GREY,
                (
                    start_x + CELL_PADDING,
                    BOARD_START_Y + CELL_SIZE + self.num_guesses * CELL_SIZE - 1,
                ),
                (
                    start_x + (CELL_SIZE * NUM_LETTERS) - 1,
                    BOARD_START_Y + CELL_SIZE + self.num_guesses * CELL_SIZE - 1,
                ),
                width=2,
            )

    def draw_title(self):
        # Draw title
        text = self.sm_title_font.render("LEGALLY DISTINCT", True, WHITE)
        self.screen.blit(text, ((SCREEN_WIDTH - text.get_width()) / 2, 15))
        text = self.lg_title_font.render("WORDLE", True, WHITE)
        self.screen.blit(text, ((SCREEN_WIDTH - text.get_width()) / 2, 32))


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
