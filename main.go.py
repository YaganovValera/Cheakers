import pygame
import sys

from const import *
import Game


# Опции меню
MENU_OPTIONS = ["Новая игра", "Выход"]
OPTION_NEW_GAME = 0
OPTION_EXIST = 1

selected_option = OPTION_NEW_GAME                               # Индекс выбранного пункта


def draw_menu(screen, font):
    global selected_option
    """Функция для отрисовки меню."""
    screen.fill(WHITE)  # Очистка экрана
    title = font.render("Меню", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))      # Заголовок

    for i, option in enumerate(MENU_OPTIONS):
        color = BLUE if i == selected_option else BLACK
        text_surface = font.render(option, True, color)
        x = (WIDTH - text_surface.get_width()) // 2
        y = HEIGHT // 2 + i * 60
        screen.blit(text_surface, (x, y))


def get_option_at_pos(pos, font):
    """Определяет, на какую опцию в меню нажали."""
    x, y = pos
    for i, option in enumerate(MENU_OPTIONS):
        text_surface = font.render(option, True, BLACK)
        option_x = (WIDTH - text_surface.get_width()) // 2
        option_y = HEIGHT // 2 + i * 60
        if option_x <= x <= option_x + text_surface.get_width() and option_y <= y <= option_y + text_surface.get_height():
            return i
    return None


def main():
    global selected_option

    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Шашки Вигмана")

    # Шрифт
    font = pygame.font.Font(None, 50)

    # Главный цикл меню
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Обработка нажатий мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_option = get_option_at_pos(event.pos, font)
                if clicked_option is not None:
                    selected_option = clicked_option
                    if selected_option == OPTION_NEW_GAME:
                        game = Game.Class_Game()
                        game.run_game()
                    elif selected_option == OPTION_EXIST:
                        running = False

        draw_menu(screen, font)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
