import pygame
from pygame.rect import Rect
from pygame.surface import Surface


class TitleSprite(pygame.sprite.Sprite):
    def __init__(self, image: Surface, screen_rect: Rect, *groups):
        self.image = image
        center_x, center_y = screen_rect.center
        self.rect = image.get_rect(center=(center_x, center_y - 160))
        super().__init__(*groups)
