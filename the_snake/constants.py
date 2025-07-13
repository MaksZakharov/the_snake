# the_snake/constants.py

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 640
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
GRID_COLOR = (200, 200, 200)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (240, 240, 235)
BORDER_COLOR = (180, 160, 140)
APPLE_COLOR = (220, 20, 60)
SNAKE_COLOR = (50, 205, 50)
TEXT_COLOR = (40, 40, 40)

# Скорость змейки
SPEED = 10

# Начальные позиции
START_POSITION_SNAKE = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
DEFAULT_POSITION = (0, 0)

# Позиция текста "Игра окончена"
GAME_OVER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Путь к файлу с рекордом
HIGHSCORE_FILE = "highscore.txt"

# Размер шрифта
FONT_SIZE = 36

# Расположение счёта
SCORE_POSITION = (10, 10)
HIGHSCORE_POSITION = (350, 10)
