# ОСНОВА ПУТИ — Лендинг

## Описание
Профессиональный лендинг для закрытой системы перерождения «ОСНОВА ПУТИ». Реализован на Flask с использованием стандартных HTML-шаблонов и анимаций на JavaScript. Проект структурирован по современным best practices, легко масштабируется и поддерживается.

## Структура проекта
```
Main_Way_Lending/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       └── components/
│           ├── header.html
│           ├── hero.html
│           ├── stages.html
│           ├── who_we_are.html
│           ├── values.html
│           ├── video_section.html
│           ├── mission.html
│           ├── offline_events.html
│           ├── faq.html
│           ├── final_cta.html
│           └── footer.html
├── tests/
├── requirements.txt
├── README.md
└── run.py
```

## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone <repo_url>
   cd Main_Way_Lending
   ```
2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Запуск
```bash
python run.py
```

## Тестирование
```bash
pytest
```

## Масштабируемость
- Каждый блок лендинга реализован отдельным компонентом (шаблон + JS).
- Легко добавлять новые секции, менять порядок, кастомизировать стили.
- Возможность интеграции с backend/API для динамического наполнения.

## Контакты
- Email: example@mail.com
- Telegram: @osnovaputi

--- 