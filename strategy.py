import random

class Strategy:
    def __init__(self, length=20):
        self.moves = [random.choice(["up", "down", "left", "right"]) for _ in range(length)]
        self.fitness = 0  # Фитнес-функция для оценки эффективности стратегии

    def mutate(self, mutation_rate=0.1):
        """Вносит мутации в стратегию"""
        for i in range(len(self.moves)):
            if random.random() < mutation_rate:
                self.moves[i] = random.choice(["up", "down", "left", "right"])

    def crossover(self, other):
        """Смешивает две стратегии"""
        split_point = random.randint(0, len(self.moves))
        child_moves = self.moves[:split_point] + other.moves[split_point:]
        return Strategy(length=len(child_moves))