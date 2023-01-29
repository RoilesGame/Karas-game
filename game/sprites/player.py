import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from core.sprite import BaseSprite
from game.sprites.fish import Fish
from game.sprites.fisher import Fisher
from settings import DIRECT_DICT, DEFAULT_CONTROLS


class Hook(BaseSprite):
    def __init__(
            self,
            image: Surface,
            screen_rect: Rect,
            fisher: Fisher,
            font: str
    ):
        self.font = pygame.font.Font(font, 50)

        width, height = image.get_size()
        self.image = pygame.transform.scale(image, (width * 0.06, height * 0.06))

        self.base_position = [screen_rect.center[0] - 20, screen_rect.center[1] + 40]

        self.controls = DEFAULT_CONTROLS
        self.direction_stack = []
        self.speed = 1.1
        self.counter = 0
        self._render_counter()

        self.action_state = "normal"
        self.catching_state = False
        self.direction = None
        self.screen_rect = screen_rect
        self.objects = []
        self.fisher = fisher

        super().__init__(
            pos=self.base_position,
            size=(width * 0.06, height * 0.06)
        )

    def add_direction(self, key):
        if key in self.controls:
            direction = self.controls[key]
            if direction in self.direction_stack:
                self.direction_stack.remove(direction)
            self.direction_stack.append(direction)

    def pop_direction(self, key):
        if key in self.controls:
            direction = self.controls[key]
            if direction in self.direction_stack:
                self.direction_stack.remove(direction)

    def check_out_of_bounds(self):
        width = self.screen_rect.width - 23
        return any([
            self.direction == "left" and self.exact_position[0] < 0,
            self.direction == "right" and self.exact_position[0] > width
        ])

    def move(self):
        if self.action_state == "catch" or not self.direction_stack:
            return

        self.direction = self.direction_stack[-1]

        if self.check_out_of_bounds():
            return

        vector = DIRECT_DICT[self.direction]
        self.exact_position[0] += self.speed * vector[0]
        self.exact_position[1] += self.speed * vector[1]

    def catch(self, fishes: list[Fish]):
        self.action_state = "catch"
        self.catching_state = True
        self.base_position = self.exact_position[:]
        self.objects = fishes

    def stop_catch(self):
        self.catching_state = False
        self.exact_position = self.base_position
        self.check_states()

    def next_step_catch(self):
        _, y = self.exact_position[:]
        edge = self.screen_rect.height

        if y >= edge:
            self.stop_catch()
            return

        self.exact_position[1] += 2

        for fish in self.objects:
            if pygame.sprite.collide_rect(self, fish):
                self.counter += 1
                self._render_counter()
                fish.get_caught()
                self.fisher.catch_animation()
                self.stop_catch()
                return

    def _render_counter(self):
        self.counter_text = self.font.render(str(self.counter), True, (255, 255, 255))

    def check_states(self):
        if not self.catching_state and self.action_state != "catch" and self.fisher.get_anim().done:
            return
        self.action_state = "normal"

    def update(self, now, *args):
        self.old_position = self.exact_position[:]

        if self.action_state != "catch":
            self.move()
        else:
            self.next_step_catch()
        self.rect.topleft = self.exact_position
