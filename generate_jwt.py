#!/usr/bin/env python3
"""
Скрипт для генерации JWT токена для админки
"""

import jwt
from datetime import datetime, timedelta

# Настройки JWT (должны совпадать с app/routes.py)
JWT_SECRET = "your-super-secret-jwt-key-change-in-production"
JWT_ALGORITHM = "HS256"

def generate_admin_token():
    """Генерирует JWT токен для админки"""
    payload = {
        'admin': True,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=24)  # Токен действителен 24 часа
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_token(token):
    """Декодирует JWT токен для проверки"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return "Токен истек"
    except jwt.InvalidTokenError:
        return "Неверный токен"

if __name__ == "__main__":
    print("🔐 Генерация JWT токена для админки")
    print("=" * 50)
    
    # Генерируем токен
    token = generate_admin_token()
    print(f"✅ JWT токен сгенерирован:")
    print(f"📋 {token}")
    print()
    
    # Проверяем токен
    print("🔍 Проверка токена:")
    result = decode_token(token)
    if isinstance(result, dict):
        print(f"✅ Токен валиден")
        print(f"📅 Создан: {datetime.fromtimestamp(result['iat'])}")
        print(f"⏰ Истекает: {datetime.fromtimestamp(result['exp'])}")
    else:
        print(f"❌ {result}")
    
    print()
    print("🌐 Полный URL для админки:")
    print(f"📎 http://127.0.0.1:5000/{token}/admin")
    print()
    print("⚠️  ВАЖНО: Измените JWT_SECRET в продакшене!")