# the_snake/utils.py

import os

import pygame

from the_snake.constants import FONT_SIZE, HIGHSCORE_FILE, TEXT_COLOR


def draw_text(surface, text, position, font=None,
              color=TEXT_COLOR, center=False):
    """
    Отображает текст на экране.

    Args:
        surface: Поверхность для отрисовки.
        text (str): Отображаемый текст.
        position (tuple): Позиция текста на экране.
        font (pygame.font.Font, optional): Шрифт.
        color (tuple, optional): Цвет текста.
        center (bool, optional): Центрировать ли текст.
    """
    if font is None:
        font = pygame.font.Font(None, FONT_SIZE)
    text_surface = font.render(text, True, color)

    if center:
        rect = text_surface.get_rect(center=position)
        surface.blit(text_surface, rect.topleft)
    else:
        surface.blit(text_surface, position)


def load_high_score():
    """
    Загружает рекорд из файла.

    Returns:
        int: Значение рекорда.
    """
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip() or 0)
    return 0


def save_high_score(score):
    """
    Сохраняет рекорд в файл.

    Args:
        score (int): Счёт, который нужно сохранить.
    """
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))
