from flask import Flask, make_response
import json


def create_app() -> Flask:
    """
    Фабрика приложения Flask.
    Возвращает и настраивает экземпляр Flask.
    """
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Добавляем фильтр для JSON
    @app.template_filter('from_json')
    def from_json_filter(value):
        try:
            return json.loads(value)
        except:
            return []

    # Импортируем роуты после создания приложения
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Добавляем заголовки для отключения кэширования
    @app.after_request
    def add_header(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    return app 