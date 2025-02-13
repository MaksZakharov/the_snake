import random

import sys

import pygame

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
TEXT_COLOR = (255, 255, 255)

# Скорость змейки
SPEED = 10

# Игровое окно
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Время
clock = pygame.time.Clock()

# Начальные позиции
START_POSITION_SNAKE = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
DEFAULT_POSITION = (0, 0)

# Позиция текста "Игра окончена"
GAME_OVER_POSITION = (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2)


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(
        self, position: tuple = DEFAULT_POSITION,
        body_color: tuple = TEXT_COLOR
    ):
        """Инициализирует объект с позицией и цветом."""
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Метод отрисовки объекта (должен быть переопределён)."""
        raise NotImplementedError(
            f"Метод draw() не переопределен в классе {self.__class__.__name__}"
        )


class Apple(GameObject):
    """Представляет собой яблоко на игровом поле."""

    def __init__(self, occupied_positions: set = None, color=APPLE_COLOR):
        """Создает яблоко в случайной позиции, не попадая на змейку."""
        if occupied_positions is None:
            occupied_positions = set()
        self.randomize_position(occupied_positions)
        super().__init__(body_color=color)

    def randomize_position(self, occupied_positions: set) -> tuple:
        """Генерирует случайную позицию яблока."""
        while True:
            new_position = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self) -> None:
        """Отображает яблоко на экране."""
        pygame.draw.rect(
            screen, self.body_color, (*self.position, GRID_SIZE, GRID_SIZE)
        )


class Snake(GameObject):
    """Класс, управляющий поведением змейки в игре."""

    def __init__(self, position=START_POSITION_SNAKE, color=SNAKE_COLOR):
        """Инициализирует змейку в центре экрана."""
        super().__init__(position, color)
        self.reset()

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [self.position]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.growing = False
        self.alive = True

    def move(self) -> None:
        """Передвигает змейку в текущем направлении."""
        if not self.alive:
            return

        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)
        if not self.growing:
            self.positions.pop()
        else:
            self.growing = False

    def grow(self) -> None:
        """Увеличивает змейку после съедения яблока."""
        self.growing = True

    def get_head_position(self) -> tuple:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction: tuple) -> None:
        """Обновляет направление движения змейки."""
        if (
            (new_direction == UP and self.direction != DOWN)
            or (new_direction == DOWN and self.direction != UP)
            or (new_direction == LEFT and self.direction != RIGHT)
            or (new_direction == RIGHT and self.direction != LEFT)
        ):
            self.direction = new_direction

    def draw(self) -> None:
        """Отображает змейку на экране."""
        for segment in self.positions:
            pygame.draw.rect(
                screen, self.body_color, (*segment, GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(
                screen, BORDER_COLOR, (*segment, GRID_SIZE, GRID_SIZE), 1
            )


def handle_keys(snake: Snake) -> None:
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit("Пользователь закрыл окно.")
        elif event.type == pygame.KEYDOWN:
            if snake.alive:
                if event.key == pygame.K_UP:
                    snake.update_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.update_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.update_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.update_direction(RIGHT)
            else:
                if event.key == pygame.K_r:
                    snake.reset()


def main() -> None:
    """Основная функция игры, запускает игровой цикл."""
    pygame.init()
    pygame.display.set_caption("Змейка")
    font = pygame.font.Font(None, 36)

    def draw_text(text: str, position: tuple) -> None:
        """Отображает текст на экране."""
        text_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surface, position)

    snake = Snake()
    apple = Apple(set(snake.positions))  # Передаём список занятых клеток

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)

        if snake.alive:
            snake.move()

            # Проверяем, не врезалась ли змейка в саму себя
            if snake.get_head_position() in snake.positions[4:]:
                snake.alive = False

            # Проверяем, съела ли змейка яблоко
            elif snake.get_head_position() == apple.position:
                snake.grow()
                apple.randomize_position(set(snake.positions))

            snake.draw()
            apple.draw()
        else:
            draw_text(
                "Игра окончена! Нажмите R для рестарта",
                GAME_OVER_POSITION,
            )

        pygame.display.update()


if __name__ == "__main__":
    main()
