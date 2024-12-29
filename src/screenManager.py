import time
import curses
import sys

import logging
logger = logging.getLogger(__name__)

from src.element_rootClass import TUIelement
from src.screen_class import Screen_class as Screen

class ScreenManager:
    
    def __init__(self) -> None:
        self.screen = Screen(window=curses.initscr())
        self.stdscr = self.screen.screen
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self.stdscr.keypad(True)
        self.cursor = self.Cursor()
        
        # Panels might make me tracking the level of the screen stack irrelevent 
        self.stack = [self.screen]

    def add(self,element: TUIelement):
        self.screen.elments.append(element)

    def start(self):

        # clear the screen
        while True:
            self.stdscr.erase()

            # load the elements
            for elements in self.screen.elments:
                elements.add_to_screen(self.stdscr)

            # Refresh elements
            curses.panel.update_panels(); 
            self.stdscr.refresh()

            # capture input
            last_y, last_x = self.stdscr.getyx()
            self.stdscr.move(self.cursor.row,self.cursor.col)
            self.handle_input(self.screen)
            # time.sleep(5)


    def __del__(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def handle_input(self, screen: Screen):

        height, width = screen.screen.getmaxyx()

        k = screen.screen.getkey()
        if k == "q":
            sys.exit(0)
        elif k == "KEY_UP":
            self.cursor.up()
        elif k == "KEY_DOWN":
            self.cursor.down(height)
        elif k == "KEY_LEFT":
            self.cursor.left()
        elif k == "KEY_RIGHT":
            self.cursor.right(width)
        elif k == "\n":
            self.cursor.right(width)
        elif k == '\t':
            self.cursor.jump_to_next(screen.elments)
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

