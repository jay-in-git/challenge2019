import random

from pygame.math import Vector2 as Vec

import View.const      as view_const
import Model.const     as model_const
from Events.Manager import *


class Player(object):
    __slots__ = ('index', 'name', 'team_index','radius', 'position', 'value', 'color', 'is_AI', 'direction', 'direction_no', 'oil_multiplier', 'insurance_value', 'speed', 'pet', 'item', 'is_invincible', 'magnet_attract', 'freeze', 'theworld', 'collide_list', 'equipments', 'speed_multiplier', 'bag')
    def __init__(self, name, index, team_index, pet_list, equipments = [0, 0, 0, 0, 0], is_AI = False):
        self.index = index
        self.name = name
        self.team_index = team_index
        self.radius = model_const.player_radius
        self.position = Vec(model_const.base_center[self.index])
        self.value = 0
        self.color = random.choice(view_const.PLAYER_COLORS)
        self.is_AI = is_AI
        self.direction = Vec(0, 0)
        self.direction_no = model_const.player_initial_direction_no[index]
        self.oil_multiplier = 1  # the oil player gains will be multiplied with this value
        self.insurance_value = model_const.init_insurance  # when collide, the player can keep at least this oil
        self.speed = model_const.player_normal_speed
        self.pet = pet_list[index]
        self.equip_equipments(equipments)
        self.item = None
        self.is_invincible = False
        self.magnet_attract = False #Use Magnet Attract to make it true
        self.freeze = False
        self.theworld = False
        self.collide_list = [i == index for i in range(4)]
        self.bag = None

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_item(self):
        return self.item

    def equip_equipments(self, equipments):
        self.equipments = equipments
        self.speed_multiplier = model_const.speed_multiplier ** equipments[model_const.speed_up_idx]
        self.speed *= self.speed_multiplier
        self.oil_multiplier = model_const.oil_multiplier ** equipments[model_const.oil_up_idx]
        self.insurance_value = model_const.init_insurance * equipments[model_const.insurance_idx]
        self.pet.carry_max *= model_const.pet_carry_max_up_multiplier ** equipments[model_const.pet_carry_max_up_idx]
        self.pet.cd_time *= int(model_const.pet_cd_down_multiplier ** equipments[model_const.pet_cd_down_idx])
        self.pet.cd = self.pet.cd_time

    def use_item(self, ev_manager):
        if self.item is not None and not self.item.active:
            self.item.trigger(ev_manager)

    def pick_oil(self, oils, ev_manager):
        for i, oil in reversed(list(enumerate(oils))):
            if (oil.position - self.position).length_squared() <= (oil.radius + self.radius)**2:
                if self.value + oil.price * self.oil_multiplier <= model_const.bag_capacity:
                    self.value += oil.price * self.oil_multiplier
                    ev_manager.post(EventEatOil(oil.price))
                    oils.remove(oil)
                    

    def store_price(self, bases, ev_manager):
        if self.position[0] <= bases[self.index].center[0] + bases[self.index].length/2 \
            and self.position[0] >= bases[self.index].center[0] - bases[self.index].length/2 \
            and self.position[1] <= bases[self.index].center[1] + bases[self.index].length/2 \
            and self.position[1] >= bases[self.index].center[1] - bases[self.index].length/2:
            bases[self.index].change_value_sum(self.value)
            if self.value > 0:
                ev_manager.post(EventStorePrice(self.value))
            self.value = 0

    def check_collide(self, player_list, ev_manager):
        collide = []
        sum_of_all = 0
        for player in player_list:
            if player.is_invincible:
                continue
            if (player.position - self.position).length() <= self.radius + player.radius:
                collide.append(player)
                sum_of_all += max(player.value - player.insurance_value, 0)
        new_collide_list = [False] * 4
        for player in collide:
            player.value = min(player.value, player.insurance_value)
            player.value += sum_of_all / len(collide)
            player.bag = sum_of_all / len(collide)
            new_collide_list[player.index] = True
        for idx in range(4):
            if new_collide_list[idx] and not self.collide_list[idx] and idx > self.index:
                ev_manager.post(EventEqualize((player_list[idx].position + self.position) / 2))
        self.collide_list = new_collide_list


    def check_market(self, market_list):
        for market in market_list:
            if (market.position - self.position).length() <= self.radius + model_const.market_radius:
                return market
        return None

    def buy(self, market_list):
        market = self.check_market(market_list)
        if market and market.item is not None and self.value >= market.item.price:
            self.value -= market.item.price
            self.item = market.item
            self.item.player_index = self.index
            market.sell()

    def update_speed(self):
        self.speed = self.speed_multiplier * max(model_const.player_speed_min, model_const.player_normal_speed - model_const.player_speed_decreasing_rate * self.value)

    def update(self, oils, bases, players, ev_manager):
        if self.item is not None and self.item.active:
            self.item.update(ev_manager)
        self.update_speed()
        if self.magnet_attract:
            for oil in oils:
                if Vec.magnitude(oil.position - self.position) <= oil.radius + model_const.magnet_attract_radius:
                    oil.update_position(Vec.normalize(self.position - oil.position) * model_const.magnet_attract_speed)
        if not self.freeze and not self.theworld:
            new_x = self.position[0] + self.direction[0] * self.speed
            new_y = self.position[1] + self.direction[1] * self.speed
            if new_x < self.radius or new_x > view_const.game_size[0] - self.radius:
                self.direction[0] = 0
            if new_y < self.radius or new_y > view_const.game_size[1] - self.radius:
                self.direction[1] = 0
            self.position += Vec(self.direction) * self.speed
        self.pick_oil(oils, ev_manager)
        self.store_price(bases, ev_manager)

    def update_collision(self, players, ev_manager):
        if not self.is_invincible:
            self.check_collide(players, ev_manager)

