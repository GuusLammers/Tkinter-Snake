import threading

from event_manager import EventManager
from model import Game
from view import Gui


WINDOW_WIDTH = 500           
WINDOW_HEIGHT = 300 
SNAKE_ICON_WIDTH = 15  
BACKGROUND_COLOUR = "green" 
ICON_COLOUR = "yellow" 


if __name__ == "__main__":
    eventManager = EventManager()
    game = Game(eventManager, WINDOW_WIDTH, WINDOW_HEIGHT)
    gui = Gui(game, eventManager, WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOUR, ICON_COLOUR, SNAKE_ICON_WIDTH)

    threading.Thread(target = game.superloop, daemon=True).start()

    gui.root.mainloop()
