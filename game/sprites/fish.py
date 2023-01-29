import random


from pygame.rect import Rect

from core.animate import Animation
from core.enemy import Enemy


class Fish(Enemy):
    def __init__(
        self,
        animations: dict[str, Animation],
        screen_rect: Rect,
        size: (int, int),
        *groups
    ):
        self.position = (random.randrange(-300, -10), random.randrange(350, 500))

        super().__init__(
            *groups,
            pos=self.position,
            size=size,
            speed=0.9,
            animations=animations,
            screen_rect=screen_rect,
            *groups
        )

    def get_caught(self):
        self.exact_position = [
            random.randrange(-500, -200),
            random.randrange(350, 500)
        ]
