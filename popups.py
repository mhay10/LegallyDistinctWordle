from pygame_gui.elements import *
from constants import *
import pygame_gui
import pygame


class PopupManager:
    def __init__(
        self, screen: pygame.Surface, manager: pygame_gui.UIManager, answer: str
    ):
        self.screen = screen
        self.manager = manager
        self.answer = answer

        self.incomplete_guess_popup = PopupGuessIncomplete(screen, manager)
        self.invalid_guess_popup = PopupGuessInvalidWord(screen, manager)
        self.correct_guess_popup = PopupGuessCorrectAnswer(screen, manager)
        self.out_of_guesses_popup = PopupGuessRanOut(screen, manager, answer)
        self.popups = [
            self.incomplete_guess_popup,
            self.invalid_guess_popup,
            self.correct_guess_popup,
            self.out_of_guesses_popup,
        ]

    def popup_open(self):
        return any(popup.visible for popup in self.popups)

    def close_all(self):
        for popup in self.popups:
            popup.hide()

    def show_incomplete_guess(self):
        self.incomplete_guess_popup.show_popup()

    def show_invalid_guess(self):
        self.invalid_guess_popup.show_popup()

    def show_correct_guess(self, num_guesses: int, max_guesses: int):
        self.correct_guess_popup.show_popup(num_guesses, max_guesses)

    def show_out_of_guesses(self):
        self.out_of_guesses_popup.show_popup()


class PopupWindow(UIWindow):
    def __init__(
        self,
        screen: pygame.Surface,
        manager: pygame_gui.UIManager,
        msg_text: str,
        btn_text: str,
    ):
        # Initalize window
        super().__init__(
            manager=manager,
            window_display_title="  ALERT",
            rect=pygame.Rect(
                (screen.width - POPUP_WIDTH) / 2,
                (screen.height - POPUP_HEIGHT) / 2,
                POPUP_WIDTH,
                POPUP_HEIGHT,
            ),
            resizable=False,
            visible=False,
        )

        # Set error message
        self.err_msg = UITextBox(
            manager=manager,
            container=self,
            html_text=msg_text,
            relative_rect=pygame.Rect(0, 0, MESSAGE_WIDTH, MESSAGE_HEIGHT),
            anchors={"centerx": "centerx"},
        )

        self.dismiss = UIButton(
            manager=manager,
            container=self,
            text=btn_text,
            relative_rect=pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT),
            anchors={"centerx": "centerx", "top_target": self.err_msg},
        )
        self.dismiss.bind(pygame_gui.UI_BUTTON_PRESSED, self.hide)

    def show_popup(self):
        self.show()


class PopupGuessIncomplete(PopupWindow):
    def __init__(self, screen: pygame.Surface, manager: pygame_gui.UIManager):
        super().__init__(
            screen,
            manager,
            msg_text="Incomplete Guess\nPlease try again",
            btn_text="OK",
        )


class PopupGuessInvalidWord(PopupWindow):
    def __init__(self, screen: pygame.Surface, manager: pygame_gui.UIManager):
        super().__init__(
            screen,
            manager,
            msg_text="Invalid Word\nPlease try again",
            btn_text="OK",
        )


class PopupGuessCorrectAnswer(PopupWindow):
    def __init__(
        self,
        screen: pygame.Surface,
        manager: pygame_gui.UIManager,
    ):
        super().__init__(
            screen,
            manager,
            msg_text=f"",
            btn_text="OK",
        )

    def show_popup(self, num_guesses: int, max_guesses: int):
        self.err_msg.set_text(
            f"Congratulations!\n{num_guesses}/{max_guesses} used to answer"
        )
        self.show()


class PopupGuessRanOut(PopupWindow):
    def __init__(
        self, screen: pygame.Surface, manager: pygame_gui.UIManager, answer: str
    ):
        super().__init__(
            screen,
            manager,
            msg_text=f"Out of Guesses\nThe answer was: {answer.upper()}",
            btn_text="OK",
        )
