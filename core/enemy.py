import random

from pygame.rect import Rect

from core.ai import BasicAI
from core.coords import get_cell_coordinates
from core.sprite import BaseSprite
from settings import DIRECTIONS, DIRECT_DICT


class Enemy(BaseSprite):
    """
    The base class for all enemies.
    """

    def __init__(
        self,
        pos,
        speed,
        size,
        animations,
        screen_rect: Rect,
        *groups
    ):
        super().__init__(pos, size, *groups)
        self.steps = [0, 0]
        self.speed = speed
        self.direction = "right"
        self.anim_directions = DIRECTIONS[:]
        self.anim_direction = random.choice(self.anim_directions)
        self.animations = animations
        self.screen_rect = screen_rect
        self.image = None
        self.state = "swim"
        self.ai = BasicAI(self)

    def get_occupied_cell(self):
        return get_cell_coordinates(
            self.screen_rect,
            self.rect.center, self.rect.size
        )

    def check_outbounds(self):
        left_x, _ = self.rect.topleft
        right_x, _ = self.rect.topright

        width = self.screen_rect.width
        return (width < left_x and width < right_x) or (left_x < 0 and right_x < 0)

    def update(self, now, obstacles):
        if self.state not in ("caught", "die"):
            if self.direction:
                self.move()
            else:
                self.change_direction(obstacles)

            if self.check_outbounds():
                self.change_directory_outbounds()

        self.rect.topleft = self.exact_position
        self.image = self.get_animation().get_next_frame(now)

    def move(self):
        for index in (0, 1):
            vec_component = DIRECT_DICT[self.direction][index]
            self.exact_position[index] += vec_component * self.speed
            self.steps[index] += abs(vec_component * self.speed)

    def change_directory_outbounds(self):
        left_x, _ = self.rect.topleft
        right_x, _ = self.rect.topright

        width = self.screen_rect.width
        if width < left_x and width < right_x:
            animation = "left"
        elif left_x < 0 and right_x < 0:
            animation = "right"
        else:
            return

        self.direction = animation
        self.anim_direction = animation

    def change_direction(self, obstacles):
        self.snap_to_grid()

        self.direction = self.ai(obstacles)
        if self.direction in self.anim_directions:
            self.anim_direction = self.direction

    def snap_to_grid(self):
        self.steps = [0, 0]
        self.rect.topleft = self.get_occupied_cell()
        self.exact_position = list(self.rect.topleft)

    def get_animation(self):
        try:
            animation = self.animations[self.state][self.anim_direction]
        except TypeError:
            animation = self.animations[self.state]
        return animation

    def draw(self, surface):
        surface.blit(self.image, self.rect)
