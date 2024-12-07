from const import *
import pygame

# Загрузка изображений
IMG_WR = pygame.image.load("image/white-regular.png")
IMG_WQ = pygame.image.load("image/white-queen.png")
IMG_BR = pygame.image.load("image/black-regular.png")
IMG_BQ = pygame.image.load("image/black-queen.png")

W_R = 1
B_R = -1
W_Q = 2
B_Q = -2

MOVE_BLACK = 1
MOVE_WHITE = -1


class Class_Checkers:
    def __init__(self, screen, board):
        """
        Создание шашек и их обработка
        """
        self.screen = screen
        self.board = board
        # Флаг для отслеживания текущей стороны
        self.is_white_turn = MOVE_WHITE  # Если 1, ход белых, если -1, ход черных
        self.selected_checker = None  # Ссылка на выбранную шашку

        self.valid_moves = []  # Список допустимых ходов для выбранной шашки
        self.capture_moves = []  # Список допустимых рубок для выбранной шашки

        self.white_regular = pygame.transform.scale(IMG_WR, (SQUARE_SIZE, SQUARE_SIZE))
        self.black_regular = pygame.transform.scale(IMG_BR, (SQUARE_SIZE, SQUARE_SIZE))
        self.white_queen = pygame.transform.scale(IMG_WQ, (SQUARE_SIZE, SQUARE_SIZE))
        self.black_queen = pygame.transform.scale(IMG_BQ, (SQUARE_SIZE, SQUARE_SIZE))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, position):
        col = position[0] // SQUARE_SIZE
        row = position[1] // SQUARE_SIZE

        if self.selected_checker:                   # Если выбрана шашка
            if (row, col) in self.valid_moves:      # Если клик по допустимому ходу
                self.make_move(row, col, self.board.boards[(row+col) % 2])
            elif (row, col) in self.capture_moves:  # Если клик по допустимой рубке
                self.make_capture(row, col,  self.board.boards[(row+col) % 2])
        self.select_checker(row, col, self.board.boards[(row+col) % 2])

    def select_checker(self, row, col, board):
        if self.is_white_turn == MOVE_WHITE:            # Если ход белых
            if board[row][col] in [W_R, W_Q]:
                self.selected_checker = (row, col)
                self.highlight_moves(row, col, board)
        else:                                           # Если ход черных
            if board[row][col] in [B_R, B_Q]:
                self.selected_checker = (row, col)
                self.highlight_moves(row, col, board)

    def highlight_moves(self, row, col, board):
        """
        Подсвечивает все возможные ходы для выбранной шашки.
        """
        self.valid_moves = []
        self.capture_moves = []

        checker = board[row][col]

        # Для белой шашки
        if checker in [W_R, B_R]:  # Простая шашка
            self.check_moves(row, col, board)
        elif checker in [W_Q, B_Q]:  # Дамка
            self.check_queen_moves(row, col, board)

    def check_moves(self, row, col, board):
        """
        Проверка возможных ходов для обычной шашки.
        """
        checkers_vrags = [W_R * self.is_white_turn, W_Q * self.is_white_turn]
        directions = [1, -1]  # Вперед и назад

        for direction in directions:
            simple_move = row + direction * self.is_white_turn
            capture_move = row + 2 * direction * self.is_white_turn

            if 0 <= simple_move < ROWS:
                # Проверка для простого хода
                if col - 1 >= 0 and board[simple_move][col - 1] == 0:
                    self.valid_moves.append((simple_move, col - 1))
                if col + 1 < COLS and board[simple_move][col + 1] == 0:
                    self.valid_moves.append((simple_move, col + 1))

            if 0 <= capture_move < ROWS:
                # Проверка для рубки
                if col - 2 >= 0 and board[simple_move][col - 1] in checkers_vrags \
                        and board[capture_move][col - 2] == 0:
                    self.capture_moves.append((capture_move, col - 2))
                if col + 2 < COLS and board[simple_move][col + 1] in checkers_vrags \
                        and board[capture_move][col + 2] == 0:
                    self.capture_moves.append((capture_move, col + 2))

    def check_queen_moves(self, row, col, board):
        """
        Проверка возможных ходов для белой дамки.
        """
        # Дамка может двигаться в любом направлении по диагонали, но не может переступать клетки.
        directions = [(-1, -1), (-1, 1), (1, -1),
                      (1, 1)]  # Направления: вверх-влево, вверх-вправо, вниз-влево, вниз-вправо
        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLS:
                    if board[r][c] == 0:
                        self.valid_moves.append((r, c))
                    elif 0 <= r + dr < ROWS and 0 <= c + dc < COLS:
                        if self.is_white_turn == MOVE_WHITE and board[r][c] in [B_R, B_Q]:
                            if board[r + dr][c + dc] == 0:
                                self.capture_moves.append((r + dr, c + dc))
                        elif self.is_white_turn == MOVE_BLACK and board[r][c] in [W_R, W_Q]:
                            if board[r + dr][c + dc] == 0:
                                self.capture_moves.append((r + dr, c + dc))
                    else:
                        break
                else:
                    break

    def make_move(self, row, col, board):
        pass

    def make_capture(self, row, col, board):
        pass

    def draw_checkers(self):
        """
        Отрисовка шашек на доске.
        """
        for board_state in self.board.boards:
            for row in range(len(board_state)):
                for col in range(len(board_state[row])):
                    checker = board_state[row][col]
                    x = col * SQUARE_SIZE
                    y = row * SQUARE_SIZE

                    # Проверка подсветки выбранной шашки
                    if self.selected_checker == (row, col):
                        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)

                    # Отрисовка шашек
                    if checker == W_R:  # Белая шашка
                        self.screen.blit(self.white_regular, (x, y))
                    elif checker == B_R:  # Черная шашка
                        self.screen.blit(self.black_regular, (x, y))
                    elif checker == W_Q:  # Белая дамка
                        self.screen.blit(self.white_queen, (x, y))
                    elif checker == B_Q:  # Черная дамка
                        self.screen.blit(self.black_queen, (x, y))

        # Отрисовка возможных ходов как красные точки
        for move in self.valid_moves:
            row, col = move
            center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(self.screen, (255, 0, 0), (center_x, center_y), SQUARE_SIZE // 8)

        # Отрисовка возможных рубок как желтых точек
        for move in self.capture_moves:
            row, col = move
            center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(self.screen, (255, 255, 0), (center_x, center_y), SQUARE_SIZE // 8)
