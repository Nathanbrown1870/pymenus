import curses
from curses import panel

from src.element_rootClass import TUIelement

# this might need one more class inbetween, TUIelement -> screen -> panel & window & pad $ yes no ...
class panel_element(TUIelement): 

    def __init__(self, cols, rows, tlx_position, tly_position):
        super().__init__(tlx_position, tly_position)
        self.win = curses.newwin(rows, cols, tly_position, tlx_position)
        self.panel = panel.new_panel(self.win)
        self.win.bkgdset(ord(' '), curses.A_BOLD)
        self.win.box()
        str="this is a panel"
        self.win.addstr(2, 2, str)
        self.contents = []

        curses.init_pair(2, curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)


    def highlight(self):
        self.win.bkgd(' ', curses.color_pair(1))

    def remove_highlight(self):
        self.win.bkgd(' ', curses.color_pair(2))

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
