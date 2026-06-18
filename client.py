import socket

def start_client(host='127.0.0.1', port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print(f"[КЛІЄНТ] Успішно підключено до сервера {host}:{port}")
        print("Введіть арифметичний вираз (або 'exit' для виходу):")
        
        while True:
            expression = input("\nВаш вираз: ")
            
            if expression.strip().lower() == 'exit':
                print("[КЛІЄНТ] Завершення роботи.")
                break
                
            if not expression.strip():
                print("Рядок не може бути порожнім. Спробуйте ще раз.")
                continue

            client_socket.sendall(expression.encode('utf-8'))

            response = client_socket.recv(1024).decode('utf-8')
            print(f"[СЕРВЕР ВІДПОВІВ]: {response}")
            
    except ConnectionRefusedError:
        print("[ПОМИЛКА] Не вдалося підключитися до сервера. Перевірте, чи запущений server.py")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()