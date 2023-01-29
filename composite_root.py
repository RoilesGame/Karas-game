import pygame

from core.animate import Animation
from game.sprites.background import Background, CompositeBackground, Hut, Water, WaterLine, Boat, Reeds
from game.sprites.fish import Fish
from game.sprites.fisher import Fisher
from game.sprites.player import Hook
from game.sprites.title import TitleSprite
from game.states.game import Game
from game.states.splash import Splash
from game.states.title import Title
from resources import ResourceMap
from settings import (
    CAPTION,
    SCREEN_SIZE,
    BACKGROUND_COLOR,
    FONT_PATH
)

pygame.init()


def create_fish(animation_fist: str, animation_second: str, root: 'CompositeRoot') -> Fish:
    fish_right_anim = [
        root.resource_map[animation_fist],
        root.resource_map[animation_second]
    ]
    fish_left_anim = [
        pygame.transform.flip(root.resource_map[animation_fist], True, False),
        pygame.transform.flip(root.resource_map[animation_second], True, False)
    ]
    return Fish(
        screen_rect=root.screen_rect,
        animations={"swim": {"left": Animation(fish_left_anim, 2), "right": Animation(fish_right_anim, 2)}},
        size=root.resource_map[animation_fist].get_size()
    )


class CompositeRoot:
    def __init__(
        self,
        caption: str,
        screen_size: (int, int),
        background_color: (int, int, int),
        font: str,
        resource_map: ResourceMap
    ):
        pygame.display.set_caption(caption)
        self.background_color = background_color
        self.screen_size = screen_size
        self.font = font
        self.screen_rect = pygame.Rect((0, 0), self.screen_size)
        self.screen = pygame.display.set_mode(screen_size)
        self.resource_map = resource_map

    def initialize(self) -> None:
        self.screen.fill(self.background_color)
        font = pygame.font.Font(self.font, 100)
        render = font.render("LOADING...", 0, pygame.Color("white"))
        self.screen.blit(render, render.get_rect(center=self.screen_rect.center))
        self.resource_map.initialize()

    def states(self):
        water_line = WaterLine(
            image=self.resource_map["NativeWater"],
            screen_rect=composite_root.screen_rect,
            amount=8
        )

        default_frames = [
            self.resource_map["Character_animation_1"],
            self.resource_map["Character_animation_1_2"],
            self.resource_map["Character_animation_1_3"],
            self.resource_map["Character_animation_1_4"],
        ]
        hook_frames = [
            self.resource_map["Character_animation_2"],
            self.resource_map["Character_animation_3"],
            self.resource_map["Character_animation_4"],
            self.resource_map["Character_animation_5"],
        ]
        check_frames = [
            self.resource_map["Character_animation_6"]
        ]

        fisher_animations = {
            "normal": Animation(default_frames, 8),
            "catch": Animation(
                hook_frames + check_frames * 4 + list(reversed(hook_frames)), 5, loops=1
            ),
        }
        fisher = Fisher(
            x=242, y=232,
            animations=fisher_animations
        )

        background = CompositeBackground(
            background=Background(self.resource_map["Background"], composite_root.screen_rect),
            hut=Hut(self.resource_map["Fishing_hut"]),
            water=water_line,
            boat=Boat(self.resource_map["Boat"]),
            reeds=[
                Reeds(self.resource_map["Grass2"], 700, 272),
                Reeds(self.resource_map["Grass3"], 755, 272)
            ],
            fisher=fisher
        )
        title = TitleSprite(
            image=self.resource_map["Title"],
            screen_rect=self.screen_rect
        )
        fish_animations = [
            ("2_1", "2_2"), ("3_1", "3_2"), ("4_1", "4_2"), ("5_1", "5_2"),
            ("6_1", "6_2"), ("7_1", "7_2"), ("8_1", "8_2")
        ]
        fishes = [
            create_fish(*anim, self) for anim in fish_animations
        ]
        hook = Hook(
            screen_rect=self.screen_rect,
            image=self.resource_map["Hook"],
            fisher=fisher,
            font=self.font
        )

        states = {
            "SPLASH": Splash(
                image=self.resource_map["Splash"],
                screen_rect=self.screen_rect
            ),
            "TITLE": Title(
                screen_rect=self.screen_rect,
                font=self.font,
                background=background,
                title=title,
                fishes=fishes
            ),
            "GAME": Game(
                screen_rect=self.screen_rect,
                font=self.font,
                background=background,
                player=hook,
                fishes=fishes
            )
        }
        return states


composite_root = CompositeRoot(
    caption=CAPTION,
    screen_size=SCREEN_SIZE,
    background_color=BACKGROUND_COLOR,
    font=FONT_PATH,
    resource_map=ResourceMap()
)
