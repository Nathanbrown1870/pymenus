from typing import override
from src.element_rootClass import TUIelement
import curses

class ScreenBase(TUIelement):
    def __init__(self, window, x_position, y_position):
        super().__init__(x_position, y_position)
        self.screen: curses.window = window
        self.elments: list[TUIelement] = []
        self.is_screen: bool = True
        self.focusable: bool = False
        self.has_focus: bool = False

    def add_text(self, text: str):
        self.screen.addstr(0, 0, text)
    
