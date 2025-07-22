from flask import Flask


def create_app() -> Flask:
    """
    Фабрика приложения Flask.
    Возвращает и настраивает экземпляр Flask.
    """
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app 