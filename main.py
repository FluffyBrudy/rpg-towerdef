import pygame
import sys
from constants import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple Game")
        self.clock = pygame.time.Clock()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def update(self):
        pass

    def run(self):
        while True:
            self.handle_event()
            self.update()
            self.draw()
            self.clock.tick(FPS)


class Pacman:
    pass


if __name__ == "__main__":
    game = Game()
