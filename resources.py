import os.path
from typing import Iterator

import pygame
from pygame.surface import Surface
from settings import ASSETS_PATH
import pathlib
from collections.abc import Mapping
from PIL.Image import Image


class ResourceMap(Mapping[str, Surface]):
    def __init__(self):
        # self.assets_path = pathlib.Path(os.path.join(ASSETS_PATH, "psd"))
        self.assets_path = pathlib.Path(os.path.join(ASSETS_PATH, "images"))
        self._images = dict()

    def __getitem__(self, key: str) -> Surface:
        if key not in self._images:
            raise ValueError(f"Image not found by {key}")
        return self._images[key]

    def __iter__(self) -> Iterator[str]:
        return self._images.keys()

    def __len__(self) -> int:
        return len(self._images)

    def initialize(self):
        # psd_images = [PSDImage.open(path) for path in self.assets_path.iterdir()]

        # layer: Group | PixelLayer
        # for image in psd_images:
        #     for layer in image:
        #         self._images[layer.name] = to_surface(
        #             layer.composite()
        #         )
        for path in get_paths(list(self.assets_path.iterdir())):
            image = pygame.image.load(path.absolute())

            if image.get_alpha():
                image = image.convert_alpha()
            else:
                image = image.convert()
                image.set_colorkey((255, 0, 255))
            self._images[path.stem] = image
        print(self._images)


def get_paths(paths: list[pathlib.Path]) -> list[pathlib.Path]:
    result = []
    for path in paths:
        if path.is_dir():
            result.extend(get_paths(path.iterdir()))
        else:
            result.append(path)
    return result


def make_format_name(layer_name: str, inner_layer_name: str):
    return f"{layer_name}_{inner_layer_name}"


def to_surface(file: Image, color_key=(255, 0, 255)) -> Surface:
    image = pygame.image.frombuffer(
        file.tobytes(),
        file.size,
        file.mode
    )

    if image.get_alpha():
        image = image.convert_alpha()
    else:
        image = image.convert()
        image.set_colorkey(color_key)
    return image
