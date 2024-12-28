import curses

from src.widgets.widget_baseclass import Widget

class label(Widget):
    def __init__(self, text: str, x_position: int, y_position: int) -> None:
        super().__init__(x_position,y_position)
        self.text: str = text
    
    def add_to_screen(self, screen):
        screen.addstr(self.y_position,self.x_position,self.text)

    
    
def test():
    screen = curses.initscr()
    screen.addstr()