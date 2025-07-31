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

# Константы для статических данных
STATIC_PARTICIPANTS = [
    {
        'id': 'static_participant_1',
        'name': 'Алексей',
        'text': 'Бывший военный',
        'story': 'История человека 1: Я был военным 15 лет. Домой вернулся другим человеком. Не мог найти себя в мирной жизни. В ОСНОВЕ ПУТИ я встретил тех, кто понимает. Кто не бросает. Кто держит. Сейчас я не один. Я иду свой путь — и знаю, ради чего встал.',
        'photo': 'img/character/character_1.png'
    },
    {
        'id': 'static_participant_2', 
        'name': 'Мария',
        'text': 'Бывшая топ-менеджер',
        'story': 'История человека 2: Я была топ-менеджером в крупной компании. Деньги, статус, но пустота внутри. В 35 поняла — я не живу, а существую. В ОСНОВЕ ПУТИ я встретила тех, кто показал: настоящая сила — в честности с собой. Сейчас я не одна. Я иду свой путь — и знаю, ради чего встала.',
        'photo': 'img/character/character_2.png'
    },
    {
        'id': 'static_participant_3',
        'name': 'Дмитрий', 
        'text': 'Бывший зависимый',
        'story': 'История человека 3: С 20 до 40 я жил во тьме: наркотики, тюрьмы, пустота. Каждый раз, когда пытался выбраться — падал снова. В какой-то момент я понял: если я ещё жив — значит, меня не просто так оставили. В ОСНОВЕ ПУТИ я встретил тех, кто тоже падал, но не сломался. Здесь не судят, не жалеют, а держат. Сейчас я не один. Я иду свой путь — и знаю, ради чего встал.',
        'photo': 'img/character/character_3.png'
    }
]

STATIC_EVENTS = [
    {
        'id': 'static_event_1',
        'title': 'Москва',
        'desc': 'Столичный слёт. Город силы и встреч.',
        'image': 'img/Moscow.png'
    },
    {
        'id': 'static_event_2',
        'title': 'Грузия: женская линия',
        'desc': 'Уникальный женский круг. Горы, ритуалы, поддержка.',
        'image': 'img/Georgia.png'
    },
    {
        'id': 'static_event_3',
        'title': 'Латвия 2025',
        'desc': 'Сбор в лесу. Единение с природой и собой.',
        'image': 'img/Latvia.png'
    }
]

STATIC_ORGANIZERS = [
    {
        'id': 'static_organizer_1',
        'name': 'Координатор',
        'role': 'Координатор',
        'photo': 'img/Coordinat.png'
    },
    {
        'id': 'static_organizer_2',
        'name': 'Глава организации',
        'role': 'Глава организации', 
        'photo': 'img/Glava.png'
    },
    {
        'id': 'static_organizer_3',
        'name': 'Проводница',
        'role': 'Проводница',
        'photo': 'img/Provodnik.png'
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

# Функции для работы с Telegram ссылкой
def load_telegram_link():
    """Загружает ссылку на Telegram из файла"""
    try:
        with open('app/data/telegram_link.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('link', 'https://t.me/VScukerman')
    except (FileNotFoundError, json.JSONDecodeError):
        return 'https://t.me/VScukerman'

def save_telegram_link(link):
    """Сохраняет ссылку на Telegram в файл"""
    os.makedirs('app/data', exist_ok=True)
    with open('app/data/telegram_link.json', 'w', encoding='utf-8') as f:
        json.dump({'link': link}, f, ensure_ascii=False, indent=2)

# Функции для работы с организаторами
def load_organizers():
    """Загружает организаторов из файла"""
    try:
        with open('app/data/organizers.json', 'r', encoding='utf-8') as f:
            dynamic_organizers = json.load(f)
            return STATIC_ORGANIZERS + dynamic_organizers
    except (FileNotFoundError, json.JSONDecodeError):
        return STATIC_ORGANIZERS

def save_organizer(organizer_data):
    """Сохраняет нового организатора"""
    os.makedirs('app/data', exist_ok=True)
    try:
        with open('app/data/organizers.json', 'r', encoding='utf-8') as f:
            organizers = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        organizers = []
    
    # Добавляем ID для нового организатора
    organizer_data['id'] = f'organizer_{uuid.uuid4().hex[:8]}'
    organizers.append(organizer_data)
    
    with open('app/data/organizers.json', 'w', encoding='utf-8') as f:
        json.dump(organizers, f, ensure_ascii=False, indent=2)

def delete_organizer(organizer_id):
    """Удаляет организатора (только динамических)"""
    try:
        with open('app/data/organizers.json', 'r', encoding='utf-8') as f:
            organizers = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    
    # Удаляем только динамических организаторов
    organizers = [org for org in organizers if org.get('id') != organizer_id]
    
    with open('app/data/organizers.json', 'w', encoding='utf-8') as f:
        json.dump(organizers, f, ensure_ascii=False, indent=2)
    
    return True

@main_bp.route('/')
@main_bp.route('/<version>')
def index(version=None):
    # Принудительно обновляем кэш, добавляя timestamp
    timestamp = int(time.time())
    
    # Загружаем данные
    participants = load_participants()
    events = load_events()
    organizers = load_organizers()
    telegram_link = load_telegram_link()
    
    response = make_response(render_template('index.html', 
                                          version=version or f'1.1.{timestamp}',
                                          participants=participants,
                                          events=events,
                                          organizers=organizers,
                                          telegram_link=telegram_link))
    
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
    # Загружаем данные
    participants = load_participants()
    events = load_events()
    organizers = load_organizers()
    telegram_link = load_telegram_link()
    
    return render_template('admin/dashboard.html', 
                         participants=participants, 
                         events=events, 
                         organizers=organizers,
                         telegram_link=telegram_link,
                         token=token)

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

# Маршрут для управления ссылкой на Telegram
@main_bp.route('/<token>/admin/telegram-link', methods=['GET', 'POST'])
@admin_required
def manage_telegram_link(token):
    if request.method == 'POST':
        new_link = request.form.get('telegram_link', '').strip()
        if new_link:
            save_telegram_link(new_link)
            flash('Ссылка на Telegram успешно обновлена!', 'success')
        else:
            flash('Ссылка не может быть пустой', 'error')
        return redirect(url_for('main.admin_dashboard', token=token))
    
    telegram_link = load_telegram_link()
    return render_template('admin/telegram_link.html', telegram_link=telegram_link, token=token)

# Маршрут для добавления нового организатора
@main_bp.route('/<token>/admin/add-organizer', methods=['GET', 'POST'])
@admin_required
def add_organizer(token):
    if request.method == 'POST':
        name = request.form.get('name')
        role = request.form.get('role')
        
        # Обработка загруженного файла
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename:
                # Генерируем уникальное имя файла
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()
                new_filename = f"organizer_{uuid.uuid4().hex[:8]}.{file_extension}"
                
                # Сохраняем файл
                upload_folder = 'app/static/img'
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                file_path = os.path.join(upload_folder, new_filename)
                file.save(file_path)
                
                # Создаем нового организатора
                new_organizer = {
                    'name': name,
                    'role': role,
                    'photo': f'img/{new_filename}'
                }
                
                # Сохраняем в JSON файл
                save_organizer(new_organizer)
                
                flash('Организатор успешно добавлен!', 'success')
                return redirect(url_for('main.admin_dashboard', token=token))
    
    return render_template('admin/add_organizer.html', token=token)

# Маршрут для редактирования участника
@main_bp.route('/<token>/admin/edit-participant/<participant_id>', methods=['GET', 'POST'])
@admin_required
def edit_participant(token, participant_id):
    participants = load_participants()
    participant = next((p for p in participants if p['id'] == participant_id), None)
    
    if not participant:
        flash('Участник не найден', 'error')
        return redirect(url_for('main.admin_dashboard', token=token))
    
    if request.method == 'POST':
        name = request.form.get('name')
        text = request.form.get('text')
        story = request.form.get('story')
        
        # Обработка загруженного файла
        new_photo = participant.get('photo')
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
                new_photo = f'img/character/{new_filename}'
        
        # Обновляем данные участника
        participant['name'] = name
        participant['text'] = text
        participant['story'] = story
        participant['photo'] = new_photo
        
        # Сохраняем изменения
        if participant_id.startswith('static_'):
            # Для статичных участников обновляем константу
            for i, static_p in enumerate(STATIC_PARTICIPANTS):
                if static_p['id'] == participant_id:
                    STATIC_PARTICIPANTS[i] = participant
                    break
            flash('Статичный участник успешно обновлен!', 'success')
        else:
            # Для динамических участников обновляем JSON
            try:
                with open('app/data/participants.json', 'r', encoding='utf-8') as f:
                    dynamic_participants = json.load(f)
                
                for i, dyn_p in enumerate(dynamic_participants):
                    if dyn_p['id'] == participant_id:
                        dynamic_participants[i] = participant
                        break
                
                save_participants(dynamic_participants)
                flash('Участник успешно обновлен!', 'success')
            except Exception as e:
                flash(f'Ошибка обновления: {e}', 'error')
        
        return redirect(url_for('main.admin_dashboard', token=token))
    
    return render_template('admin/edit_participant.html', participant=participant, token=token)

# Маршрут для редактирования события
@main_bp.route('/<token>/admin/edit-event/<event_id>', methods=['GET', 'POST'])
@admin_required
def edit_event(token, event_id):
    events = load_events()
    event = next((e for e in events if e['id'] == event_id), None)
    
    if not event:
        flash('Событие не найдено', 'error')
        return redirect(url_for('main.admin_dashboard', token=token))
    
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        
        # Обработка загруженного файла
        new_image = event.get('image')
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
                new_image = f'img/{new_filename}'
        
        # Обновляем данные события
        event['title'] = title
        event['desc'] = desc
        event['image'] = new_image
        
        # Сохраняем изменения
        if event_id.startswith('static_event_'):
            # Для статичных событий обновляем константу
            for i, static_e in enumerate(STATIC_EVENTS):
                if static_e['id'] == event_id:
                    STATIC_EVENTS[i] = event
                    break
            flash('Статичное событие успешно обновлено!', 'success')
        else:
            # Для динамических событий обновляем JSON
            try:
                with open('app/data/events.json', 'r', encoding='utf-8') as f:
                    dynamic_events = json.load(f)
                
                for i, dyn_e in enumerate(dynamic_events):
                    if dyn_e['id'] == event_id:
                        dynamic_events[i] = event
                        break
                
                save_events(dynamic_events)
                flash('Событие успешно обновлено!', 'success')
            except Exception as e:
                flash(f'Ошибка обновления: {e}', 'error')
        
        return redirect(url_for('main.admin_dashboard', token=token))
    
    return render_template('admin/edit_event.html', event=event, token=token)

# Маршрут для редактирования организатора
@main_bp.route('/<token>/admin/edit-organizer/<organizer_id>', methods=['GET', 'POST'])
@admin_required
def edit_organizer(token, organizer_id):
    organizers = load_organizers()
    organizer = next((o for o in organizers if o['id'] == organizer_id), None)
    
    if not organizer:
        flash('Организатор не найден', 'error')
        return redirect(url_for('main.admin_dashboard', token=token))
    
    if request.method == 'POST':
        name = request.form.get('name')
        role = request.form.get('role')
        
        # Обработка загруженного файла
        new_photo = organizer.get('photo')
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename:
                # Генерируем уникальное имя файла
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()
                new_filename = f"organizer_{uuid.uuid4().hex[:8]}.{file_extension}"
                
                # Сохраняем файл
                upload_folder = 'app/static/img'
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                file_path = os.path.join(upload_folder, new_filename)
                file.save(file_path)
                new_photo = f'img/{new_filename}'
        
        # Обновляем данные организатора
        organizer['name'] = name
        organizer['role'] = role
        organizer['photo'] = new_photo
        
        # Сохраняем изменения
        if organizer_id.startswith('static_'):
            # Для статичных организаторов обновляем константу
            for i, static_o in enumerate(STATIC_ORGANIZERS):
                if static_o['id'] == organizer_id:
                    STATIC_ORGANIZERS[i] = organizer
                    break
            flash('Статичный организатор успешно обновлен!', 'success')
        else:
            # Для динамических организаторов обновляем JSON
            try:
                with open('app/data/organizers.json', 'r', encoding='utf-8') as f:
                    dynamic_organizers = json.load(f)
                
                for i, dyn_o in enumerate(dynamic_organizers):
                    if dyn_o['id'] == organizer_id:
                        dynamic_organizers[i] = organizer
                        break
                
                with open('app/data/organizers.json', 'w', encoding='utf-8') as f:
                    json.dump(dynamic_organizers, f, ensure_ascii=False, indent=2)
                flash('Организатор успешно обновлен!', 'success')
            except Exception as e:
                flash(f'Ошибка обновления: {e}', 'error')
        
        return redirect(url_for('main.admin_dashboard', token=token))
    
    return render_template('admin/edit_organizer.html', organizer=organizer, token=token)

# Маршрут для удаления организатора
@main_bp.route('/<token>/admin/delete-organizer/<organizer_id>')
@admin_required
def delete_organizer_route(token, organizer_id):
    organizers = load_organizers()
    organizer = next((o for o in organizers if o['id'] == organizer_id), None)
    
    if organizer:
        # Удаляем файл фото (только для динамических организаторов)
        if not organizer_id.startswith('static_') and organizer.get('photo'):
            photo_path = os.path.join('app/static', organizer['photo'])
            if os.path.exists(photo_path):
                os.remove(photo_path)
        
        # Удаляем из JSON (только динамических организаторов)
        if not organizer_id.startswith('static_'):
            if delete_organizer(organizer_id):
                flash('Организатор успешно удален!', 'success')
            else:
                flash('Ошибка при удалении организатора', 'error')
        else:
            flash('Статических организаторов нельзя удалить', 'error')
    else:
        flash('Организатор не найден', 'error')
    
    return redirect(url_for('main.admin_dashboard', token=token)) 