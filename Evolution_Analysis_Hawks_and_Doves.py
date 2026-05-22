import random
import matplotlib.pyplot as plt
import time

start = time.time()

HAWK_RATIO = 0.5   
POP_SIZE = 1000       
GENERATIONS = 100    
MATCHES = 300        

ENVIRONMENT_SCHEDULE = [
    (15, 20),  
    (5, 20),   
    (18, 20),  
    (10, 10),  
    (15, 20),  
]

num_hawks = int(POP_SIZE * HAWK_RATIO)      
num_doves = POP_SIZE - num_hawks            

population = ['H'] * num_hawks + ['D'] * num_doves
random.shuffle(population)  

stats = {'H': [], 'D': []}          
theory_history_H = []                
theory_history_D = []                

def play_match(p1, p2):
    if p1 == 'H' and p2 == 'H':
        return (V, -C) if random.random() < 0.5 else (-C, V)
    elif p1 == 'H':
        return V, 0              # Ястреб забирает ресурс у Голубя
    elif p2 == 'H':
        return 0, V              # Голубь отступает, Ястреб побеждает
    else:
        return V/2, V/2          # Два Голубя делят ресурс поровну

def calculate_fitness(pop):
    scores = [0] * len(pop)
    for i, player in enumerate(pop):
        for _ in range(MATCHES):
            opponent = random.choice(pop)
            score, _ = play_match(player, opponent)
            scores[i] += score
    return scores

def select_next_generation(pop, scores):
    min_score = min(scores)
    fitness = [s - min_score + 1 for s in scores]
    return random.choices(pop, weights=fitness, k=POP_SIZE)

for gen in range(GENERATIONS):
    phase_index = gen // 20
    if phase_index >= len(ENVIRONMENT_SCHEDULE):
        phase_index = len(ENVIRONMENT_SCHEDULE) - 1  # Защита от выхода за границы
    V, C = ENVIRONMENT_SCHEDULE[phase_index]

    current_theory_hawks = POP_SIZE * V / C
    current_theory_doves = POP_SIZE - current_theory_hawks

    theory_history_H.append(current_theory_hawks)
    theory_history_D.append(current_theory_doves)

    scores = calculate_fitness(population)
    population = select_next_generation(population, scores)
    hawks = population.count('H')

    stats['H'].append(hawks)
    stats['D'].append(POP_SIZE - hawks)
    if gen % 20 == 0:
        print(f"Поколение {gen:3d}: V={V:2d}, C={C:2d} | Ястребы: {hawks:4d} ({hawks/POP_SIZE*100:5.1f}%)")

end = time.time()

# Теория для последних условий
final_V, final_C = ENVIRONMENT_SCHEDULE[-1]
final_theory_h = POP_SIZE * final_V / final_C
final_theory_d = POP_SIZE - final_theory_h

print(f"\nВремямя выполнения:{end - start:.2f} секунд")
print(f"Запуск симуляции: {num_hawks} Ястребов ({HAWK_RATIO*100:.0f}%), {num_doves} Голубей")
print(f"Параметры: POP_SIZE={POP_SIZE}, GENERATIONS={GENERATIONS}, MATCHES={MATCHES}\n")
plt.figure(figsize=(12, 6))

plt.plot(stats['H'], label='Ястребы (факт)', color='red', linewidth=2)
plt.plot(stats['D'], label='Голуби (факт)', color='skyblue', linewidth=2)

# Теоретическое равновесие (динамическая линия!)
plt.plot(theory_history_H, label='Теория Ястребов', color='red', linestyle=':', linewidth=1.5, alpha=0.7)
plt.plot(theory_history_D, label='Теория Голубей', color='skyblue', linestyle=':', linewidth=1.5, alpha=0.7)

# Вертикальные линии — моменты смены среды
for change_point in range(20, GENERATIONS, 20):
    plt.axvline(x=change_point, color='gray', linestyle=':', alpha=0.2)

plt.xlabel('Поколение', fontsize=12)
plt.ylabel('Количество особей', fontsize=12)
plt.title(f'Эволюция стратегий (старт:{HAWK_RATIO*100:.0f}% Ястребов)', fontsize=14, pad=20)
plt.legend(loc='best', fontsize=10)
plt.grid(alpha=0.3, linestyle='-')
plt.tight_layout()
plt.show()