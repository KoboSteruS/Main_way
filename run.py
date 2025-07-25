from app import create_app

app = create_app()

if __name__ == '__main__':
    # Используем stat reloader вместо watchdog для совместимости с Python 3.13
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=True, reloader_type='stat') 