class BaseEvent(object):
    """
    A superclass for any events that might be generated by
    an object and sent to the EventManager.
    """
    def __init__(self):
        self.name = "Generic event"
    def __str__(self):
        return self.name

class EventInitialize(BaseEvent):
    """
    Initialize event.
    """
    def __init__(self):
        self.name = "Initialize event"
    def __str__(self):
        return self.name

class EventRestart(BaseEvent):
    def __init__(self):
        self.name = "Restart event"
    def __str__(self):
        return self.name

class EventQuit(BaseEvent):
    """
    Quit event.
    """
    def __init__ (self):
        self.name = "Quit event"
    def __str__(self):
        return self.name

class EventStateChange(BaseEvent):
    """
    change state event.
    """
    def __init__(self, state):
        self.name = "StateChange event"
        self.state = state
    def __str__(self):
        return "{0} => StateTo: {1}".format(self.name, self.state)

class EventEveryTick(BaseEvent):
    """
    Tick event.
    """
    def __init__ (self):
        self.name = "Tick event"
    def __str__(self):
        return self.name

class EventEverySec(BaseEvent):
    """
    Sec event.
    """
    def __init__(self):
        self.name = "Sec event"
    def __str__(self):
        return self.name

class EventTimeUp(BaseEvent):
    """
    TimeUp event.
    """
    def __init__(self):
        self.name = "TimeUp event"
    def __str__(self):
        return self.name

class EventMove(BaseEvent):
    """
    Move event.
    """
    def __init__(self, player_index, direction):
        self.name = "Move event"
        self.player_index = player_index
        self.direction = direction
    def __str__(self):
        return "{0} => player_index = {1}, DirectionTo: {2}".format(self.name, self.player_index, self.direction)

class EventTriggerItem(BaseEvent):
    """
    Buy/Use item.
    """
    def __init__(self, player_index):
        self.name = "Trigger item event"
        self.player_index = player_index
    def __str__(self):
        return f"{self.name} => player_index = {player}"

class EventIGoHome(BaseEvent):
    def __init__(self, player):
        self.name = "I Go Home"
        self.player_index = player.index
    def __str__(self):
        return self.name

class EventOtherGoHome(BaseEvent):
    def __init__(self, player):
        self.name = "Other Go HOme"
        self.player_index = player.index
    def __str__(self):
        return self.name

class EventTheWorldStart(BaseEvent):
    '''
    A player trigger 'The World'(time stop)
    '''
    def __init__(self, player):
        self.name = f"Player {player.index} triggers The World"
        self.position = tuple(player.position)
        self.player_index = player.index
    def __str__(self):
        return self.name

class EventTheWorldStop(BaseEvent):
    '''
    The duration of 'The world' ends
    '''
    def __init__(self, player):
        self.name = "The World Ends"
        self.player_index = player.index
    def __str__(self):
        return self.name

class EventMagnetAttractStart(BaseEvent):
    '''
    The duration of 'Magnet Attract' starts
    '''
    def __init__(self, player):
        self.name = "Magnet Attract Start"
        self.player_index = player.index
    def __str__(self):
        return self.name

class EventMagnetAttractStop(BaseEvent):
    '''
    The duration of 'Magnet Attract' ends
    '''
    def __init__(self, player):
        self.name = "Magnet AttractEnd"
        self.player_index = player.index
    def __str__(self):
        return self.name

class EventRadiationOil(BaseEvent):
    def __init__(self):
        self.name = "Radiation Oil"
    def __str__(self):
        return self.name

class EventInvincibleStart(BaseEvent):
    '''
    A player trigger 'Invincible'
    '''
    def __init__(self, player):
        self.name = "Invincible Start"
        self.player_index = player.index
    def __str__(self):
        return self.name

class EventInvincibleStop(BaseEvent):
    '''
    The duration of 'Invincible' ends
    '''
    def __init__(self, player):
        self.name = "Invincible End"
        self.player_index = player.index
    def __str__(self):
        return self.name


class EventManager(object):
    """
    We coordinate communication between the Model, View, and Controller.
    """
    def __init__(self):
        self.listeners = []

    def register_listener(self, listener):
        """ 
        Adds a listener to our spam list. 
        It will receive Post()ed events through it's notify(event) call. 
        """
        self.listeners.append(listener)

    def unregister_listener(self, listener):
        """ 
        Remove a listener from our spam list.
        This is implemented but hardly used.
        Our weak ref spam list will auto remove any listeners who stop existing.
        """
        pass
        
    def post(self, event):
        """
        Post a new event to the message queue.
        It will be broadcast to all listeners.
        """
        # # this segment use to debug
        # if not (isinstance(event, Event_EveryTick) or isinstance(event, Event_EverySec)):
        #     print( str(event) )
        for listener in self.listeners:
            listener.notify(event)
