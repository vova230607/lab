import threading
import queue
import time
import random
import numpy as np

N = 1000       
M = 5          
T_OPEN = 120   
T1 = 0.5       
stadium_queue = queue.Queue()

arrival_times = []      
completion_times = []  
waiting_times = []      

stats_lock = threading.Lock()

def turnstile_worker(turnstile_id):
    """Модель роботи одного турнікета (потоку)"""
    while True:
        try:
            spectator = stadium_queue.get(timeout=0.5)
        except queue.Empty:
            break
        
        arrival_t = spectator['arrival_time']

        process_time = random.uniform(1/60, T1)

        with stats_lock:

            current_turnstile_time = max(arrival_t, completion_times[-1] if completion_times else -T_OPEN)
            finish_t = current_turnstile_time + process_time
            wait_t = finish_t - arrival_t
            
            completion_times.append(finish_t)
            waiting_times.append(wait_t)
            
        stadium_queue.task_done()

if __name__ == "__main__":
    print("=== Моделювання СМО: Стадіон ===")

    raw_arrivals = np.random.uniform(-T_OPEN, 0, N)
    raw_arrivals.sort() 

    for i, arr_time in enumerate(raw_arrivals):
        stadium_queue.put({'id': i, 'arrival_time': arr_time})
        arrival_times.append(arr_time)

    threads = []
    for m in range(M):
        t = threading.Thread(target=turnstile_worker, args=(m,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    waiting_times = np.array(waiting_times)

    required_advance_time = np.percentile(waiting_times, 90)

    late_spectators = sum(1 for t in completion_times if t > 0)

    print("\n--- Результати моделювання ---")
    print(f"Глядачів: {N}, Турнікетів: {M}")
    print(f"Максимальний час очікування в черзі: {max(waiting_times):.2f} хв.")
    print(f"Середній час очікування в черзі: {np.mean(waiting_times):.2f} хв.")
    print(f"Кількість глядачів, що запізнилися на початок матчу: {late_spectators} з {N}")
    print("-" * 30)
    print(f"ВИСНОВОК: Щоб з імовірністю 0.9 (90%) встигнути на матч,")
    print(f"глядачу потрібно прийти щонайменше за {required_advance_time:.2f} хвилин до початку матчу.")