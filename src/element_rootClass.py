from abc import ABC, abstractmethod
import curses

class TUIelement(ABC):
    
    def __init__(self,x_position,y_position) -> None:
        self.x_position: int = x_position
        self.y_position: int = y_position

    @abstractmethod
    def add_to_screen(self,screen):
        pass
        
    # @abstractmethod
    # def refresh(self):
    #     pass