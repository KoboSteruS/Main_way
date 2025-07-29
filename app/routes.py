from flask import Blueprint, render_template, make_response, request, redirect, url_for, flash, session
import time
import os
import uuid
from werkzeug.utils import secure_filename
import json
from functools import wraps
import jwt
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

# JWT настройки
JWT_SECRET = "your-super-secret-jwt-key-change-in-production"
JWT_ALGORITHM = "HS256"
ADMIN_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6dHJ1ZSwiaWF0IjoxNzM0NzI4MDAwLCJleHAiOjE3MzQ4MTQ0MDB9.ADMIN_TOKEN_HERE"

# Функция для проверки JWT токена
def verify_jwt_token(token):
    try:
        # Декодируем токен
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get('admin', False)
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

# Декоратор для защиты админских маршрутов
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Получаем токен из URL параметра
        token = request.args.get('token')
        if not token or not verify_jwt_token(token):
            return redirect(url_for('main.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
@main_bp.route('/<version>')
def index(version=None):
    # Принудительно обновляем кэш, добавляя timestamp
    timestamp = int(time.time())
    response = make_response(render_template('index.html', version=version or f'1.1.{timestamp}'))
    
    # Добавляем заголовки для отключения кэширования
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Last-Modified'] = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
    
    return response

# Маршрут для входа в админку
@main_bp.route('/jwt-ключи/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        token = request.form.get('token')
        
        if token and verify_jwt_token(token):
            return redirect(url_for('main.admin_dashboard', token=token))
        else:
            flash('Неверный JWT токен', 'error')
    
    return render_template('admin/login.html')

# Маршрут для админской панели
@main_bp.route('/jwt-ключи/admin')
@admin_required
def admin_dashboard():
    # Загружаем существующих участников
    participants = load_participants()
    return render_template('admin/dashboard.html', participants=participants)

# Маршрут для добавления нового участника
@main_bp.route('/jwt-ключи/admin/add-participant', methods=['GET', 'POST'])
@admin_required
def add_participant():
    if request.method == 'POST':
        name = request.form.get('name')
        text = request.form.get('text')
        story = request.form.get('story')
        
        # Обработка загруженного файла
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename:
                # Генерируем уникальное имя файла
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()
                new_filename = f"character_{uuid.uuid4().hex[:8]}.{file_extension}"
                
                # Сохраняем файл
                upload_folder = 'app/static/img/character'
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                file_path = os.path.join(upload_folder, new_filename)
                file.save(file_path)
                
                # Создаем нового участника
                new_participant = {
                    'id': str(uuid.uuid4()),
                    'name': name,
                    'text': text,
                    'story': story,
                    'photo': f'img/character/{new_filename}'
                }
                
                # Сохраняем в JSON файл
                save_participant(new_participant)
                
                flash('Участник успешно добавлен!', 'success')
                return redirect(url_for('main.admin_dashboard', token=request.args.get('token')))
    
    return render_template('admin/add_participant.html')

# Маршрут для удаления участника
@main_bp.route('/jwt-ключи/admin/delete-participant/<participant_id>')
@admin_required
def delete_participant(participant_id):
    participants = load_participants()
    participant = next((p for p in participants if p['id'] == participant_id), None)
    
    if participant:
        # Удаляем файл фото
        if participant.get('photo'):
            photo_path = os.path.join('app/static', participant['photo'])
            if os.path.exists(photo_path):
                os.remove(photo_path)
        
        # Удаляем из JSON
        participants = [p for p in participants if p['id'] != participant_id]
        save_participants(participants)
        flash('Участник удален!', 'success')
    
    return redirect(url_for('main.admin_dashboard', token=request.args.get('token')))

# Маршрут для выхода из админки
@main_bp.route('/jwt-ключи/admin/logout')
def admin_logout():
    return redirect(url_for('main.admin_login'))

# Вспомогательные функции
def load_participants():
    try:
        with open('app/data/participants.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_participant(participant):
    participants = load_participants()
    participants.append(participant)
    save_participants(participants)

def save_participants(participants):
    # Создаем папку если её нет
    os.makedirs('app/data', exist_ok=True)
    
    with open('app/data/participants.json', 'w', encoding='utf-8') as f:
        json.dump(participants, f, ensure_ascii=False, indent=2)

# Функция для генерации JWT токена (для справки)
def generate_admin_token():
    payload = {
        'admin': True,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM) 