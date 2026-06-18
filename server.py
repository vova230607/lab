import socket
import ast

def check_syntax(expression):
    """
    Перевіряє синтаксичну правильність арифметичного виразу за допомогою ast.
    """
    try:
        expr_clean = expression.strip()
        if not expr_clean:
            return "Помилка: Порожній рядок."

        parsed = ast.parse(expr_clean, mode='eval')

        for node in ast.walk(parsed):
            if isinstance(node, (ast.Call, ast.Attribute, ast.Import, ast.ImportFrom)):
                return "Помилка: Вираз містить недозволені елементи (можна лише числа та знаки операцій)."
                
        return "Успіх: Вираз синтаксично правильний."
        
    except SyntaxError:
        return "Помилка: Некоректний синтаксис арифметичного виразу."
    except Exception as e:
        return f"Помилка аналізу: {str(e)}"

def start_server(host='127.0.0.1', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[СЕРВЕР] Запущено на {host}:{port}. Очікування підключення клієнта...")

    while True:
        conn, addr = server_socket.accept()
        print(f"[СЕРВЕР] Підключено клієнта з адреси: {addr}")
        
        try:
            while True:

                data = conn.recv(1024)
                if not data:
                    break 
                
                expression = data.decode('utf-8')
                print(f"[СЕРВЕР] Отримано вираз для перевірки: '{expression}'")

                response = check_syntax(expression)

                conn.sendall(response.encode('utf-8'))
        except ConnectionResetError:
            print("[СЕРВЕР] З'єднання було примусово розірвано клієнтом.")
        finally:
            conn.close()
            print("[СЕРВЕР] З'єднання з клієнтом закрито. Очікування нового підключення...\n")

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n[СЕРВЕР] Зупинено користувачем.")