import random
from strategy import Strategy

def evaluate_strategies(bots):
    """Оценивает стратегии всех ботов на основе времени жизни"""
    total_time_alive = sum(bot.time_alive for bot in bots)
    for bot in bots:
        bot.strategy.fitness = bot.time_alive / total_time_alive if total_time_alive > 0 else 0

def select_parents(population, num_parents):
    """Выбирает лучших родителей для следующего поколения"""
    sorted_population = sorted(population, key=lambda bot: bot.strategy.fitness, reverse=True)
    return sorted_population[:num_parents]

def create_next_generation(parents, population_size, mutation_rate=0.1):
    """Создает новое поколение стратегий"""
    next_generation = []
    while len(next_generation) < population_size:
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child_strategy = parent1.strategy.crossover(parent2.strategy)
        child_strategy.mutate(mutation_rate)
        next_generation.append(child_strategy)
    return next_generation