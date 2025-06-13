from typing import Optional
import pygame
import sys
from constants import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple Game")
        self.clock = pygame.time.Clock()

        self.level = Level(1)
        self.global_event: Optional[pygame.Event] = None

        pygame.mouse.set_cursor(pygame.cursors.broken_x)

        self.screen_rect = self.screen.get_rect()

    def handle_event(self):
        global_event = None
        for event in pygame.event.get():
            global_event = event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.global_event = global_event

    def draw(self):
        self.screen.fill(pygame.Color("#25afa9"), self.screen_rect)
        self.level.draw(self.screen)
        pygame.display.update(self.screen_rect)

    def update(self):
        self.level.update(self.global_event)

    def run(self):
        while True:
            self.handle_event()
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
