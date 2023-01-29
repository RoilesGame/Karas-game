from os import path

import pygame

CAPTION = "The Fishing"
SCREEN_SIZE = (800, 550)
BACKGROUND_COLOR = (30, 40, 50)
WATER_COLOR = (86, 88, 123)
ASSETS_PATH = ".\\assets"

FONT_PATH = path.join(ASSETS_PATH, "fonts\\Fixedsys500c.ttf")

DEFAULT_CONTROLS = {
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right"
}

DIRECT_DICT = {
    "left": (-1, 0),
    "right": (1, 0)
}
DIRECTIONS = ["left", "right"]
CELL_SIZE = (50, 50)
