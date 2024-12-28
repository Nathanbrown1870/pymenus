import time
import curses
from src.element_rootClass import TUIelement

class ScreenManager:
    
    def __init__(self) -> None:
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.tui_manager: list[TUIelement] = []

    def add(self,element: TUIelement):
        self.tui_manager.append(element)

    def start(self):

        # clear the screen
        self.stdscr.clear()

        # load the elements
        for elements in self.tui_manager:
            elements.add_to_screen(self.stdscr)

        # capture input
        self.stdscr.get_wch()
        # time.sleep(5)

        # Refresh elements

    def __del__(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()