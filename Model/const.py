import View.const as view_const

game_length = 60 * 60 * 1
#dir const
"""
DIR_U  = 1
DIR_RU = 2
DIR_R  = 3
DIR_RD = 4
DIR_D  = 5
DIR_LD = 6
DIR_L  = 7
DIR_LU = 8
"""
dir_mapping = [
    [0, 0],             #steady
    [0, -1],             #up
    [0.707, -0.707],     #up right
    [1, 0],             #right
    [0.707, 0.707],    #right down
    [0, 1],            #down
    [-0.707, 0.707],   #left down
    [-1, 0],	        #left
    [-0.707, -0.707],    #left up
]

# color
colors = [ 
    view_const.COLOR_BLUE,
    view_const.COLOR_GREEN,
    view_const.COLOR_RED,
    view_const.COLOR_ORANGE
]

# oil_const
curve_a = 100000
curve_b = 100
oil_probability = 1 / 40
init_oil_number = 20
oil_radius = 8
price_max = 1200
price_min = 50
price_scale = 50

# player
player_number = 4
player_radius = 15
bag_capacity = 100**20
max_manual_player_num = 4
player_normal_speed = 7
init_insurance = 50
player_speed_decreasing_rate = player_normal_speed / price_max / 10
player_speed_min = player_normal_speed / 3
player_initial_direction_no = [4, 6, 2, 8]

# pet
pet_normal_speed = player_normal_speed / 3
pet_radius = 4
pet_carry_max = 1000
pet_cd_time = 60 * 20

# base

base_length = 100
base_center = [
    [ base_length / 2 , base_length / 2] ,
    [ view_const.game_size[0] - base_length / 2 , base_length / 2] ,
    [ base_length / 2 , view_const.game_size[0] - base_length / 2] ,
    [ view_const.game_size[0] - base_length / 2 , view_const.game_size[0] - base_length / 2]
]


# equipments
speed_up_idx = 0
oil_up_idx = 1
insurance_idx = 2
pet_carry_max_up_idx = 3
pet_cd_down_idx = 4

speed_multiplier = 1.2
oil_multiplier = 1.2
init_insurance = 50
pet_carry_max_up_multiplier = 1.5
pet_cd_down_multiplier = 0.8

default_equipments = [
    [0, 0, 0, 0, 10],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

priced_market_positions = [
    (376, 373.5)
]
market_radius = 70
market_generate_item_probability = 1 / 1
market_refresh_item_probability = 1 / 4800

item_price = {
    'IGoHome': 100, 
    'OtherGoHome': 200, 
    'TheWorld': 300,
    'MagnetAttract': 400,
    'Invincible': 500,
    'RadiusNotMove': 600,
    'RadiationOil': 700,
    'ShuffleBases': 800,
    'FaDaCai': 0,
}
the_world_duration = 60 * 5
magnet_attract_duration = 60 * 3
magnet_attract_radius = 50
magnet_attract_speed = 5
invincible_duration = 60 * 10
radius_oil_multiplier = 0.8
radius_not_move_radius = 100
radius_not_move_duration = 60 * 5
fadacai_duration = 60 * 5
fadacai_oil_probability = 1 / 3

priced_item_activate = {
    'IGoHome': True,
    'OtherGoHome': True,
    'TheWorld': True,
    'MagnetAttract': True,
    'Invincible': True,
    'RadiusNotMove': True,
    'RadiationOil': True,
    'ShuffleBases': True,
    'FaDaCai': False,
}


# score
score_position = [ (800, 160 * (i + 1)) for i in range(player_number) ]
rank_str = ['1st', '2nd', '3rd', '4th']
swap_duration = 60
