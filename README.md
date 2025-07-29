# ОСНОВА ПУТИ

Веб-сайт для закрытой системы мужской трансформации.

## Установка и запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите приложение:
```bash
python run.py
```

3. Откройте браузер и перейдите по адресу: `http://127.0.0.1:5000`

## Админка с JWT авторизацией

### Генерация JWT токена
```bash
python generate_jwt.py
```

### Доступ к админке
- **Формат URL**: `http://127.0.0.1:5000/{JWT_TOKEN}/admin`
- **Авторизация**: JWT токен прямо в URL
- **Срок действия**: 24 часа

### Как использовать:
1. Запустите `python generate_jwt.py`
2. Скопируйте полный URL из вывода
3. Откройте URL в браузере

### Пример URL:
```
http://127.0.0.1:5000/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6dHJ1ZSwiaWF0IjoxNzUzNzc4NjQ5LCJleHAiOjE3NTM4NjUwNDl9.9cll4-INksn4ZCnsTReMNn5-mvwLEvFBqgGPhZ3zDPQ/admin
```

### Функции админки
- **Добавление участников**: Загрузка фото и текста
- **Просмотр участников**: Список всех добавленных участников
- **Удаление участников**: Удаление с подтверждением

### Структура данных участника
```json
{
  "id": "уникальный-id",
  "name": "👨‍🦰 Массажист из Швейцарии",
  "text": "«Я касался сотен тел, но не чувствовал своего»",
  "story": "Полная история участника...",
  "photo": "img/character/filename.jpg"
}
```

### Файлы данных
- Участники сохраняются в: `app/data/participants.json`
- Фото сохраняются в: `app/static/img/character/`

## Структура проекта

```
Main_Way_Lending/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   ├── templates/
│   │   ├── components/
│   │   └── admin/
│   ├── data/
│   ├── __init__.py
│   ├── config.py
│   └── routes.py
├── requirements.txt
├── generate_jwt.py
└── run.py
```

## Технологии

- **Backend**: Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **База данных**: JSON файлы
- **Аутентификация**: JWT токены (PyJWT)

## Безопасность

⚠️ **Важно**: В продакшене обязательно измените:
- `JWT_SECRET` в `app/routes.py` и `generate_jwt.py`
- Используйте HTTPS
- Ограничьте доступ к админке по IP
- Регулярно обновляйте токены 