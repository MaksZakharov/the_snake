# the_snake/game.py

import sys

import pygame

from the_snake.apple import Apple
from the_snake.constants import (BOARD_BACKGROUND_COLOR, DOWN, GRID_COLOR,
                                 GRID_SIZE, HIGHSCORE_POSITION, LEFT, RIGHT,
                                 SCORE_POSITION, SCREEN_HEIGHT, SCREEN_WIDTH,
                                 SPEED, UP)
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
            draw_grid(self.screen)

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
                font_big = pygame.font.Font(None, 32)
                lines = [
                    "Игра окончена!",
                    "Нажмите R для рестарта"
                ]
                for i, line in enumerate(lines):
                    text_surface = font_big.render(line, True, (220, 20, 60))
                    text_rect = text_surface.get_rect(center=(
                        SCREEN_WIDTH // 2,
                        SCREEN_HEIGHT // 2 + i * 40  # отступ между строками
                    ))
                    self.screen.blit(text_surface, text_rect)

            pygame.display.update()


def draw_grid(screen):
    """Рисует сетку на игровом поле."""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
