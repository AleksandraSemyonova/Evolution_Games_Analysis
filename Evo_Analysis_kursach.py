import random
import matplotlib.pyplot as plt
import time

start = time.time()

V = 15              # ценность ресурса
C = 20          # цена травмы 
POP_SIZE = 1000      # размер популяции
GENERATIONS = 100        # число поколений
MATCHES = 150 

#Задаем любой размер популяции
population = ['H'] * (POP_SIZE //2) + ['D'] * (POP_SIZE // 2)
stats = {'H': [], 'D': []}

def play_match(p1, p2):
    if p1 == 'H' and p2 == 'H':
        return (V, -C) if random.random() < 0.5 else (-C, V)
    elif p1 == 'H':
        return V, 0              # Ястреб забирает ресурс
    elif p2 == 'H':
        return 0, V              # Ястреб забирает ресурс
    else:
        return V/2, V/2          # Голуби делят поровну

def calculate_fitness(pop):     #Очки особи за поколение +моделирует одну встречу двух особей и возвращает, сколько очков получила каждая.
    scores = [0] * len(pop)
    for i, player in enumerate(pop):
        for _ in range(MATCHES):
            opponent = random.choice(pop)
            score, _ = play_match(player, opponent)
            scores[i] += score
    return scores

def select_next_generation(pop, scores):                # Сдвигаем очки, чтобы все были > 0 и строим новую популяцию
    min_score = min(scores)
    fitness = [s - min_score + 1 for s in scores]  # +1 избегаем деления на 0 
    new_population = []
    for _ in range(POP_SIZE):
        chosen = random.choices(pop, weights=fitness, k=1)
        new_population.append(chosen[0])  
    return new_population

for gen in range(GENERATIONS):
    scores = calculate_fitness(population)
    population = select_next_generation(population, scores)

    hawks = population.count('H')
    stats['H'].append(hawks)
    stats['D'].append(POP_SIZE - hawks)  # проще, чем считать отдельно
    
end = time.time()

theory_hawks = POP_SIZE * V / C
theory_doves = POP_SIZE * (C - V) / C    

plt.figure(figsize=(10, 5))
plt.plot(stats['H'], label='Ястребы (H)', color='red', linewidth=2)
plt.plot(stats['D'], label='Голуби (D)', color='skyblue', linewidth=2)
plt.axhline(y=theory_hawks, color='gray', linestyle='--', label=f'Теория (ЭСС): {theory_hawks:.0f}')
plt.axhline(y=theory_doves, color='gray', linestyle='--', label=f'Теория (ЭСС): {theory_doves:.0f}')
plt.xlabel('Поколение', fontsize=12)
plt.ylabel('Количество особей', fontsize=12)
plt.title(' Эволюционная игра "Ястребы и Голуби"', fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
