from flask import Blueprint, render_template, make_response
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Главная страница лендинга.
    """
    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@main_bp.route('/test')
def test():
    """
    Тестовая страница для проверки изображений.
    """
    return render_template('test.html')

@main_bp.route('/debug')
def debug():
    """
    Отладочная страница для проверки работы Flask.
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
    <html>
    <head><title>Debug Info</title></head>
    <body style="background: #000; color: #fff; padding: 20px; font-family: monospace;">
        <h1>Debug Information</h1>
        <p><strong>Current Time:</strong> {current_time}</p>
        <p><strong>Flask Debug:</strong> {main_bp.app.config.get('DEBUG', 'Not set')}</p>
        <p><strong>Templates Auto Reload:</strong> {main_bp.app.config.get('TEMPLATES_AUTO_RELOAD', 'Not set')}</p>
        <hr>
        <h2>Test Images:</h2>
        <img src="/static/img/character/character_1.png" alt="Test 1" style="width: 200px; height: 200px; object-fit: cover; border-radius: 10px; margin: 10px;">
        <img src="/static/img/character/character_2.png" alt="Test 2" style="width: 200px; height: 200px; object-fit: cover; border-radius: 10px; margin: 10px;">
        <img src="/static/img/character/character_3.png" alt="Test 3" style="width: 200px; height: 200px; object-fit: cover; border-radius: 10px; margin: 10px;">
    </body>
    </html>
    """ 