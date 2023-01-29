import random

import pygame

from settings import DIRECT_DICT, CELL_SIZE, DIRECTIONS


class BasicAI:
    def __init__(self, sprite):
        self.sprite = sprite

    def __call__(self, obstacles):
        return self.get_direction(obstacles)

    def get_direction(self, obstacles):
        new_dir = None
        while not new_dir:
            new_dir = random.choice(DIRECTIONS)
            move = (
                DIRECT_DICT[new_dir][0] * CELL_SIZE[0],
                DIRECT_DICT[new_dir][1] * CELL_SIZE[1]
            )
            self.sprite.rect.move_ip(*move)
            if self.check_collisions(obstacles):
                new_dir = None

            self.sprite.rect.move_ip(-move[0], -move[1])
        return new_dir

    def check_collisions(self, obstacles):
        return pygame.sprite.spritecollideany(self.sprite, obstacles)
