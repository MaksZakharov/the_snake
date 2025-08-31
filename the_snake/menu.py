import pygame
import pygame_menu
import sys
import os

from the_snake.game import Game
from the_snake.constants import SCREEN_WIDTH, SCREEN_HEIGHT

player_name = "Игрок 1"

def set_player_name(value: str):
    global player_name
    player_name = value

def start_game():
    game = Game()
    game.player_name = player_name
    game.run()

def exit_game():
    pygame.quit()
    sys.exit()

def show_menu():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змейка")

    # Путь к фону
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bg_path = os.path.join(base_dir, 'the_snake', 'assets', 'background.png')

    # Загрузка и масштабирование
    background = pygame.image.load(bg_path)
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Тема
    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.title = False
    theme.widget_font_size = 32
    theme.widget_font_color = (255, 255, 255)
    theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER

    # Меню: нижняя половина экрана, по центру
    menu = pygame_menu.Menu(
        height=SCREEN_HEIGHT // 2,
        width=SCREEN_WIDTH - 80,
        theme=theme,
        title='',  # без заголовка
        center_content=True  # центрирует кнопки
    )

    menu.add.text_input('Имя: ', default='Игрок 1', onchange=set_player_name)
    menu.add.button('▶ Играть', start_game)
    menu.add.button('❌ Выход', exit_game)

    # Цикл отрисовки
    while True:
        surface.blit(background, (0, 0))

        # Вручную размещаем меню в нижней части
        menu_rect = menu.get_rect()
        menu_rect.midtop = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
        menu._position = menu_rect.topleft  # Переопределяем позицию

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit_game()

        menu.update(events)
        menu.draw(surface)
        pygame.display.flip()
