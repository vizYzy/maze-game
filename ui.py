def draw_ui(screen, font, time_left, attempts, grid_width, cell_size):
    text_time = font.render(f"Время: {time_left}", True, (0, 0, 0))
    text_attempts = font.render(f"Попытка: {attempts}", True, (0, 0, 0))

    screen.blit(text_time, (grid_width * cell_size + 20, 20))
    screen.blit(text_attempts, (grid_width * cell_size + 20, 60))