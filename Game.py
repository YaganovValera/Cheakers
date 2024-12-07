import pygame

import board
import checkers
from const import *


class Class_Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Инициализация компонентов игры
        self.board = board.Class_Board(self.screen)
        self.checkers = checkers.Class_Checkers(self.screen, self.board)

    def run_game(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.check_game_over()
            self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.checkers.handle_events(event)

    def update(self):
        pass

    def render(self):
        self.board.draw_board()
        self.checkers.draw_checkers()
        pygame.display.flip()

    def check_game_over(self):
        pass
