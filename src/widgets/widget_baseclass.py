import curses

from src.element_rootClass import TUIelement

class Widget(TUIelement):
    def __init__(self,x_position: int, y_position: int) -> None:
        super().__init__(x_position,y_position)
