"""
define Application Programming Interface(API) 
"""
from pygame.math import Vector2 as Vec

import Model.const as model_const
import View.const as view_const

class Helper(object):

    def __init__(self, model, index):
        self.model = model
        self.player_id = index
        self.oil_radius = model_const.oil_radius
        self.player_radius = model_const.player_radius
        self.bag_capacity = model_const.bag_capacity
        self.player_normal_speed = model_const.player_normal_speed
        self.base_length = model_const.base_length
        self.game_size = view_const.game_size
        

    # Get player data
    def get_self_id(self):
        return self.player_id

    def get_players_position(self):
        return [tuple(player.position) for player in self.model.player_list]
    def get_player_position(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return tuple(self.model.player_list[player_id].position)

    def get_players_direction(self):
        return [tuple(player.direction) for player in self.model.player_list]
    def get_player_direction(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return tuple(self.model.player_list[player_id].direction)

    def get_players_value(self):
        return [player.value for player in self.model.player_list]
    def get_player_value(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return self.model.player_list[player_id].value

    def get_players_bag(self):
        return [player.bag for player in self.model.player_list]
    def get_player_bag(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return self.model.player_list[player_id].bag

    def get_players_is_AI(self):
        return [player.is_AI for player in self.model.player_list]
    def get_player_is_AI(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return self.model.player_list[player_id].is_AI

    def get_players_speed(self):
        return [player.speed for player in self.model.player_list]
    def get_player_speed(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return self.model.player_list[player_id].speed

    # Get pet data

    # Get oil data
    def get_oils(self):
        return [tuple(oil.position) for oil in self.model.oil_list]
    def get_oils_distance_to_center(self):
        return [get_distance_to_center(oil) for oil in self.get_oils()]
    def get_oils_by_distance_from_center(self):
        return sort(self.get_oils(), key=lambda p: get_distance_to_center(p))

    # Get base data
    def get_bases_center(self):
        return [tuple(base.center) for base in self.model.base_list]
    def get_base_center(self, player_id = None):
        if player_id == None: player_id = self.player_id
        return tuple(self.model.base_list[player_id].center)

    # Get market data
    def get_markets(self):
        return [(tuple(market.position), market.item) for market in self.model.market_list]

    # Get item data
    def get_items_data(self):
        pass
        
    # Get game informations
    def get_timer(self):
        return self.model.timer

    # Extra functions
    def get_nearest_player(self, player_id = None):
        if player_id == None: player_id = self.player_id
        my_pos = self.get_player_position(player_id)
        players = self.get_players_position()
        return min(players.remove(my_pos), key=lambda player: (Vec(player) - Vec(my_pos)).magnitude())

    def get_nearest_oil(self, player_id = None):
        if player_id == None: player_id = self.player_id
        my_pos = self.get_player_position(player_id)
        return min(self.get_oils(), key=lambda oil: self.get_distance(oil, my_pos))
    
    def get_most_valuable_player(self):
        return max(range(4), key=lambda i: self.get_player_value(i))

    def get_nearest_market(self, player_id = None):
        if player_id == None: player_id = self.player_id
        my_pos = self.get_player_position(player_id)
        return min(self.get_markets(), key=lambda market: self.get_distance(market[0], my_pos))

    def get_nearest_market_with_item(self, player_id = None):
        if player_id == None: player_id = self.player_id
        my_pos = self.get_player_position(player_id)
        market_with_item = filter(lambda market: market[1] != None, self.get_markets())
        return min(market_with_item, key=lambda market: self.get_distance(market[0], my_pos)) if market_with_item != [] else None


    # Useful (?) functions
    def get_distance(self, p1, p2):
        return (Vec(p1) - Vec(p2)).magnitude()

    def get_distance_to_center(self, p1):
        return self.get_distance(p1, Vec(self.game_size) / 2) 
