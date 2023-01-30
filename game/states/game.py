from pathlib import Path

import pygame
from pygame.rect import Rect
from pygame.sprite import LayeredUpdates
from pygame import mixer

from core.state_machine import State
from game.sprites.background import CompositeBackground
from game.sprites.fish import Fish
from game.sprites.fisher import Fisher
from game.sprites.player import Hook
from settings import WATER_COLOR


class Game(State):
    def __init__(
        self,
        screen_rect: Rect,
        font: str,
        background: CompositeBackground,
        player: Hook,
        fishes: list[Fish]
    ):
        super().__init__()

        self.screen_rect = screen_rect
        self.font = font
        self.background = background
        self.player = player
        self.fishes = fishes
        self.now = None

        self.entities = LayeredUpdates()
        self.entities.add(self.background.elements, layer=1)
        self.entities.add(self.fishes, layer=2)
        self.entities.add(self.player, layer=2)

        self.fishes = LayeredUpdates()
        self.fishes.add(fishes, layer=2)

    def startup(self, now, persistant):
        mixer.init()
        pygame.mixer.music.load(Path("./assets/music/ambient.ogg").absolute())
        pygame.mixer.music.play(-1, 0.0)

    def get_event(self, event):
        """
        Process game state events. Add and pop directions from the player's
        direction stack as necessary.
        """
        if event.type == pygame.KEYDOWN:
            self.player.add_direction(event.key)
        if event.type == pygame.KEYUP:
            self.player.pop_direction(event.key)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.player.catching_state:
            self.player.catch(self.fishes)

    def update(self, keys, now):
        self.now = now
        self.entities.update(now, self.entities)

    def draw(self, surface, interpolate):
        surface.fill(WATER_COLOR, self.screen_rect)
        self.entities.draw(surface)
        self.fishes.draw(surface)

        counter_rect = self.player.counter_text.get_rect(
            topright=self.screen_rect.topright
        )
        surface.blit(self.player.counter_text, counter_rect)
