import random

import pygame

from the_snake.constants import APPLE_COLOR, GRID_HEIGHT, GRID_SIZE, GRID_WIDTH
from the_snake.game_object import GameObject


class Apple(GameObject):
    """Класс, представляющий яблоко на игровом поле."""

    def __init__(self, occupied_positions=None, color=APPLE_COLOR):
        """
        Инициализирует яблоко, размещая его в случайной свободной позиции.

        :param occupied_positions: Набор занятых координат,
        чтобы избежать коллизий.
        :param color: Цвет яблока.
        """
        super().__init__(body_color=color)
        if occupied_positions is None:
            occupied_positions = set()
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """
        Назначает новое случайное положение яблока,
        не попадающее на занятые клетки.

        :param occupied_positions: Множество координат, занятых змейкой.
        """
        while True:
            self.position = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in occupied_positions:
                break

    def draw(self, surface):
        """
        Отображает яблоко на переданной поверхности.

        :param surface: Экран или поверхность Pygame,
        на которой рисуется яблоко.
        """
        pygame.draw.rect(
            surface, self.body_color,
            (*self.position, GRID_SIZE, GRID_SIZE)
        )
