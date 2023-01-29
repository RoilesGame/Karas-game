from typing import List

import pygame.sprite
from pygame._sprite import LayeredUpdates
from pygame.rect import Rect
from pygame.surface import Surface

from game.sprites.fisher import Fisher
from settings import WATER_COLOR


class Background(pygame.sprite.Sprite):
    def __init__(self, image: Surface, screen_rect: Rect, *groups):
        self.image = image

        size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (screen_rect.size[0], size[-1]))
        self.rect = self.image.get_rect(top=screen_rect.top)
        super().__init__(*groups)


class WaterLine(pygame.sprite.Group):
    def __init__(
            self,
            amount: int,
            image: Surface,
            screen_rect: Rect,
    ):
        self.water = [
            Water(
                image=image,
                screen_rect=screen_rect,
                multiplier=mult
            ) for mult in range(amount)
        ]
        self.bottom_water = screen_rect
        super().__init__(self.water)

    def draw(self, surface: Surface) -> List[Rect]:
        surface.blit(WATER_COLOR, self.bottom_water)

        return super().draw(surface)


class Water(pygame.sprite.Sprite):
    def __init__(
            self,
            image: Surface,
            screen_rect: Rect,
            multiplier: int,
            *groups
    ):
        self.image = image
        width, height = screen_rect.size
        image_width = self.image.get_width()
        self.image = pygame.transform.scale(
            self.image,
            (image_width * 2, self.image.get_height() * 2 + 10)
        )
        self.rect = self.image.get_rect(
            x=0 + image_width * multiplier,
            y=height // 2 + 45
        )
        super().__init__(*groups)


class Hut(pygame.sprite.Sprite):
    def __init__(self, image: Surface, *groups):
        self.image = image

        self.image = pygame.transform.scale(self.image, (280, 200))
        self.rect = Rect((0, 187, 100, 100))
        super().__init__(*groups)


class Boat(pygame.sprite.Sprite):
    def __init__(self, image: Surface, *groups):
        self.image = image
        print(self.image.get_rect())
        self.image = pygame.transform.scale(self.image, (133.2, 32.4))
        self.rect = Rect((500, 293, 133.2, 32.4))
        super().__init__(*groups)


class Reeds(pygame.sprite.Sprite):
    def __init__(self, image: Surface, x: int, y: int, *groups):
        self.image = image
        width, height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (width * 2.3, height * 2.3))
        self.rect = Rect((x, y, 100, 50))
        super().__init__(*groups)


class CompositeBackground:
    def __init__(
            self,
            background: Background,
            hut: Hut,
            water: WaterLine,
            boat: Boat,
            reeds: list[Reeds],
            fisher: Fisher
    ):
        self.background = background
        self.hut = hut
        self.water_line = water
        self.boat = boat
        self.reeds = reeds
        self.fisher = fisher
        self.elements = LayeredUpdates()

        self.elements.add(
            self.background, self.hut,
            self.boat, self.reeds, self.fisher,
            layer=1
        )
        self.elements.add(self.water_line, layer=2)

