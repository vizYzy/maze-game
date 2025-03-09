import pygame
from strategy import Strategy
import random

class Bot:
    def __init__(self, maze, color=(0, 0, 255)):
        self.maze = maze
        self.x, self.y = self.find_empty_cell()
        self.color = color
        self.strategy = Strategy()  # Начальная случайная стратегия
        self.time_alive = 0  # Добавляем атрибут для отслеживания времени жизни
        self.last_move_time = 0  # Время последнего хода
        self.path = []  # Список для хранения пути бота

    def find_empty_cell(self):
        while True:
            x = random.randint(1, len(self.maze[0]) - 2)
            y = random.randint(1, len(self.maze) - 2)
            if self.maze[y][x] == 0:
                return x, y

    def calculate_path(self, maze, player_x, player_y, steps=10):
        """Рассчитывает путь бота на 10 шагов вперед"""
        path = []
        current_x, current_y = self.x, self.y

        for _ in range(steps):
            # Вычисляем текущее расстояние до игрока
            current_distance = abs(current_x - player_x) + abs(current_y - player_y)

            best_move = None
            max_distance = current_distance

            # Проверяем все возможные направления
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            for dx, dy in directions:
                new_x, new_y = current_x + dx, current_y + dy

                # Проверяем, что новая позиция допустима
                if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and maze[new_y][new_x] == 0:
                    new_distance = abs(new_x - player_x) + abs(new_y - player_y)
                    if new_distance > max_distance:
                        max_distance = new_distance
                        best_move = (dx, dy)

            # Если найден лучший ход, добавляем его в путь
            if best_move:
                current_x += best_move[0]
                current_y += best_move[1]
                path.append((current_x, current_y))
            else:
                break  # Если бот застрял, прерываем расчет пути

        return path

    def move(self, maze, player_x, player_y, current_time, move_speed=1):
        # Проверяем, прошло ли достаточно времени для следующего хода
        if current_time - self.last_move_time < 1000 / move_speed:
            return

        self.last_move_time = current_time

        # Рассчитываем путь на 10 шагов вперед
        self.path = self.calculate_path(maze, player_x, player_y, steps=10)

        # Выполняем первый шаг из пути
        if self.path:
            self.x, self.y = self.path[0]

    def draw(self, screen, cell_size):
        # Отрисовываем бота
        pygame.draw.rect(screen, self.color, (self.x * cell_size, self.y * cell_size, cell_size, cell_size))

        # Отрисовываем путь бота в виде сплошной линии
        if len(self.path) > 1:
            # Преобразуем координаты пути в пиксельные координаты
            pixel_path = [(x * cell_size + cell_size // 2, y * cell_size + cell_size // 2) for (x, y) in self.path]
            pygame.draw.lines(screen, (255, 0, 0), False, pixel_path, 3)  # Рисуем сплошную линию

    def set_strategy(self, strategy):
        """Устанавливает новую стратегию для бота"""
        self.strategy = strategy