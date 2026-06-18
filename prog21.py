import threading
import queue
import time
import random

# Можна змінювати ці параметри для симуляції різних умов
T1 = 3  # Максимальний час генерації повідомлення
T2 = 2  # Максимальний час обробки повідомлення

message_queue = queue.Queue()

def producer(t1):
    """
    Потік-виробник: генерує повідомлення через випадкові інтервали 
    та додає їх у чергу.
    """
    message_id = 1
    while True:
        sleep_time = random.uniform(1, t1)
        time.sleep(sleep_time)
        
        message = f"Повідомлення #{message_id}"

        message_queue.put(message)
        print(f"[Генератор] Створено та додано в чергу: {message} (пауза {sleep_time:.2f}с)")
        
        message_id += 1

def consumer(t2):
    """
    Потік-споживач: виймає повідомлення з черги та обробляє їх
    (виводить на екран) з випадковою затримкою обробки.
    """
    while True:
        message = message_queue.get()

        process_time = random.uniform(1, t2)
        time.sleep(process_time)

        print(f"    [Обробник] ОБРОБЛЕНО: {message} (час обробки {process_time:.2f}с)")

        message_queue.task_done()

if __name__ == "__main__":
    print("=== Старт симуляції черги повідомлень (Ctrl+C для виходу) ===")
    print(f"Параметри: Макс. час генерації T1 = {T1}с, Макс. час обробки T2 = {T2}с.\n")

    producer_thread = threading.Thread(target=producer, args=(T1,), daemon=True)
    consumer_thread = threading.Thread(target=consumer, args=(T2,), daemon=True)

    producer_thread.start()
    consumer_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n=== Симуляцію зупинено користувачем ===")