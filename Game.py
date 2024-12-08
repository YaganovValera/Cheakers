import pygame

import board
import checkers
import info
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
        self.info = info.Info(self.screen)

    def run_game(self):
        while self.running:
            self.handle_events()
            self.render()
            self.check_game_over()
            self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.info.is_button_clicked(event):
                self.checkers.check_end_move()
            self.checkers.handle_events(event)

    def render(self):
        self.board.draw_board()
        self.checkers.draw_checkers()
        self.info.draw_info(self.checkers)
        pygame.display.flip()

    def check_game_over(self):
        self.checkers.check_end_game()
        if self.checkers.game_over_black is not None and self.checkers.game_over_white is not None:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # Пользователь закрыл окно
                        self.running = False
                        return
                self.render()                      # Отрисовываем результаты на экране
                pygame.display.flip()
                self.clock.tick(10)                # Ограничиваем частоту кадров до 10 FPS

