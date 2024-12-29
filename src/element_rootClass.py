from abc import ABC, abstractmethod
import curses

class TUIelement(ABC):
    
    def __init__(self,x_position,y_position) -> None:
        self.x_position: int = x_position
        self.y_position: int = y_position
        self.focusable: bool = True
        self.has_focus: bool = False

    @abstractmethod
    def set_focus(self):
        self.has_focus = True

    @abstractmethod
    def remove_focus(self):
        self.has_focus = False

    @abstractmethod
    def add_to_screen(self,screen):
        pass
        
    # @abstractmethod
    # def refresh(self):
    #     pass