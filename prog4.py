import math
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = 'super_secret_key_for_knu_labs'

#логіни й паролі
USERS = {
    "student": "knu2026",
    "admin": "admin777"
}

BASE_STYLE = """
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
    .container { background: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); width: 100%; max-width: 600px; box-sizing: border-box; }
    h1, h2 { color: #2c3e50; text-align: center; }
    .form-group { margin-bottom: 20px; }
    label { display: block; margin-bottom: 8px; font-weight: 600; color: #4a5568; }
    input[type="text"], input[type="password"], input[type="number"] { width: 100%; padding: 12px; border: 1px solid #cbd5e0; border-radius: 6px; box-sizing: border-box; font-size: 16px; }
    button { width: 100%; background-color: #3182ce; color: white; border: none; padding: 12px; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background 0.2s; }
    button:hover { background-color: #2b6cb0; }
    .task-card { background: #edf2f7; padding: 20px; border-radius: 8px; margin-bottom: 20px; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; border: 1px solid #e2e8f0; }
    .task-card:hover { transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .error { color: #e53e3e; background: #fff5f5; padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 15px; font-weight: 500; }
    .result-box { background: #f0fff4; border: 1px solid #c6f6d5; padding: 20px; border-radius: 8px; margin-top: 20px; }
    .explanation { font-style: italic; color: #4a5568; background: #f7fafc; padding: 15px; border-left: 4px solid #4a5568; margin-top: 15px; border-radius: 0 6px 6px 0; }
    .nav-links { display: flex; justify-content: space-between; margin-top: 25px; }
    .nav-links a { color: #3182ce; text-decoration: none; font-weight: 500; }
    .nav-links a:hover { text-decoration: underline; }
    .logout-btn { text-align: right; margin-bottom: 10px; }
    .logout-btn a { color: #e53e3e; text-decoration: none; font-size: 14px; }
</style>
"""

LOGIN_TEMPLATE = BASE_STYLE + """
<div class="container">
    <h1>Вхід до системи</h1>
    {% if error %}
        <div class="error">{{ error }}</div>
    {% endif %}
    <form method="POST">
        <div class="form-group">
            <label for="username">Логін:</label>
            <input type="text" id="username" name="username" required autocomplete="off">
        </div>
        <div class="form-group">
            <label for="password">Пароль:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <button type="submit">Увійти</button>
    </form>
</div>
"""

DASHBOARD_TEMPLATE = BASE_STYLE + """
<div class="container">
    <div class="logout-btn"><a href="{{ url_for('logout') }}">Вийти ({{ session['user'] }})</a></div>
    <h1>Вибір математичної задачі</h1>
    <p style="text-align: center; color: #718096;">Оберіть задачу для виконання обчислень:</p>
    
    <div class="task-card" onclick="location.href='{{ url_for('task_one') }}'">
        <h2>Задача №1: Геометрія трикутника</h2>
        <p>Обчислює гіпотенузу (для прямокутного трикутника), площу за формулою Герона, а також довжини медіан для заданих трьох сторін <i>a</i>, <i>b</i>, <i>c</i>.</p>
    </div>
    
    <div class="task-card" onclick="location.href='{{ url_for('task_two') }}'">
        <h2>Задача №2: Квадратне рівняння</h2>
        <p>Знаходить дійсні чи комплексні корені квадратного рівняння виду <i>ax² + bx + c = 0</i> з детальним покроковим розбором дискримінанту.</p>
    </div>
</div>
"""

TASK_ONE_TEMPLATE = BASE_STYLE + """
<div class="container">
    <h1>Геометрія трикутника</h1>
    <form method="POST">
        <div class="form-group">
            <label for="side_a">Сторона A:</label>
            <input type="number" step="any" id="side_a" name="side_a" value="{{ request.form.get('side_a', '') }}" required min="0.001">
        </div>
        <div class="form-group">
            <label for="side_b">Сторона B:</label>
            <input type="number" step="any" id="side_b" name="side_b" value="{{ request.form.get('side_b', '') }}" required min="0.001">
        </div>
        <div class="form-group">
            <label for="side_c">Сторона C:</label>
            <input type="number" step="any" id="side_c" name="side_c" value="{{ request.form.get('side_c', '') }}" required min="0.001">
        </div>
        <button type="submit">Обчислити</button>
    </form>

    {% if error %}
        <div class="error" style="margin-top: 20px;">{{ error }}</div>
    {% endif %}

    {% if result %}
        <div class="result-box">
            <h2>Результати обчислень:</h2>
            <ul>
                <li><b>Тип:</b> {{ result.triangle_type }}</li>
                <li><b>Площа (за Героном):</b> {{ result.area | round(4) }} кв. од.</li>
                <li><b>Медіана до стоони a (m_a):</b> {{ result.m_a | round(4) }}</li>
                <li><b>Медіана до сторони b (m_b):</b> {{ result.m_b | round(4) }}</li>
                <li><b>Медіана до сторони c (m_c):</b> {{ result.m_c | round(4) }}</li>
            </ul>
            <div class="explanation">
                <b>Пояснення:</b> Перевірка існування виконується за нерівністю трикутника ($a+b>c$). Медіани знайдені за класичною теоремою: $m_a = \\frac{1}{2}\\sqrt{2b^2 + 2c^2 - a^2}$.
            </div>
        </div>
    {% endif %}

    <div class="nav-links">
        <a href="{{ url_for('dashboard') }}">← До списку задач</a>
    </div>
</div>
"""

TASK_TWO_TEMPLATE = BASE_STYLE + """
<div class="container">
    <h1>Квадратне рівняння</h1>
    <form method="POST">
        <div class="form-group">
            <label for="coef_a">Коефіцієнт a (при x²):</label>
            <input type="number" step="any" id="coef_a" name="coef_a" value="{{ request.form.get('coef_a', '') }}" required>
        </div>
        <div class="form-group">
            <label for="coef_b">Коефіцієнт b (при x):</label>
            <input type="number" step="any" id="coef_b" name="coef_b" value="{{ request.form.get('coef_b', '') }}" required>
        </div>
        <div class="form-group">
            <label for="coef_c">Вільний член c:</label>
            <input type="number" step="any" id="coef_c" name="coef_c" value="{{ request.form.get('coef_c', '') }}" required>
        </div>
        <button type="submit">Розв'язати</button>
    </form>

    {% if error %}
        <div class="error" style="margin-top: 20px;">{{ error }}</div>
    {% endif %}

    {% if result %}
        <div class="result-box">
            <h2>Результат:</h2>
            <p><b>Дискримінант (D):</b> {{ result.D | round(4) }}</p>
            <p><b>Корені рівняння:</b></p>
            <ul>
                {% if result.roots_type == 'two_real' %}
                    <li>x₁ = {{ result.x1 | round(4) }}</li>
                    <li>x₂ = {{ result.x2 | round(4) }}</li>
                {% elif result.roots_type == 'one_real' %}
                    <li>x = {{ result.x1 | round(4) }} (кратність 2)</li>
                {% else %}
                    <li>x₁ = {{ result.x1 }}</li>
                    <li>x₂ = {{ result.x2 }}</li>
                {% endif %}
            </ul>
            <div class="explanation">
                <b>Покроковий аналіз:</b> {{ result.explanation }}
            </div>
        </div>
    {% endif %}

    <div class="nav-links">
        <a href="{{ url_for('dashboard') }}">← До списку задач</a>
    </div>
</div>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    """1. Початкова сторінка — автентифікація користувача."""
    if 'user' in session:
        return redirect(url_for('dashboard'))
        
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            error = "Невірний логін або пароль! Спробуйте ще раз."
            
    return render_template_string(LOGIN_TEMPLATE, error=error)


@app.route('/dashboard')
def dashboard():
    """2. Сторінка вибору задачі з коротким описом."""
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template_string(DASHBOARD_TEMPLATE)


@app.route('/task1', methods=['GET', 'POST'])
def task_one():
    """3 та 4. Задача №1: Форма введення та вивід результатів."""
    if 'user' not in session:
        return redirect(url_for('login'))
        
    result = None
    error = None
    
    if request.method == 'POST':
        try:
            a = float(request.form.get('side_a'))
            b = float(request.form.get('side_b'))
            c = float(request.form.get('side_c'))
            
            # Валідація існування трикутника
            if a + b > c and a + c > b and b + c > a:
                # Напівпериметр
                p = (a + b + c) / 2
                # Формула Герона
                area = math.sqrt(p * (p - a) * (p - b) * (p - c))
                
                # Довжини медіан
                m_a = 0.5 * math.sqrt(2*(b**2) + 2*(c**2) - a**2)
                m_b = 0.5 * math.sqrt(2*(a**2) + 2*(c**2) - b**2)
                m_c = 0.5 * math.sqrt(2*(a**2) + 2*(b**2) - c**2)
                
                # Визначення типу трикутника за теоремою косинусів
                sides = sorted([a, b, c])
                if math.isclose(sides[0]**2 + sides[1]**2, sides[2]**2):
                    t_type = "Прямокутний трикутник"
                elif sides[0]**2 + sides[1]**2 > sides[2]**2:
                    t_type = "Гострокутний трикутник"
                else:
                    t_type = "Тупокутний трикутник"
                    
                result = {
                    "triangle_type": t_type,
                    "area": area,
                    "m_a": m_a,
                    "m_b": m_b,
                    "m_c": m_c
                }
            else:
                error = "Трикутник із такими сторонами не існує (не виконується нерівність трикутника)."
        except ValueError:
            error = "Будь ласка, введіть коректні числові значення."
            
    return render_template_string(TASK_ONE_TEMPLATE, result=result, error=error)


@app.route('/task2', methods=['GET', 'POST'])
def task_two():
    """3 та 4. Задача №2: Квадратне рівняння."""
    if 'user' not in session:
        return redirect(url_for('login'))
        
    result = None
    error = None
    
    if request.method == 'POST':
        try:
            a = float(request.form.get('coef_a'))
            b = float(request.form.get('coef_b'))
            c = float(request.form.get('coef_c'))
            
            if math.isclose(a, 0.0):
                if math.isclose(b, 0.0):
                    error = "При a=0 та b=0 рівняння вироджується. Коренів немає або безліч."
                else:
                    # Лінійне рівняння bx + c = 0
                    x = -c / b
                    result = {
                        "D": 0.0,
                        "roots_type": "one_real",
                        "x1": x,
                        "explanation": f"Оскільки коефіцієнт a = 0, рівняння перетворилося на лінійне: {b}x + {c} = 0."
                    }
            else:
                # Розрахунок дискримінанту
                D = b**2 - 4*a*c
                
                if D > 0:
                    x1 = (-b + math.sqrt(D)) / (2*a)
                    x2 = (-b - math.sqrt(D)) / (2*a)
                    result = {
                        "D": D,
                        "roots_type": "two_real",
                        "x1": x1,
                        "x2": x2,
                        "explanation": "Дискримінант додатний (D > 0). Рівняння має два дійсні різні корені."
                    }
                elif math.isclose(D, 0.0):
                    x = -b / (2*a)
                    result = {
                        "D": 0.0,
                        "roots_type": "one_real",
                        "x1": x,
                        "explanation": "Дискримінант дорівнює нулю (D = 0). Рівняння має один дійсний корінь кратності 2."
                    }
                else:
                    # Комплексні корені
                    real_part = -b / (2*a)
                    imag_part = math.sqrt(-D) / (2*a)
                    result = {
                        "D": D,
                        "roots_type": "complex",
                        "x1": f"{round(real_part, 4)} + {round(imag_part, 4)}i",
                        "x2": f"{round(real_part, 4)} - {round(imag_part, 4)}i",
                        "explanation": "Дискримінант від'ємний (D < 0). Рівняння має два комплексно-спряжені корені."
                    }
        except ValueError:
            error = "Помилка введення даних. Перевірте значення коефіцієнтів."
            
    return render_template_string(TASK_TWO_TEMPLATE, result=result, error=error)


@app.route('/logout')
def logout():
    """Вихід із системи."""
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)