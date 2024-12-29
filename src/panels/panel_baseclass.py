import curses
from curses import panel

from typing import override

from src.element_rootClass import TUIelement
from src.screenBase import ScreenBase

class panel_element(ScreenBase): 
    def __init__(self, width: int, height: int, tlx_position: int, tly_position: int):
        win = curses.newwin(height, width, tly_position, tlx_position)
        super().__init__(win, tlx_position, tly_position)
        self.focusable = True

        self.panel = panel.new_panel(self.screen)
        self.screen.box()

        curses.init_pair(2, curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    @override
    def identify(self):
        return __name__
        
    @override
    def add_text(self, text):
        height, width = self.screen.getmaxyx()
        content_height = height - 2  # Exclude top and bottom borders
        content_width = width - 2    # Exclude left and right borders 

        text_arry = text.split()
        i = 0 
        for row in range(content_height):
            for column in range(content_width):
                if i < len(text):
                    self.screen.addch(1 + row, 1 + column, text[i])
                    i += 1
                else:
                    return

    # BUG: this will overflow the edges and to the next row, it needs to check if the string will print and cancatonate that...
    def add_list(self, text):
        height, width = self.screen.getmaxyx()
        content_height = height - 2  # Exclude top and bottom borders
        content_width = width - 2    # Exclude left and right borders 

        text_arry = text.split()
        i = 0 
        for row in range(content_height):
            for column in range(content_width):
                if i < len(text_arry):
                    self.screen.addstr(1 + row, 1 + column, text_arry[i])
                    i += 1
                    break
                else:
                    return
    

    def bold(self):
        self.screen.bkgdset(ord(' '), curses.A_BOLD)

    def highlight(self):
        self.screen.bkgd(' ', curses.color_pair(1))

    def remove_highlight(self):
        self.screen.bkgd(' ', curses.color_pair(2))

    def set_focus(self):
        self.highlight()
        return super().set_focus()

    def remove_focus(self):
        self.remove_highlight()
        return super().remove_focus()

    def add_to_screen(self, screen):
        pass
        # panel.update_panels(); 
        # screen.refresh()
