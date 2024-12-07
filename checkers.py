from const import *
import pygame

# Загрузка изображений
IMG_WR = pygame.image.load("image/white-regular.png")
IMG_WQ = pygame.image.load("image/white-queen.png")
IMG_BR = pygame.image.load("image/black-regular.png")
IMG_BQ = pygame.image.load("image/black-queen.png")


class Class_Checkers:
    def __init__(self, screen, board):
        # Масштабирование изображений под размер клетки
        self.screen = screen
        self.board = board
        # Флаг для отслеживания текущей стороны
        self.is_white_turn = True  # Если True, ход белых, если False, ход черных
        self.selected_checker = None  # Ссылка на выбранную шашку

        self.white_regular = pygame.transform.scale(IMG_WR, (SQUARE_SIZE, SQUARE_SIZE))
        self.black_regular = pygame.transform.scale(IMG_BR, (SQUARE_SIZE, SQUARE_SIZE))
        self.white_queen = pygame.transform.scale(IMG_WQ, (SQUARE_SIZE, SQUARE_SIZE))
        self.black_queen = pygame.transform.scale(IMG_BQ, (SQUARE_SIZE, SQUARE_SIZE))

    def draw_checkers(self):
        """
        Отрисовка шашек на доске.
        """
        for board_state in [self.board.board_white, self.board.board_black]:
            for row in range(len(board_state)):
                for col in range(len(board_state[row])):
                    checker = board_state[row][col]
                    x = col * SQUARE_SIZE
                    y = row * SQUARE_SIZE

                    # Проверка подсветки выбранной шашки
                    if self.selected_checker == (row, col):
                        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)  # Красная обводка

                    if checker == 1:  # Белая шашка
                        self.screen.blit(self.white_regular, (x, y))
                    elif checker == 2:  # Черная шашка
                        self.screen.blit(self.black_regular, (x, y))
                    elif checker == 3:  # Белая дамка
                        self.screen.blit(self.white_queen, (x, y))
                    elif checker == 4:  # Черная дамка
                        self.screen.blit(self.black_queen, (x, y))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, position):
        col = position[0] // SQUARE_SIZE
        row = position[1] // SQUARE_SIZE

        if self.is_white_turn:  # Если ход белых
            if self.board.board_white[row][col] == 1 or self.board.board_white[row][col] == 3\
                    or self.board.board_black[row][col] == 1 or self.board.board_black[row][col] == 3:
                self.selected_checker = (row, col)
        else:  # Если ход черных
            if self.board.board_black[row][col] == 2 or self.board.board_black[row][col] == 4\
                    or self.board.board_white[row][col] == 2 or self.board.board_white[row][col] == 4:
                self.selected_checker = (row, col)

