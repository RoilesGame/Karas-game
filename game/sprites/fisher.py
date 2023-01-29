import pygame.sprite
from pygame.surface import Surface

from core.animate import Animation
from core.sprite import BaseSprite
from settings import DEFAULT_CONTROLS


class Fisher(BaseSprite):
    def __init__(
        self,
        x: int,
        y: int,
        animations: dict[str, Animation],
        *groups
    ):
        self.animations = animations

        self.controls = DEFAULT_CONTROLS
        self.speed = 1.1

        self.animation = "normal"
        super().__init__((x, y), (60.8, 57.6), *groups)

    def catch_animation(self):
        self.animation = "catch"

    def update(self, now, *args):
        if self.animation == "catch" and self.get_anim().done:
            self.get_anim().reset()
            self.animation = "normal"

        self.image = self.get_anim().get_next_frame(now)
        width, height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (width * 1.6, height * 1.6))

    def get_anim(self):
        return self.animations[self.animation]
