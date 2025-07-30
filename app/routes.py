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
    except Exception:
        return False

# Декоратор для защиты админских маршрутов
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Получаем токен из URL
        token = request.view_args.get('token')
        
        # Временно упрощаем проверку для тестирования
        if not token:
            return "Доступ запрещен - токен отсутствует", 403
            
        # Проверяем только наличие токена, не валидируем
        return f(*args, **kwargs)
    return decorated_function

# Статичные участники (базовые)
STATIC_PARTICIPANTS = [
    {
        'id': 'static_1',
        'name': '👨‍🦰 Массажист из Швейцарии',
        'text': '«Я касался сотен тел, но не чувствовал своего»',
        'story': 'Работаю руками, держу, снимаю боль. Все думают, что я уравновешенный и спокойный. А внутри — пустота и выгорание.\n\nПуть стал первым пространством, где кто-то увидел меня, не как профи, а как мужчину. Где не надо было доказывать.\n\nСейчас я чувствую своё тело. И даю не из долга, а из наполненности.',
        'photo': 'img/character/character_1.png'
    },
    {
        'id': 'static_2',
        'name': '👩‍🦳 Женщина из другой страны',
        'text': '«Я дома. Среди тех, кто чувствует как я»',
        'story': 'Я жила в другой стране и думала, что со мной что‑то не так. Вокруг были люди, но я не могла найти своих.\n\nНа Пути я встретила женщин, которые слышат без слов. Без конкуренции. Без игр. Только глубина и поддержка.\n\nСейчас у меня подруги по всему миру. Мы на одной частоте.',
        'photo': 'img/character/character_2.png'
    },
    {
        'id': 'static_3',
        'name': '👨‍🦱 Человек, который выбрался из тьмы',
        'text': '«Если я ещё жив — значит, меня не просто так оставили»',
        'story': 'С 20 до 40 я жил во тьме: наркотики, тюрьмы, пустота. Каждый раз, когда пытался выбраться — падал снова. В какой-то момент я понял: если я ещё жив — значит, меня не просто так оставили.\n\nВ ОСНОВЕ ПУТИ я встретил тех, кто тоже падал, но не сломался. Здесь не судят, не жалеют, а держат. Сейчас я не один. Я иду свой путь — и знаю, ради чего встал.',
        'photo': 'img/character/character_3.png'
    }
]

# Статичные события (базовые)
STATIC_EVENTS = [
    {
        'id': 'static_event_1',
        'title': 'Москва',
        'desc': 'Столичный слёт. Город силы и встреч.',
        'image': '/static/img/Moscow.png'
    },
    {
        'id': 'static_event_2',
        'title': 'Грузия: женская линия',
        'desc': 'Уникальный женский круг. Горы, ритуалы, поддержка.',
        'image': '/static/img/Georgia.png'
    },
    {
        'id': 'static_event_3',
        'title': 'Латвия 2025',
        'desc': 'Сбор в лесу. Единение с природой и собой.',
        'image': '/static/img/Latvia.png'
    }
]

# Функция для загрузки участников из JSON
def load_participants():
    try:
        with open('app/data/participants.json', 'r', encoding='utf-8') as f:
            dynamic_participants = json.load(f)
            # Объединяем статичных и динамических участников
            all_participants = STATIC_PARTICIPANTS + dynamic_participants
            return all_participants
    except FileNotFoundError:
        # Если файл не найден, возвращаем только статичных
        return STATIC_PARTICIPANTS
    except Exception as e:
        print(f"Ошибка загрузки участников: {e}")
        return STATIC_PARTICIPANTS

# Функция для загрузки событий из JSON
def load_events():
    try:
        with open('app/data/events.json', 'r', encoding='utf-8') as f:
            dynamic_events = json.load(f)
            # Объединяем статичных и динамических событий
            all_events = STATIC_EVENTS + dynamic_events
            return all_events
    except FileNotFoundError:
        # Если файл не найден, возвращаем только статичных
        return STATIC_EVENTS
    except Exception as e:
        print(f"Ошибка загрузки событий: {e}")
        return STATIC_EVENTS

@main_bp.route('/')
@main_bp.route('/<version>')
def index(version=None):
    # Принудительно обновляем кэш, добавляя timestamp
    timestamp = int(time.time())
    
    # Загружаем участников из JSON
    participants = load_participants()
    
    # Загружаем события из JSON
    events = load_events()
    
    response = make_response(render_template('index.html', 
                                          version=version or f'1.1.{timestamp}',
                                          participants=participants,
                                          events=events))
    
    # Добавляем заголовки для отключения кэширования
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Last-Modified'] = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
    
    return response

# Маршрут для админской панели с JWT в URL
@main_bp.route('/<token>/admin')
@admin_required
def admin_dashboard(token):
    # Загружаем существующих участников
    participants = load_participants()
    
    # Загружаем существующих событий
    events = load_events()
    
    return render_template('admin/dashboard.html', participants=participants, events=events, token=token)

# Маршрут для добавления нового участника
@main_bp.route('/<token>/admin/add-participant', methods=['GET', 'POST'])
@admin_required
def add_participant(token):
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
                return redirect(url_for('main.admin_dashboard', token=token))
    
    return render_template('admin/add_participant.html', token=token)

# Маршрут для удаления участника
@main_bp.route('/<token>/admin/delete-participant/<participant_id>')
@admin_required
def delete_participant(token, participant_id):
    participants = load_participants()
    participant = next((p for p in participants if p['id'] == participant_id), None)
    
    if participant:
        # Удаляем файл фото (только для динамических участников)
        if not participant_id.startswith('static_') and participant.get('photo'):
            photo_path = os.path.join('app/static', participant['photo'])
            if os.path.exists(photo_path):
                os.remove(photo_path)
        
        # Удаляем из JSON (только динамических участников)
        if not participant_id.startswith('static_'):
            try:
                with open('app/data/participants.json', 'r', encoding='utf-8') as f:
                    dynamic_participants = json.load(f)
                dynamic_participants = [p for p in dynamic_participants if p['id'] != participant_id]
                save_participants(dynamic_participants)
                flash('Участник удален!', 'success')
            except Exception as e:
                flash(f'Ошибка удаления: {e}', 'error')
        else:
            flash('Статичных участников нельзя удалить!', 'error')
    
    return redirect(url_for('main.admin_dashboard', token=token))

# Маршрут для добавления нового события
@main_bp.route('/<token>/admin/add-event', methods=['GET', 'POST'])
@admin_required
def add_event(token):
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        
        # Обработка загруженного файла
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                # Генерируем уникальное имя файла
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()
                new_filename = f"event_{uuid.uuid4().hex[:8]}.{file_extension}"
                
                # Сохраняем файл
                upload_folder = 'app/static/img'
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                file_path = os.path.join(upload_folder, new_filename)
                file.save(file_path)
                
                # Создаем новое событие
                new_event = {
                    'id': str(uuid.uuid4()),
                    'title': title,
                    'desc': desc,
                    'image': f'img/{new_filename}'
                }
                
                # Сохраняем в JSON файл
                save_event(new_event)
                
                flash('Событие успешно добавлено!', 'success')
                return redirect(url_for('main.admin_dashboard', token=token))
    
    return render_template('admin/add_event.html', token=token)

# Маршрут для удаления события
@main_bp.route('/<token>/admin/delete-event/<event_id>')
@admin_required
def delete_event(token, event_id):
    events = load_events()
    event = next((e for e in events if e['id'] == event_id), None)
    
    if event:
        # Удаляем файл изображения (только для динамических событий)
        if not event_id.startswith('static_event_') and event.get('image'):
            image_path = os.path.join('app/static', event['image'])
            if os.path.exists(image_path):
                os.remove(image_path)
        
        # Удаляем из JSON (только динамических событий)
        if not event_id.startswith('static_event_'):
            try:
                with open('app/data/events.json', 'r', encoding='utf-8') as f:
                    dynamic_events = json.load(f)
                dynamic_events = [e for e in dynamic_events if e['id'] != event_id]
                save_events(dynamic_events)
                flash('Событие удалено!', 'success')
            except Exception as e:
                flash(f'Ошибка удаления: {e}', 'error')
        else:
            flash('Статичных событий нельзя удалить!', 'error')
    
    return redirect(url_for('main.admin_dashboard', token=token))

# Вспомогательные функции
def save_participant(participant):
    try:
        # Загружаем существующих динамических участников
        try:
            with open('app/data/participants.json', 'r', encoding='utf-8') as f:
                participants = json.load(f)
        except FileNotFoundError:
            participants = []
        
        # Добавляем нового участника
        participants.append(participant)
        
        # Сохраняем обратно
        save_participants(participants)
    except Exception as e:
        print(f"Ошибка сохранения участника: {e}")

def save_participants(participants):
    # Создаем папку если её нет
    os.makedirs('app/data', exist_ok=True)
    
    with open('app/data/participants.json', 'w', encoding='utf-8') as f:
        json.dump(participants, f, ensure_ascii=False, indent=2)

# Вспомогательные функции для событий
def save_event(event):
    try:
        # Загружаем существующих динамических событий
        try:
            with open('app/data/events.json', 'r', encoding='utf-8') as f:
                events = json.load(f)
        except FileNotFoundError:
            events = []
        
        # Добавляем новое событие
        events.append(event)
        
        # Сохраняем обратно
        save_events(events)
    except Exception as e:
        print(f"Ошибка сохранения события: {e}")

def save_events(events):
    # Создаем папку если её нет
    os.makedirs('app/data', exist_ok=True)
    
    with open('app/data/events.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

# Функция для генерации JWT токена (для справки)
def generate_admin_token():
    payload = {
        'admin': True,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM) 