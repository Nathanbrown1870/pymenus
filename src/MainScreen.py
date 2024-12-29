from typing import override
from src.screenBase import ScreenBase
from src.element_rootClass import TUIelement

class MainScreen(ScreenBase):
    def __init__(self, window, x_position=0, y_position=0):
        super().__init__(window,x_position, y_position)
        self.screen = window
        self.elments: list[TUIelement] = []
        self.is_screen: bool = True
        self.focusable: bool = False
        self.has_focus: bool = False

    def add_to_screen(self, screen):
        return super().add_to_screen(screen)

    @override
    def set_focus(self):
        pass

    @override
    def remove_focus(self):
        pass
    

