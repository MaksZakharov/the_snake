"""Модуль, содержащий класс Snake — игрового персонажа змейки."""

import random

import pygame

from the_snake.constants import (BORDER_COLOR, DOWN, GRID_SIZE, LEFT, RIGHT,
                                 SCREEN_HEIGHT, SCREEN_WIDTH, SNAKE_COLOR,
                                 START_POSITION_SNAKE, UP)
from the_snake.game_object import GameObject


class Snake(GameObject):
    """Класс, управляющий поведением и состоянием змейки."""

    def __init__(self, position=START_POSITION_SNAKE, color=SNAKE_COLOR):
        """
        Инициализирует змейку с начальной позицией и цветом.

        Аргументы:
            position (tuple): начальная позиция.
            color (tuple): цвет сегментов змейки.
        """
        super().__init__(position, color)
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [self.position]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.growing = False
        self.alive = True

    def move(self):
        """Перемещает змейку в текущем направлении."""
        if not self.alive:
            return

        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        if not self.growing:
            self.positions.pop()
        else:
            self.growing = False

    def grow(self):
        """Увеличивает длину змейки после поедания яблока."""
        self.growing = True

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.

        Возврат:
            tuple: координаты головы.
        """
        return self.positions[0]

    def update_direction(self, new_direction):
        """
        Обновляет направление движения змейки.

        Аргументы:
            new_direction (tuple): новое направление.
        """
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def draw(self, surface):
        """
        Отображает змейку на экране.

        Аргументы:
            surface (pygame.Surface): поверхность для отрисовки.
        """
        for segment in self.positions:
            pygame.draw.rect(
                surface, self.body_color,
                (*segment, GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(
                surface, BORDER_COLOR,
                (*segment, GRID_SIZE, GRID_SIZE), 1
            )
