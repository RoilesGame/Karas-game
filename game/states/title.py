import pygame
from pygame.font import Font
from pygame.rect import Rect
from pygame.sprite import LayeredUpdates
from pygame.surface import Surface

from core.state_machine import State
from core.timer import Timer
from game.sprites.background import CompositeBackground
from game.sprites.fish import Fish
from game.sprites.title import TitleSprite
from settings import WATER_COLOR


class Title(State):
    def __init__(
        self,
        screen_rect: Rect,
        font: str,
        background: CompositeBackground,
        title: TitleSprite,
        fishes: list[Fish]
    ):
        super().__init__()
        self.screen_rect = screen_rect
        self.font = font
        self.elements = self.make_elements()
        self.elements.add(background.elements, layer=1)
        self.elements.add(title, layer=2)

        self.fishes = LayeredUpdates()
        self.fishes.add(fishes, layer=2)

    def make_elements(self) -> LayeredUpdates:
        group = LayeredUpdates()
        group.add(
            AnyKeySprite(self.screen_rect, self.font),
            layer=2
        )
        return group

    def update(self, keys, now):
        """Updates the title screen."""
        self.now = now
        self.elements.update(now)
        self.fishes.update(now, self.elements)

    def draw(self, surface, interpolate):
        surface.fill(WATER_COLOR, self.screen_rect)
        self.elements.draw(surface)
        self.fishes.draw(surface)

    def get_event(self, event):
        """
        Get events from Control.  Currently changes to next state on any key press.
        """
        if event.type != pygame.KEYDOWN:
            return
        self.next = "GAME"
        self.done = True


class AnyKeySprite(pygame.sprite.Sprite):
    def __init__(self, screen_rect: Rect, font: str, *groups):
        font = Font(font, 30)
        super().__init__(*groups)
        self.raw_image = self._render_text(font)
        self.null_image = Surface((1, 1)).convert_alpha()
        self.null_image.fill((0, 0, 0, 0))
        self.image = self.raw_image
        center = (screen_rect.centerx, 500)
        self.rect = self.image.get_rect(center=center)
        self.blink = False
        self.timer = Timer(470)

    def _render_text(self, font: Font) -> Surface:
        return font.render("[Press Any Key]", True, (255, 255, 0))

    def update(self, now, *args):
        if self.timer.check_tick(now):
            self.blink = not self.blink
        self.image = self.raw_image if self.blink else self.null_image
