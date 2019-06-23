import Model.const as model_const
import View.const as view_const
import numpy as np
import math
import random
from pygame.math import Vector2 as Vec

class Oil(object):
    def __init__(self, pos, price):
        self.position = pos
        self.price = price
        self.radius = model_const.oil_radius

    def update(self):
        pass

def calc_price(pos):
    game_center = Vec(
        view_const.game_size[0] / 2,
        view_const.game_size[1] / 2
        )
    dist_from_center = (pos - game_center).length()
    mean = view_const.game_size[0] / dist_from_center
    price = min(
        model_const.price_max, 
        np.random.normal(mean, model_const.price_scale)
        )
    return price

def new_oil(): 
    R = random.random() * 400
    theta = random.random() * np.pi
    pos = Vec(
	R * math.cos(theta) + 400,
	R * math.sin(theta) + 400
        )
    price = calc_price(pos)
    return Oil(pos, price) 
