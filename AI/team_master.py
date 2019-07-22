from AI.base import *
import Model.const as model_const

from pygame.math import Vector2 as Vec
import random
PICK = 9
direct = [
[0, 0],             #steady
[0, -1],             #up
[0.707, -0.707],     #up right
[1, 0],             #right
[0.707, 0.707],    #right down
[0, 1],            #down
[-0.707, 0.707],   #left down
[-1, 0],            #left
[-0.707, -0.707],    #left up
]
class TeamAI(BaseAI):
    def __init__(self, helper):
        self.helper = helper
        self.equipments = [0, 0, 0, 0, 0]
        self.prev = Vec(self.helper.market_position) - Vec(self.helper.get_player_position())
        self.prev /= self.prev.magnitude()
        self.want_to_buy = {'RadiusNotMove' : 100, 'TheWorld' : 100, 'IGoHome' : 100, 'ShuffleBases': 1, 'Invincible': 1}
        self.FaDaCai1 = True
    def update_direction(self, v):
        beta = 0
        v = v / v.magnitude() if v.magnitude() > 1e-5 else v
        self.prev = beta * self.prev + (1 - beta) * v
        return self.prev
    def get_best_oil_position(self):
        my_pos = self.helper.get_player_position()
        oil_poses = self.helper.get_oils()
        oil_prices = self.helper.get_oils_distance_to_center()
        best_pos = None
        best_cp = -1
        for i in range(len(oil_poses)):
            cp = (400-oil_prices[i])/((Vec(my_pos) - Vec(oil_poses[i])).length()**2)
            if cp > best_cp:
                best_cp = cp
                best_pos = oil_poses[i]
        return best_pos, my_pos, best_cp

    def attack(self, carry, my_pos):
        if self.helper.get_player_item_is_active() and self.helper.get_player_item_name() == 'Invincible':
            return 0, 0
        players_value = self.helper.get_players_value()
        players_speed = self.helper.get_players_speed()
        players_position = self.helper.get_players_position()
        my_speed = self.helper.get_player_speed()
        maximum = 0
        target = -1
        for i in range(4):
            if self.helper.player_id == i or self.helper.get_player_is_invincible(i) or self.helper.get_player_is_invincible():
                continue
            cp = 1e-3 * (players_value[i] - carry)/(((Vec(my_pos) - Vec(players_position[i])).length() / abs(players_speed[i] - my_speed + 1)))
            # print("{}th cp is {}".format(i, cp))
            if maximum <= cp and players_speed[i] < my_speed:
                maximum = cp
                target = i
        return maximum, players_position[target]

    def ankle_break(self, my_dir, carry, my_pos):
        players_position = self.helper.get_players_position()
        new_dir = Vec(direct[my_dir])
        for i in range(4):
            if self.helper.player_id == i:
                continue
            distance = (Vec(players_position[i]) - Vec(my_pos)).length()
            if distance <= 9 * self.helper.player_radius and self.helper.get_player_value(player_id = i) < self.helper.get_player_value():
                vector_of_centers = (Vec(my_pos) - Vec(self.helper.get_player_position(player_id = i)))
                new_dir = Vec(direct[my_dir]) +  vector_of_centers / vector_of_centers.length()
        maximum = 0
        togo = -1
        for i in range(1, 9):
            # print("new is {}".format(new_dir))
            if maximum < new_dir.dot(Vec(direct[i])):
                maximum = new_dir.dot(Vec(direct[i]))
                togo = i
        return togo

    def pick_item(self, dest, my_pos, carry):
        if self.helper.get_player_item_name() or self.helper.get_player_item_is_active():
            return dest
        total_value = carry + self.helper.get_base_value()
        time_past = 60 * 60 * 4 - self.helper.get_timer()
        item = self.helper.get_market()
        # print("{} / {} = {}".format(total_value, (time_past + 1e-9), total_value / (time_past + 1e-9)))
        the_max = True
        for i in range(4):
            if i == self.helper.player_id:
                continue
            if total_value < self.helper.get_player_value(player_id=i) + self.helper.get_player_value(player_id=i):
                the_max = False
        if item[0] in self.want_to_buy and self.want_to_buy[item[0]] > 0 and carry > item[1] and not self.helper.get_player_item_name():
            if (Vec(my_pos) - Vec(self.helper.get_market_center())).length() < self.helper.player_radius:
                self.want_to_buy[item[0]] -= 1
                return PICK
            return self.helper.get_market_center()
        return dest
    def use(self, my_pos):
        if not self.helper.get_player_item_is_active():
            use_directly = ['TheWorld', 'ShuffleBases', 'Invincible', 'ShuffleBases']
            if self.helper.get_player_item_name() in use_directly:
                return True
            elif self.helper.get_player_item_name() == 'RadiusNotMove':
                tmp = 0
                best_idx = 0
                for idx in range(4):
                    if idx == self.helper.player_id:
                        continue
                    value = self.helper.get_player_value(idx)
                    if value > tmp:
                        tmp = value
                        best_idx = idx
                if self.helper.get_distance(self.helper.get_player_position(best_idx), my_pos) < model_const.radius_not_move_radius:
                    return True
        return False
    def decide(self):
        #print(self.helper.get_timer())
        if self.helper.get_timer() == 179 * 60 and self.FaDaCai1:
            self.FaDaCai1 = False
            return 10
        carry = self.helper.get_player_value()
        best_pos, my_pos, best_cp = self.get_best_oil_position()
        home = self.helper.get_base_center()
        dest = best_pos
        if self.use(my_pos) == True:
            return PICK
        home_cp = 5e-6 * carry if self.helper.get_distance(self.helper.get_base_center(), my_pos) \
                     <= self.helper.get_distance_to_center(self.helper.get_base_center()) \
                     else 3e-8 * carry * self.helper.get_distance(self.helper.get_base_center(), my_pos)**0.8

        attack_cp, target_pos = self.attack(carry, my_pos)
        if attack_cp >= best_cp:
            dest = target_pos
        dest = self.pick_item(dest, my_pos, carry)
        if dest == PICK:
            return PICK
        if home_cp > best_cp:
            if self.helper.get_player_item_duration() == 0 and (self.helper.get_player_item_name() == 'IGoHome' or \
                            self.helper.get_player_item_name() == 'OtherGoHome' or \
                            self.helper.get_player_item_name() == 'TheWorld' or \
                            self.helper.get_player_item_name() == 'Invincible'):
                return 9
            go_direction = Vec(home) - Vec(my_pos)
            return self.helper.get_direction(self.update_direction(go_direction))
        go_direction = Vec(dest) - Vec(my_pos)
        return self.helper.get_direction(self.update_direction(go_direction))