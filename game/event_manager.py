from typing import Dict


class Event(object):
    """
    A superclass for any event that may be generated 
    by an object and sent to the EventManager.
    """
    def __init__(self) -> None:
        pass


class TickEvent(Event):
    def __init__(self) -> None:
        self.name = "Move Event"


class UpdateScoreEvent(Event):
    def __init__(self) -> None:
        self.name = "Update Score Event"


class GameOverEvent(Event):
    def __init__(self) -> None:
        self.name = "Game Over Event"


class CreateNewPreyEvent(Event):
    def __init__(self) -> None:
        self.name = "Create New Prey Event"


class EventManager(object):
    """
    Coordinates communication between the model, view, and controller.
    """    
    
    def __init__(self) -> None:
        self.listeners = dict()

    def RegisterListener(self, listener: object) -> None:
        """
        Adds a listener. The listener will recieve posted events
        through its notify(event) call.
        """    
        self.listeners[listener] = 1

    def UnregisterListener(self, listener: object) -> None:
        """
        Removes a listener.
        """    
        if listener in self.listener.keys():
            del self.listeners[listener]

    def Post(self, event: Event) -> None:
        """
        Post new event. The event will be broadcasted to all listeners.
        """
        for listener in self.listeners.keys():
            listener.notify(event)