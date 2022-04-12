from tkinter import Tk, Canvas, Button

from event_manager import *
from model import Game


class Gui():
    """
        This class takes care of the game's graphic user interface (gui)
        creation and termination.
    """
    def __init__(
        self, 
        game: Game, 
        eventManager: EventManager, 
        WINDOW_WIDTH: int, 
        WINDOW_HEIGHT: int, 
        BACKGROUND_COLOUR: str, 
        ICON_COLOUR: str, 
        SNAKE_ICON_WIDTH: int):
        """        
            The initializer instantiates the main window and 
            creates the starting icons for the snake and the prey,
            and displays the initial gamer score.
        """
        self.eventManager = eventManager
        eventManager.RegisterListener(self)

        self.game = game

        #some GUI constants
        scoreTextXLocation = 60
        scoreTextYLocation = 15
        textColour = "white"
        #instantiate and create gui
        self.root = Tk()
        self.canvas = Canvas(self.root, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, bg = BACKGROUND_COLOUR)
        self.canvas.pack()
        #create starting game icons for snake and the prey
        self.snakeIcon = self.canvas.create_line((0, 0), (0, 0), fill=ICON_COLOUR, width=SNAKE_ICON_WIDTH)
        self.preyIcon = self.canvas.create_rectangle(0, 0, 0, 0, fill=ICON_COLOUR, outline=ICON_COLOUR)
        #display starting score of 0
        self.score = self.canvas.create_text(scoreTextXLocation, scoreTextYLocation, fill=textColour, text='Your Score: 0', font=("Helvetica","11","bold"))
        #binding the arrow keys to be able to control the snake
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<Key-{key}>", self.game.whenAnArrowKeyIsPressed)

    def gameOver(self):
        """
            This method is used at the end to display a
            game over button.
        """
        gameOverButton = Button(self.canvas, text="Game Over!", 
            height = 3, width = 10, font=("Helvetica","14","bold"), 
            command=self.root.destroy)
        self.canvas.create_window(200, 100, anchor="nw", window=gameOverButton)

    def notify(self, event: Event):
        """
        The event manager will send all recieved events here. 
        """
        if isinstance(event, TickEvent):
            points = [x for point in self.game.snakeCoordinates for x in point]
            self.canvas.coords(self.snakeIcon, *points)    
        elif isinstance(event, CreateNewPreyEvent):
            self.canvas.coords(self.preyIcon, *self.game.preyCoordinates)   
        elif isinstance(event, GameOverEvent):
            self.gameOver()
        elif isinstance(event, UpdateScoreEvent):
            self.canvas.itemconfigure(self.score, text=f"Your Score: {self.game.score}")         