#!/usr/bin/env python3
"""
Скрипт для принудительного обновления всех файлов
"""
import os
import time

def touch_file(filepath):
    """Обновляет время модификации файла"""
    try:
        with open(filepath, 'a'):
            os.utime(filepath, None)
        print(f"✓ Обновлен: {filepath}")
    except Exception as e:
        print(f"✗ Ошибка: {filepath} - {e}")

def main():
    """Основная функция"""
    print("🔄 Принудительное обновление файлов...")
    
    # Список файлов для обновления
    files_to_touch = [
        'app/templates/index.html',
        'app/templates/components/who_we_are.html',
        'app/templates/components/values.html',
        'app/static/css/main.css',
        'app/static/js/main.js',
        'app/templates/base.html'
    ]
    
    # Обновляем каждый файл
    for filepath in files_to_touch:
        if os.path.exists(filepath):
            touch_file(filepath)
        else:
            print(f"⚠ Файл не найден: {filepath}")
    
    print(f"\n✅ Обновление завершено в {time.strftime('%H:%M:%S')}")
    print("🔄 Перезапустите Flask приложение")

if __name__ == '__main__':
    main() 