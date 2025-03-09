import random

def generate_maze(width, height, extra_holes=0):
    maze = [[1] * width for _ in range(height)]  # 1 - стена, 0 - пустое место

    def is_valid(x, y):
        return 0 < x < width - 1 and 0 < y < height - 1

    def carve_path(x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if is_valid(nx, ny) and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy][x + dx] = 0
                carve_path(nx, ny)

    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0
    carve_path(start_x, start_y)

    # Добавляем случайные отверстия в стенах
    for _ in range(extra_holes):
        x = random.randint(1, width - 5)
        y = random.randint(1, height - 5)
        if maze[y][x] == 1:  # Если это стена
            maze[y][x] = 0  # Превращаем её в проход

    return maze