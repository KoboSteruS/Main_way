from app import create_app

app = create_app()

# Отключаем кэширование шаблонов
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000) 