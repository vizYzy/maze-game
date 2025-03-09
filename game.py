import pygame
from maze_generator import generate_maze
from player import Player
from bot import Bot
from ui import draw_ui
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, WHITE, BLACK, TIME_LIMIT, MOVE_SPEED
from genetic_algorithm import evaluate_strategies, select_parents, create_next_generation


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Лови бота!")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    running = True
    attempts = 1
    population_size = 10  # Размер популяции ботов
    mutation_rate = 0.1  # Вероятность мутации
    bots = []  # Популяция ботов для обучения

    while running:
        # Генерация нового лабиринта для каждого раунда
        maze = generate_maze(GRID_WIDTH, GRID_HEIGHT, extra_holes=30)

        # Выбираем лучшего бота из предыдущего поколения
        best_bot = max(bots, key=lambda bot: getattr(bot, 'time_alive', 0), default=None)
        if best_bot:
            bot = Bot(maze, color=(0, 255, 0))  # Используем лучшего бота для игры
            bot.maze = maze  # Обновляем лабиринт для бота
        else:
            bot = Bot(maze)  # Создаем нового бота, если популяция пуста

        player = Player(1, 1)  # Создаем игрока
        start_time = pygame.time.get_ticks()  # Засекаем время начала раунда
        caught_bot = False  # Флаг для отслеживания поимки бота

        while not caught_bot and running:
            current_time = pygame.time.get_ticks()
            time_left = max(0, TIME_LIMIT - (current_time - start_time) // 1000)

            # Проверяем, истекло ли время
            if time_left == 0:
                caught_bot = True  # Время вышло, завершаем раунд
                break

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    caught_bot = True  # Завершаем раунд по нажатию пробела
                    break

            # Получаем состояние клавиш
            keys = pygame.key.get_pressed()
            directions = {
                "up": keys[pygame.K_UP],
                "down": keys[pygame.K_DOWN],
                "left": keys[pygame.K_LEFT],
                "right": keys[pygame.K_RIGHT]
            }

            # Движение игрока и бота
            collision = player.move(directions, maze, current_time, MOVE_SPEED, bot)
            bot.move(maze, player.x, player.y, current_time, MOVE_SPEED)

            # Проверяем столкновение
            if collision or (player.x, player.y) == (bot.x, bot.y):
                caught_bot = True  # Игрок поймал бота
                break

            # Отрисовка экрана
            screen.fill(WHITE)

            # Отрисовка лабиринта
            for y, row in enumerate(maze):
                for x, cell in enumerate(row):
                    color = BLACK if cell == 1 else WHITE
                    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            # Отрисовка игрока и бота
            player.draw(screen, CELL_SIZE)
            bot.draw(screen, CELL_SIZE)

            # Отрисовка UI (время и попытки)
            draw_ui(screen, font, time_left, attempts, GRID_WIDTH, CELL_SIZE)

            pygame.display.flip()
            clock.tick(30)  # Ограничиваем FPS до 30

        # Если игра завершилась (по времени, поимке бота или нажатию пробела)
        if running:
            # Сохраняем время жизни текущего бота
            bot.time_alive = time_left
            bots.append(bot)  # Добавляем бота в популяцию

            # Показываем сообщение о результате
            if time_left > 0:
                message = "Вы поймали бота!"
            else:
                message = "Время вышло!"

            screen.fill(WHITE)
            text_message = font.render(message, True, BLACK)
            text_restart = font.render("Нажмите пробел, чтобы начать новую попытку", True, BLACK)
            screen.blit(text_message, (SCREEN_WIDTH // 2 - text_message.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(text_restart, (SCREEN_WIDTH // 2 - text_restart.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
            pygame.display.flip()

            # Генетический алгоритм
            evaluate_strategies(bots)
            parents = select_parents(bots, population_size // 2)
            new_strategies = create_next_generation(parents, population_size, mutation_rate)

            # Обновляем стратегии для ботов
            for bot, strategy in zip(bots, new_strategies):
                bot.set_strategy(strategy)

            # Ожидание нажатия пробела для рестарта
            waiting_for_restart = True
            while waiting_for_restart and running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        waiting_for_restart = False

            if running:
                attempts += 1  # Увеличиваем счетчик попыток

    pygame.quit()