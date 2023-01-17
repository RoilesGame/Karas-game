import pygame


pygame.init()


class GameParameters:
    height = 700
    width = 500
    game_name = "Karas' Game"


class Game(GameParameters):
    def start_game(self):
        pygame.display.set_mode((self.height, self.width))
        pygame.display.set_caption(self.game_name)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()


game = Game()
game.start_game()

pygame.quit()
