import pygame
from pygame.rect import Rect

from core.state_machine import State
from settings import BACKGROUND_COLOR

from pygame.surface import Surface


class Splash(State):
    def __init__(self, image: Surface, screen_rect: Rect):
        super().__init__()
        self.next = "TITLE"
        self.timeout = 5
        self.alpha = 0
        self.alpha_speed = 2
        self.image = image.convert()
        # size = self.image.get_size()
        # self.image = pygame.transform.scale(self.image, (screen_rect.size[0], size[-1]))
        # self.image.set_alpha(self.alpha)
        # self.rect = self.image.get_rect(top=screen_rect.top)
        self.image = pygame.transform.scale(self.image, screen_rect.size)
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=screen_rect.center)

    def update(self, keys, now):
        """Updates the splash screen."""
        self.now = now
        self.alpha = min(self.alpha + self.alpha_speed, 255)
        self.image.set_alpha(self.alpha)
        if self.now - self.start_time > 1000.0 * self.timeout:
            self.done = True

    def draw(self, surface, interpolate):
        surface.fill(BACKGROUND_COLOR)
        surface.blit(self.image, self.rect)

    def get_event(self, event):
        """
        Get events from Control. Changes to next state on any key press.
        """
        self.done = event.type == pygame.KEYDOWN
