import pytest
from app import create_app


@pytest.fixture
def app():
    """Создание тестового приложения."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Создание тестового клиента."""
    return app.test_client()


def test_index_route(client):
    """Тест главной страницы."""
    response = client.get('/')
    assert response.status_code == 200
    assert 'ОСНОВА ПУТИ' in response.data.decode('utf-8')


def test_index_contains_all_sections(client):
    """Тест наличия всех основных секций на главной странице."""
    response = client.get('/')
    data = response.data.decode('utf-8')
    
    # Проверяем наличие всех основных секций
    sections = [
        'header',
        'hero',
        'stages',
        'who-we-are',
        'values',
        'video-section',
        'mission',
        'offline-events',
        'faq',
        'final-cta',
        'footer'
    ]
    
    for section in sections:
        assert section in data, f"Секция {section} не найдена на странице"


def test_css_loaded(client):
    """Тест загрузки CSS файла."""
    response = client.get('/static/css/main.css')
    assert response.status_code == 200
    assert 'text/css' in response.headers.get('Content-Type', '')


def test_js_loaded(client):
    """Тест загрузки JavaScript файла."""
    response = client.get('/static/js/main.js')
    assert response.status_code == 200
    assert 'text/javascript' in response.headers.get('Content-Type', '')


def test_404_route(client):
    """Тест обработки несуществующих маршрутов."""
    response = client.get('/nonexistent')
    assert response.status_code == 404


def test_header_content(client):
    """Тест содержимого header."""
    response = client.get('/')
    data = response.data.decode('utf-8')
    
    # Проверяем наличие элементов header
    assert 'header__logo' in data
    assert 'header__nav' in data
    assert 'header__cta-btn' in data


def test_hero_section_content(client):
    """Тест содержимого hero секции."""
    response = client.get('/')
    data = response.data.decode('utf-8')
    
    # Проверяем наличие элементов hero
    assert 'hero__title' in data
    assert 'hero__subtitle' in data
    assert 'hero__actions' in data


def test_stages_section_content(client):
    """Тест содержимого секции этапов."""
    response = client.get('/')
    data = response.data.decode('utf-8')
    
    # Проверяем наличие элементов stages
    assert 'stages__carousel' in data
    assert 'stage' in data
    assert '28 дней Пути' in data
    assert 'ЯДРО' in data
    assert 'СБОРКА 30 дней' in data
    assert '2.0' in data


def test_values_section_content(client):
    """Тест содержимого секции ценностей."""
    response = client.get('/')
    data = response.data.decode('utf-8')
    
    # Проверяем наличие элементов values
    assert 'values__title' in data
    assert 'Наши ценности' in data
    assert 'value__name' in data
    assert 'value__desc' in data
    assert 'Чистота' in data
    assert 'Сила' in data
    assert 'Глубина' in data


def test_faq_section_content(client):
    """Тест содержимого FAQ секции."""
    response = client.get('/')
    data = response.data.decode('utf-8')
    
    # Проверяем наличие FAQ элементов
    assert 'faq__item' in data
    assert 'faq__question' in data
    assert 'faq__answer' in data
    assert 'Кому здесь не место?' in data
    assert 'Как попасть?' in data 