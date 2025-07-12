# the_snake/game.py

import sys

import pygame

from the_snake.apple import Apple
from the_snake.constants import (BOARD_BACKGROUND_COLOR, DOWN,
                                 GAME_OVER_POSITION, HIGHSCORE_POSITION, LEFT,
                                 RIGHT, SCORE_POSITION, SCREEN_HEIGHT,
                                 SCREEN_WIDTH, SPEED, UP)
from the_snake.snake import Snake
from the_snake.utils import draw_text, load_high_score, save_high_score


class Game:
    """Основной класс игры 'Змейка'."""

    def __init__(self):
        """Инициализирует окно игры, объекты, счёт и настройки."""
        pygame.init()
        pygame.display.set_caption("Змейка")

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.snake = Snake()
        self.apple = Apple(set(self.snake.positions))
        self.score = 0
        self.high_score = load_high_score()
        self.speed = SPEED

    def handle_keys(self):
        """
        Обрабатывает нажатия клавиш:
        - Стрелки: управление змейкой
        - R: рестарт игры после окончания
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit("Пользователь закрыл окно.")
            elif event.type == pygame.KEYDOWN:
                if self.snake.alive:
                    if event.key == pygame.K_UP:
                        self.snake.update_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.update_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.update_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.update_direction(RIGHT)
                else:
                    if event.key == pygame.K_r:
                        self.reset()

    def reset(self):
        """Сбрасывает игру: змейку, очки, скорость и позицию яблока."""
        self.snake.reset()
        self.apple.randomize_position(set())
        self.score = 0
        self.speed = SPEED

    def run(self):
        """Основной игровой цикл."""
        while True:
            self.clock.tick(self.speed)
            self.handle_keys()
            self.screen.fill(BOARD_BACKGROUND_COLOR)

            if self.snake.alive:
                self.snake.move()

                if (self.snake.get_head_position()
                        in self.snake.positions[4:]):
                    self.snake.alive = False
                    save_high_score(
                        max(self.score, self.high_score)
                    )

                elif (self.snake.get_head_position()
                      == self.apple.position):
                    self.snake.grow()
                    self.apple.randomize_position(
                        set(self.snake.positions)
                    )
                    self.score += 1
                    self.speed = SPEED + self.score // 5

                self.snake.draw(self.screen)
                self.apple.draw(self.screen)
                draw_text(
                    self.screen, f"Score: {self.score}",
                    (SCORE_POSITION), self.font
                )
                draw_text(
                    self.screen, f"High: {self.high_score}",
                    HIGHSCORE_POSITION, self.font
                )

            else:
                draw_text(
                    self.screen,
                    "Игра окончена! Нажмите R для рестарта",
                    GAME_OVER_POSITION,
                    self.font,
                    center=True
                )

            pygame.display.update()
