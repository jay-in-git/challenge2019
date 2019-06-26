import time, random, sys

from Model.StateMachine import *
from Model.GameObject.player import *
from Model.GameObject.oil import *
from Model.GameObject.base import *
from Model.GameObject.pet import *
from Model.GameObject.market import *
from Model.GameObject.scoreboard import Scoreboard

import Model.const       as model_const
import View.const        as view_const
from Events.Manager import *

class GameEngine(object):
    """
    Tracks the game state.
    """
    def __init__(self, ev_manager, AI_names):
        """
        evManager (EventManager): Allows posting messages to the event queue.

        Attributes:
            running (bool): True while the engine is online. Changed via Event_Quit().
            state (StateMachine()): control state change, stack data structure.
            AIList (list.str): all AI name list.
            players (list.player()): all player object.
            TurnTo (int): current player
        """
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.running = False
        self.state = StateMachine()
        self.AI_names = AI_names
        self.player_list = []
        self.pet_list = []
        self.oil_list = []
        self.base_list = []
        self.free_market_list = []
        self.priced_market_list = []
        self.turn_to = 0
        self.timer = 0
        self.fadacai = False

        self.init_oil()
        self.init_pet()
        self.init_player()
        self.init_base()
        self.init_markets()

        self.scoreboard = Scoreboard(self.player_list, self.base_list)

        random.seed(time.time())
        

    def notify(self, event):
        """
        Called by an event in the message queue. 
        """
        if isinstance(event, EventEveryTick):
            cur_state = self.state.peek()
            if cur_state == STATE_PLAY:
                self.update_objects()
        elif isinstance(event, EventStateChange):
            # if event.state is None >> pop state.
            if event.state is None:
                # false if no more states are left
                if not self.state.pop() or event.state == STATE_ENDGAME:
                    self.ev_manager.post(EventQuit())
            elif event.state == STATE_RESTART:
                self.state.clear()
                self.state.push(STATE_MENU)
            else:
                # push a new state on the stack
                self.state.push(event.state)
        elif isinstance(event, EventMove):
            self.set_player_direction(event.player_index, event.direction)
        elif isinstance(event, EventTriggerItem):
            player = self.player_list[event.player_index]
            if player.item is not None:
                player.use_item(self.ev_manager)
            else:
                player.buy(self.free_market_list + self.priced_market_list)
        elif isinstance(event, EventQuit):
            self.running = False
        elif isinstance(event, (EventInitialize, EventRestart)):
            pass  # self.initialize()
        elif isinstance(event, EventFaDaCaiStart):
            self.fadacai = True
        elif isinstance(event, EventFaDaCaiStop):
            self.fadacai = False

    def init_player(self):
        # set AI Names List
        # "_" ==> default AI, "~" ==> manual player
        self.player_list, manual_player_num = [], 0
        for index in range(model_const.player_number):
            if len(self.AI_names) > index:
                PlayerName = self.AI_names[index]
                if PlayerName == "~":
                    if manual_player_num < model_const.max_manual_player_num:
                        manual_player_num += 1
                    else:
                        self.AI_names[index] = "_"
            else:
                if manual_player_num < model_const.max_manual_player_num:
                    manual_player_num += 1
                    self.AI_names.append("~")
                else:
                    self.AI_names.append("_")

        # init Player object
        for index in range(model_const.player_number):
            if self.AI_names[index] == "~":
                Tmp_P = Player("manual", index, self.pet_list, model_const.default_equipments[index])
            elif self.AI_names[index] == "_":
                Tmp_P = Player("default", index, self.pet_list)
            else:
                Tmp_P = Player(self.AI_names[index], index, self.pet_list)
            self.player_list.append(Tmp_P)
            
    def init_pet(self):
        self.pet_list = []
        for index in range(model_const.player_number):
            self.pet_list.append(Pet(index, model_const.base_center[index]))

    def init_markets(self):
        # self.free_market_list = [ Market(position, is_free=True) for position in model_const.free_market_positions ]
        self.priced_market_list = [ Market(position, is_free=False) for position in model_const.priced_market_positions ]

    def set_player_direction(self, player_index, direction):
        if self.player_list[player_index] is not None:
            player = self.player_list[player_index]
            player.direction = Vec(model_const.dir_mapping[direction]) 
            if direction > 0:
                player.direction_no = direction

    def update_objects(self):
        # Update player_list
        for player in self.player_list:
            player.update(self.oil_list, self.base_list, self.player_list, self.ev_manager)

        if self.timer % 2400 == 1000:
            for pet in self.pet_list:
                pet.change_status(1)
        
        for pet in self.pet_list:
            pet.update(self.player_list, self.base_list)

        for oil in self.oil_list:
            oil.update()
        self.try_create_oil()

        for market in (self.free_market_list + self.priced_market_list):
            market.update(self.player_list, self.oil_list, self.base_list, None)

        self.scoreboard.update()

        self.timer -= 1
        if self.timer == 0:
            self.ev_manager.post(EventStateChange(STATE_ENDGAME))

    def init_oil(self):
        for _ in range(model_const.init_oil_number):
            self.create_oil()

    def create_oil(self):
        self.oil_list.append(new_oil())

    def try_create_oil(self):
        if self.fadacai:
            if random.random() < model_const.fadacai_oil_probability:
                self.create_oil()
        else:
            if random.random() < model_const.oil_probability:
                self.create_oil()

    def init_base(self) :
        # todo
        for index in range(model_const.player_number) :
            self.base_list.append(Base(index, model_const.base_center[index]))
    
    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify(). 
        """
        self.running = True
        self.ev_manager.post(EventInitialize())
        self.state.push(STATE_MENU)
        self.timer = model_const.game_length
        while self.running:
            newTick = EventEveryTick()
            self.ev_manager.post(newTick)
