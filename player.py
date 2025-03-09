import pygame

class Player:
    def __init__(self, x, y, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.color = color
        self.last_move_time = 0  # Время последнего хода

    def move(self, keys, maze, current_time, move_speed=1, bot=None):
        # Проверяем, прошло ли достаточно времени для следующего хода
        if current_time - self.last_move_time < 1000 / move_speed:
            return

        self.last_move_time = current_time

        new_x, new_y = self.x, self.y

        if keys["up"] and maze[self.y - 1][self.x] == 0:
            new_y -= 1
        elif keys["down"] and maze[self.y + 1][self.x] == 0:
            new_y += 1
        elif keys["left"] and maze[self.y][self.x - 1] == 0:
            new_x -= 1
        elif keys["right"] and maze[self.y][self.x + 1] == 0:
            new_x += 1

        # Проверяем, чтобы игрок не мог зайти на клетку бота
        if bot and (new_x, new_y) == (bot.x, bot.y):
            # Если игрок пытается зайти на клетку бота, считаем это столкновением
            return True  # Возвращаем True, чтобы сигнализировать о столкновении

        # Если столкновения нет, обновляем позицию игрока
        self.x, self.y = new_x, new_y
        return False  # Возвращаем False, если столкновения не было

    def draw(self, screen, cell_size):
        pygame.draw.rect(screen, self.color, (self.x * cell_size, self.y * cell_size, cell_size, cell_size))