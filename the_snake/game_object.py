# the_snake/game_object.py

from the_snake.constants import DEFAULT_POSITION, TEXT_COLOR


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
            f'Метод draw() не переопределен в классе {self.__class__.__name__}'
        )
