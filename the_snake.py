from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Черный
BORDER_COLOR = (93, 216, 228)       # Голубой
APPLE_COLOR = (255, 0, 0)           # Красный
SNAKE_COLOR = (0, 255, 0)           # Зеленый
DEFAULT_COLOR = (255, 255, 255)     # Белый

# Позиции:
ZERO_POSITION = (0, 0)
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс с игровыми объектами."""

    def __init__(self, position=ZERO_POSITION, color=DEFAULT_COLOR):
        self.position = position
        self.body_color = color

    def draw_cell(self, position=None):
        """Отрисовка ячейки на игровом поле."""
        if position is None:
            position = self.position
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Функция рисования."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_positions=None):
        if occupied_positions is None:
            occupied_positions = []
        position = self.randomize_position(occupied_positions)
        super().__init__(position, APPLE_COLOR)

    def randomize_position(self, occupied_positions):
        """Рандомизируем позицию яблока, чтобы не пересекалось со змейкой."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if new_position not in occupied_positions:
                break
        return new_position

    def draw(self):
        """Отрисовываем яблоко."""
        self.draw_cell()


class Snake(GameObject):
    """Класс змеи и её поведения."""

    def __init__(self):
        super().__init__(CENTER_POSITION, SNAKE_COLOR)
        self.reset()  # Инициализация состояния змейки

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляем направление движения змейки."""
        if (
            self.next_direction
            and self.next_direction != (-self.direction[0], -self.direction[1])
        ):
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позиции всех сегментов змейки."""
        head_x, head_y = self.get_head_position()
        new_head = (
            (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            self.draw_cell(position)

    def reset(self):
        """Сбрасывает змейку в начальное состояние после столкновения."""
        self.positions = [CENTER_POSITION]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Клавиши управления."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Инициализация PyGame"""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            apple.position = apple.randomize_position(snake.positions)

        elif snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
