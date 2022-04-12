import random
import time
from event_manager import *


class Game():
    '''
        This class implements the game functionalities.
    '''
    def __init__(self, eventManager: EventManager, WINDOW_WIDTH: int, WINDOW_HEIGHT: int):
        """
           This initializer sets the initial snake coordinate list, movement
           direction, and arranges for the first prey to be created.
        """
        self.eventManager = eventManager
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.score = 0
        self.direction = "Left" #initial direction of the snake
        self.gameNotOver = True
        self.preyCoordinates = tuple() # this variable keeps track of the current preys position    
        self.snakeCoordinates = [
            (495, 0), 
            (485, 0), 
            (475, 0),
            (465, 0), 
            (455, 0)]

    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move" 
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED = 0.05 # speed of snake updates (sec)
        self.createNewPrey()
        while self.gameNotOver:
            self.move()
            tickEvent = TickEvent()
            self.eventManager.Post(tickEvent)
            time.sleep(SPEED)

    def whenAnArrowKeyIsPressed(self, e) -> None:
        """ 
            This method is bound to the arrow keys
            and is called when one of those is clicked.
            It sets the movement direction based on 
            the key that was pressed by the gamer.
            Use as is.
        """
        currentDirection = self.direction
        #ignore invalid keys
        if (currentDirection == "Left" and e.keysym == "Right" or 
            currentDirection == "Right" and e.keysym == "Left" or
            currentDirection == "Up" and e.keysym == "Down" or
            currentDirection == "Down" and e.keysym == "Up"):
            return
        self.direction = e.keysym

    def move(self) -> None:
        """ 
            This method implements what is needed to be done
            for the movement of the snake.
            It generates a new snake coordinate. 
            If based on this new movement, the prey has been 
            captured, it adds a task to the queue for the updated
            score and also creates a new prey.
            It also calls a corresponding method to check if 
            the game should be over. 
            The snake coordinates list (representing its length 
            and position) should be correctly updated.
        """

        def isPreyEaten(newSnakeCoordinates: tuple) -> bool:
            """
                This function checks if the snake has eaten the prey
                when moving to its new coordinates.
            """
            COLLISION_PROXIMITY = 10 # sets how close the snake must come to the prey to eat it
            xSnake, ySnake = newSnakeCoordinates
            xPrey, yPrey = self.preyCoordinates[0] + 5, self.preyCoordinates[1] + 5
            if abs(xSnake - xPrey) < COLLISION_PROXIMITY and abs(ySnake - yPrey) < COLLISION_PROXIMITY:
                return True

            return False 

        newSnakeCoordinates = self.calculateNewCoordinates() # get new snake coordinates
        
        self.isGameOver(newSnakeCoordinates) # check if the game is over

        self.snakeCoordinates.append(newSnakeCoordinates) # add new snake coordinate to end of snakeCoordinates

        if isPreyEaten(newSnakeCoordinates): # check if the prey has been eaten
            self.score += 1
            updateScoreEvent = UpdateScoreEvent()
            self.eventManager.Post(updateScoreEvent)
            self.createNewPrey()
        else: # remove first coordinate from snake coordinate
            self.snakeCoordinates.pop(0)

    def calculateNewCoordinates(self) -> tuple:
        """
            This method calculates and returns the new 
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of 
            head of the snake.
            It is used by the move() method.    
        """
        lastX, lastY = self.snakeCoordinates[-1]
        newCoordinates = None
        # check the snakes direction
        if self.direction == "Left":
            newCoordinates = (lastX - 10, lastY)
        elif self.direction == "Right":
            newCoordinates = (lastX + 10, lastY)
        elif self.direction == "Up":
            newCoordinates = (lastX, lastY - 10)
        elif self.direction == "Down":
            newCoordinates = (lastX, lastY + 10)    

        return newCoordinates

    def isGameOver(self, snakeCoordinates) -> None:
        """
            This method checks if the game is over by 
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the gameNotOver 
            field and also adds a "game_over" task to the queue. 
        """
        
        x, y = snakeCoordinates
        if x < 0 or x > self.WINDOW_WIDTH or y < 0 or y > self.WINDOW_HEIGHT: # checking if snake is off the screen
            self.gameNotOver = False
            gameOverEvent = GameOverEvent()
            self.eventManager.Post(gameOverEvent)

        if snakeCoordinates in self.snakeCoordinates: # checking if snake tried to eat itself
            self.gameNotOver = False
            gameOverEvent = GameOverEvent()
            self.eventManager.Post(gameOverEvent)

    def createNewPrey(self) -> None:
        """ 
            This methods randomly picks an x and a y as the coordinate 
            of the new prey and uses that to calculate the 
            coordinates (x - 5, y - 5, x + 5, y + 5). 
            It then adds a "prey" task to the queue with the calculated
            rectangle coordinates as its value. This is used by the 
            queue handler to represent the new prey.                    
            To make playing the game easier, set the x and y to be THRESHOLD
            away from the walls. 
        """
       
        THRESHOLD = 15   # sets how close prey can be to borders
        x, y = random.randint(0 + THRESHOLD, self.WINDOW_WIDTH - THRESHOLD), random.randint(0 + THRESHOLD, self.WINDOW_HEIGHT - THRESHOLD) # random x and y coordinates for new prey      
        preyCoordinates = (x - 5, y - 5, x + 5, y + 5) # prey coordinates
        self.preyCoordinates = preyCoordinates 

        createNewPreyEvent = CreateNewPreyEvent()
        self.eventManager.Post(createNewPreyEvent)   