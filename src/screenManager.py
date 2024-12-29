import curses.panel
import time
import curses
import sys

import logging
logger = logging.getLogger(__name__)

from src.MainScreen import MainScreen
from src.screenBase import ScreenBase as Screen
from src.element_rootClass import TUIelement

class ScreenManager:
    
    def __init__(self) -> None:
        self.mainScreen = MainScreen(window=curses.initscr())
        self.stdscr = self.mainScreen.screen
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self.stdscr.keypad(True)
        self.cursor = self.Cursor()
        
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()
        # Panels might make me tracking the level of the screen stack irrelevent 
        self.stack = [self.mainScreen]

    def add(self,element: TUIelement):
        self.mainScreen.elments.append(element)

    def start(self):

        # clear the screen
        while True:
            self.stdscr.erase()

            # Load screen elements
            self.screen_height, self.screen_width = self.stdscr.getmaxyx()

            # Calculate the height of the shorter box
            box_height = self.screen_height - 2  # 2 rows shorter at the top and bottom
            box_width = self.screen_width - 2  # Slightly narrower for aesthetics
            start_y = 1 
            start_x = 1 
            win = curses.newwin(box_height, box_width, start_y, start_x)
            win.box()
            win.addstr(1, 1, "This is a smaller box!")
            panel = curses.panel.new_panel(win)
            panel.bottom()

            # load the elements
            for element in self.mainScreen.elments:
                element.add_to_screen(self.stdscr)
                
                if element not in self.stack and element.is_screen:
                    self.stack.append(element)

            # Refresh elements
            curses.panel.update_panels(); 
            self.stdscr.refresh()

            # capture input
            last_y, last_x = self.stdscr.getyx()
            self.stdscr.move(self.cursor.row,self.cursor.col)
            self.handle_input(self.mainScreen)
            # time.sleep(5)


    def __del__(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def handle_input(self, screen: Screen):

        height, width = screen.screen.getmaxyx()

        # This is basically navigation mode
        k = screen.screen.getkey()
        if k == "q":
            sys.exit(0)
        elif k == "KEY_UP" or k == "k":
            self.cursor.up()
        elif k == "KEY_DOWN" or k == "j":
            self.cursor.down(height)
        elif k == "KEY_LEFT" or k == "h":
            self.cursor.left()
        elif k == "KEY_RIGHT"or k == "l":
            self.cursor.right(width)
        elif k == "\n":
            self.cursor.right(width)
        elif k == '\t':
            self.cursor.jump_to_next(screen.elments)
        elif k == "KEY_RESIZE":
            screen_height, screen_width = self.stdscr.getmaxyx()
        else:
            logger.debug(k)


    class Cursor:
        def __init__(self, row=0, col=0):
            self.row = row
            self.col = col
            
        def up(self):
            if self.row > 0:
                self.row -= 1
                # self._clamp_col(buffer)

        def down(self, buffer):
            if self.row < buffer - 1:
                self.row += 1
                # self._clamp_col(buffer)

        def left(self):
            if self.col > 0:
                self.col -= 1
            elif self.row > 0:
                self.row -= 1

        def right(self, buffer):
            if self.col < buffer-1:
                self.col += 1
            elif self.row < buffer - 1:
                self.row += 1
                self.col = 0

        def jump_to_next(self, elements: list[TUIelement]):
            for index, element in enumerate(elements):
                if not element.focusable:
                    continue

                if element.has_focus:
                    # logger.debug(f"element {element} has focus")
                    element.remove_focus()
                    if index < len(elements)-1:
                        elements[index + 1].set_focus()
                        return
                    else:
                        break

            for element in elements:
                if element.focusable:
                    element.set_focus()
                    return


        def _clamp_col(self, buffer):
            self.col = min(self.col, len(buffer))
    

class Buffer:
    def __init__(self, lines):
        self.lines = lines

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, index):
        return self.lines[index]

    @property
    def bottom(self):
        return len(self) - 1

    def insert(self, cursor, string):
        row, col = cursor.row, cursor.col
        try:
            current = self.lines.pop(row)
        except IndexError:
            current = ''
        new = current[:col] + string + current[col:]
        self.lines.insert(row, new)

    def split(self, cursor):
        row, col = cursor.row, cursor.col
        current = self.lines.pop(row)
        self.lines.insert(row, current[:col])
        self.lines.insert(row + 1, current[col:])

    def delete(self, cursor):
        row, col = cursor.row, cursor.col
        if (row, col) < (self.bottom, len(self[row])):
            current = self.lines.pop(row)
            if col < len(current):
                new = current[:col] + current[col + 1:]
                self.lines.insert(row, new)
            else:
                next = self.lines.pop(row)
                new = current + next
                self.lines.insert(row, new)

