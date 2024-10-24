from flask import Flask, render_template, request, redirect, url_for, flash
import json
import re
import os

app = Flask(__name__)
app.my_secret = os.environ['SECRET_KEY']  # Замените на случайную строку
app.secret_key = app.my_secret

# ID администратора (замените на реальный ID)
ADMIN_ID = 123456789

# Категории нейросетей
CATEGORIES = ["Генерация картинок", "Работа с текстом", "Работа с видео", "Программирование"]

# Функция для загрузки данных из JSON файла
def load_data():
    if os.path.exists('ai_library.json'):
        with open('ai_library.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

# Функция для сохранения данных в JSON файл
def save_data(data):
    with open('ai_library.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

# Функция для проверки правильности ссылки
def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        link = request.form['link']
        description = request.form['description']
        category = request.form['category']

        if not is_valid_url(link):
            flash('Некорректная ссылка. Пожалуйста, введите правильную ссылку.', 'error')
            return redirect(url_for('add'))

        new_ai = {
            'link': link,
            'description': description,
            'category': category
        }

        data = load_data()
        data.append(new_ai)
        save_data(data)

        flash('Нейросеть успешно добавлена в библиотеку!', 'success')
        return redirect(url_for('index'))

    return render_template('add.html', categories=CATEGORIES)

@app.route('/search')
def search():
    category = request.args.get('category')
    data = load_data()
    if category:
        filtered_data = [ai for ai in data if ai['category'] == category]
    else:
        filtered_data = data
    return render_template('search.html', ais=filtered_data, categories=CATEGORIES, selected_category=category)

@app.route('/delete/<path:link>')
def delete(link):
    # В реальном приложении здесь должна быть проверка на администратора
    data = load_data()
    new_data = [ai for ai in data if ai['link'] != link]
    if len(data) != len(new_data):
        save_data(new_data)
        flash('Нейросеть успешно удалена из библиотеки.', 'success')
    else:
        flash('Нейросеть с указанной ссылкой не найдена.', 'error')
    return redirect(url_for('search'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)