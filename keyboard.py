from constants import *
import pygame


class OnScreenKeyboard:
    def __init__(self):
        self.keyboard_font = pygame.font.SysFont(None, size=26)
        self.keys: list[list[KeyButton]] = [
            [],  # Row 1
            [],  # Row 2
            [],  # Row 3
        ]
        self._create_keyboard()

    def _create_keyboard(self):
        # Calculate starting position for keys
        start_x = (SCREEN_WIDTH - KEYBOARD_WIDTH) // 2
        start_y = BOARD_START_Y + BOARD_HEIGHT

        # Create each row of keyboard
        for i, row in enumerate(KEYBOARD_ROWS):
            # Add corresponding offsets for each row
            x_offset = KEYROW_OFFSETS[i]
            y_offset = (KEYBUTTON_HEIGHT + KEYBUTTON_PADDING) * i

            # Add keys to keyboard
            for letter in row:
                key = KeyButton(
                    letter,
                    x=start_x + x_offset,
                    y=start_y + y_offset,
                    font=self.keyboard_font,
                )
                self.keys[i].append(key)

                # Update offset for next key
                x_offset += KEYBUTTON_WIDTH + KEYBUTTON_PADDING

    def color_letter(self, letter: str, color: tuple[int, int, int]):
        # Find matching key based on letter
        key = None
        for row in self.keys:
            key = next((k for k in row if k.letter == letter), None)
            if key is not None:
                break

        # Throw error if key isn't found
        if key is None:
            raise RuntimeError(f"Invalid letter in keyboard: {letter}")

        # Update key's color
        key.color = color

    def draw(self, screen: pygame.Surface):
        for row in self.keys:
            for key in row:
                key.draw(screen)


class KeyButton:
    def __init__(self, letter: str, x: int, y: int, font: pygame.Font):
        self.letter = letter
        self.rect = pygame.Rect(x, y, KEYBUTTON_WIDTH, KEYBUTTON_HEIGHT)
        self.color = LIGHT_GREY
        self.text = font.render(letter.upper(), True, WHITE)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=3)
        screen.blit(
            self.text,
            (
                self.rect.x + (self.rect.width - self.text.width) // 2,
                self.rect.y
                + KEYBUTTON_TEXTPADDING
                + (self.rect.height - self.text.height) // 2,
            ),
        )
