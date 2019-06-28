import pygame as pg
import Model.main as model
import Model.const as model_const
import View.const as view_const
import View.utils as view_utils
import os.path

'''
* How Animation works:

tick = 0
animations = []
while True:
    for ani in animations:
        if ani.expired:
            animations.remove(ani)

    animations.append(new_animation)

    for ani in animations:
        ani.draw(screen)
    
    tick += 1
'''

class Animation_base():
    '''
    Base class of all animation.
    There will be a list (call it ANI) of all currently effective animations in main.py of view.
    To start an animation, you have to append the new Animation to ANI.
    Every animation in ANI should be drawn (if valid) or be discarded (if expired) in every tick.
    '''

    def __init__(self, delay_of_frames, **pos):
        self._timer = 0
        self.expired = False
    
    def update(self):
        pass

    def draw(self, screen):
        # draw first
        # update second
        pass


class Animation_vector(Animation_base):
    pass


class Animation_raster(Animation_base):
    frames = tuple()

    @classmethod
    def init_convert(cls):
        cls.frames = tuple( _frame.convert_alpha() for _frame in cls.frames )
    
    def __init__(self, delay_of_frames, expire_time, **pos):
        self._timer = 0
        self.delay_of_frames = delay_of_frames
        self.frame_index_to_draw = 0
        self.expire_time = expire_time
        self.expired = False
        pos[next(iter(pos))] = pg.math.Vector2(pos[next(iter(pos))]) # turn tuple into vec2
        self.pos = pos

    def update(self):
        self._timer += 1

        if self._timer == self.expire_time:
            self.expired = True
        elif self._timer % self.delay_of_frames == 0:
            self.frame_index_to_draw = (self.frame_index_to_draw + 1) % len(self.frames)

        # update self.pos if needed
        # self.pos[ next(iter(self.pos)) ] = pg.math.Vector2(next_pos)
        # or
        # self.pos[ next(iter(self.pos)) ] += pg.math.Vector2(dx, dy)
            
    def draw(self, screen):
        screen.blit(
            self.frames[self.frame_index_to_draw],
            self.frames[self.frame_index_to_draw].get_rect(**self.pos),
        )

        self.update()
        

class Animation_equalize(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'equalize_background.png')),
            1 / 20 * i
        )
        for i in range(1, 21)
    )

    def __init__(self, **pos):
        super().__init__(2, 2*len(self.frames), **pos)


class Animation_gohome(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'gohome.png')),
            1/20 * i
        )
        for i in range(1, 20)
    )

    def __init__(self, **pos):
        super().__init__(1, 2*len(self.frames), **pos)


class Animation_magnetattract(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'mag.png')),
            1 / 40 * i
        )
        for i in range(1, 11)
    )

    def __init__(self, player_index, model):
        super().__init__(2, model_const.magnet_attract_duration, center=model.player_list[player_index].position)
        self.player_index = player_index
        self.model = model
    
    def update(self):
        super().update()
        self.pos[ next(iter(self.pos)) ] = self.model.player_list[self.player_index].position


class Animation_othergohome(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'othergohome.png')),
            1/20 * i
        )
        for i in range(1, 20)
    )

    def __init__(self, **pos):
        super().__init__(1, 2*len(self.frames), **pos)


class Animation_radiationOil(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'radiation.png')),
            1/30 * i
        )
        for i in range(1, 30)
    )

    def __init__(self, **pos):
        super().__init__(1, 2*len(self.frames), **pos)

# the countdown animation
class Animation_start():
    pass


class Animation_shuffleBases_vertical(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'thunder_vertical.png')),
            1/30 * i
        )
        for i in range(1, 30)
    )

    def __init__(self, **pos):
        super().__init__(1, 2*len(self.frames), **pos)

class Animation_shuffleBases_horizontal(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'thunder_horizontal.png')),
            1/30 * i
        )
        for i in range(1, 30)
    )

    def __init__(self, **pos):
        super().__init__(1, 2*len(self.frames), **pos)
# the countdown animation
class Animation_start():
    pass

class Animation_endboard(Animation_raster):
    def __init__(self, color, max_height, **pos):
        super().__init__(1, 90, **pos)
        self.height = 1
        self.vel = max_height / self.expire_time

    def update(self):
        if self.height + self.vel < self.max_height:
            self.height += self.vel
        else:
            self.height = self.max_height

    def draw(self, screen):
        col = pg.Rect(0,0,0,0)
        col.w = 200
        col.h = self.height
        col.midbottom = self.pos + (0, -20)
        pg.draw.rect(screen, self.color, col)
        self.update()


"""class Animation_freeze(Animation_raster):
    frames = tuple(
        view_utils.scaled_surface(
            pg.image.load(os.path.join(view_const.IMAGE_PATH, 'ice.png')),
            1/30 * i
        )
        for i in range(1, 30)
    )

    def __init__(self, **pos):
        super().__init__(1, len(self.frames), **pos)

# the countdown animation
class Animation_start():
    pass
"""

def init_animation():
    Animation_equalize.init_convert()
    Animation_gohome.init_convert()
    Animation_magnetattract.init_convert()
    Animation_othergohome.init_convert()
    Animation_radiationOil.init_convert()
    """Animation_freeze.init_convert()"""

