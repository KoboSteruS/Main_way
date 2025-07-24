from flask import Blueprint, render_template, make_response
import time

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/<version>')
def index(version=None):
    # Принудительно обновляем кэш, добавляя timestamp
    timestamp = int(time.time())
    response = make_response(render_template('index.html', version=version or f'1.0.{timestamp}'))
    
    # Добавляем заголовки для отключения кэширования
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Last-Modified'] = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
    
    return response

@main_bp.route('/test')
def test():
    return render_template('test.html')

@main_bp.route('/debug')
def debug():
    return "Debug route working" 