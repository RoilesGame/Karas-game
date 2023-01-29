import pygame


class BaseSprite(pygame.sprite.Sprite):
    """
    A very basic base class that contains some commonly used functionality.
    """
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)
        self.rect = pygame.Rect(pos, size)
        self.exact_position = list(self.rect.topleft)
        self.old_position = self.exact_position[:]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
