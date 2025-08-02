// ===== ОСНОВА ПУТИ — Основной JavaScript =====

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всех модулей
    initFAQ();
    initStagesAnimation();
    initSmoothScroll();
    initVideoPlayer();
    initIntersectionObserver();
    initHeaderScroll();
    initOfflineEventsCarouselV2();
    initMobileSidebar();
    initPortraitsCarousel();
    initOrganizersCarousel();
    initProgramsCarousel();
    initModals();
    
    // Инициализация карты с небольшой задержкой
    setTimeout(() => {
    initMissionMap();
    }, 100);
});

// ===== FAQ АККОРДЕОН =====
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq__item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq__question');
        
        question.addEventListener('click', () => {
            // Закрываем все остальные элементы
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });
            
            // Переключаем текущий элемент
            item.classList.toggle('active');
        });
    });
}

// ===== АНИМАЦИЯ ЭТАПОВ С ПЛАВНЫМИ ПЕРЕХОДАМИ =====
// ===== ОТКЛЮЧАЕМ АНИМАЦИИ ЭТАПОВ =====
function initStagesAnimation() {
    // Отключаем анимации этапов
    console.log('Анимации этапов отключены');
}

// ===== ПЛАВНАЯ ПРОКРУТКА =====
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            const targetId = link.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===== ВИДЕО ПЛЕЙЕР =====
function initVideoPlayer() {
    const playBtn = document.getElementById('playVideoBtn');
    const videoCover = document.querySelector('.video-section__cover');
    
    if (playBtn && videoCover) {
        playBtn.addEventListener('click', () => {
            // Здесь можно добавить логику для открытия модального окна с видео
            // или встраивания iframe с YouTube/Vimeo
            
            // Пример для YouTube
            const videoId = 'YOUR_VIDEO_ID'; // Замените на реальный ID видео
            const iframe = document.createElement('iframe');
            iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
            iframe.width = '100%';
            iframe.height = '450';
            iframe.frameBorder = '0';
            iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
            
            videoCover.innerHTML = '';
            videoCover.appendChild(iframe);
        });
    }
}

// ===== INTERSECTION OBSERVER ДЛЯ АНИМАЦИЙ =====
function initIntersectionObserver() {
    // Отключаем все анимации загрузки
    console.log('Анимации загрузки отключены');
}

// ===== АНИМАЦИЯ HEADER ПРИ СКРОЛЛЕ =====
function initHeaderScroll() {
    const header = document.querySelector('.header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            header.style.background = 'rgba(10, 10, 10, 0.98)';
            header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.3)';
        } else {
            header.style.background = 'rgba(10, 10, 10, 0.95)';
            header.style.boxShadow = 'none';
        }
        
        // Скрытие/показ header при скролле
        if (scrollTop > lastScrollTop && scrollTop > 200) {
            header.style.transform = 'translateY(-100%)';
        } else {
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
}

// ===== КАРУСЕЛЬ ДЛЯ ОФФЛАЙН СОБЫТИЙ =====
function initOfflineEventsCarousel() {
    const carousel = document.querySelector('.offline-events__carousel');
    if (!carousel) return;
    
    let currentSlide = 0;
    const slides = carousel.querySelectorAll('.event-slide');
    const totalSlides = slides.length;
    
    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.style.transform = `translateX(${(i - index) * 100}%)`;
        });
    }
    
    // Автоматическое переключение слайдов
    setInterval(() => {
        currentSlide = (currentSlide + 1) % totalSlides;
        showSlide(currentSlide);
    }, 5000);
    
    // Инициализация первого слайда
    showSlide(0);
}

// ===== АНИМАЦИЯ ТЕКСТА (ТИППИНГ ЭФФЕКТ) =====
function initTypingEffect() {
    const heroTitle = document.querySelector('.hero__title');
    if (!heroTitle) return;
    
    const text = heroTitle.textContent;
    heroTitle.textContent = '';
    
    let i = 0;
    const typeWriter = () => {
        if (i < text.length) {
            heroTitle.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, 100);
        }
    };
    
    // Запускаем эффект печати
    setTimeout(typeWriter, 500);
}

// ===== ПЛАВНЫЕ ПЕРЕХОДЫ МЕЖДУ ЭТАПАМИ (ДОПОЛНИТЕЛЬНО) =====
function initStagesTransitions() {
    const stages = document.querySelectorAll('.stage');
    
    stages.forEach((stage, index) => {
        // Добавляем задержку для каждого этапа
        stage.style.transitionDelay = `${index * 0.2}s`;
        
        // Добавляем hover эффекты
        stage.addEventListener('mouseenter', () => {
            stage.style.transform = 'translateY(-15px) scale(1.05)';
            stage.style.boxShadow = '0 25px 50px rgba(191, 164, 107, 0.3)';
        });
        
        stage.addEventListener('mouseleave', () => {
            stage.style.transform = 'translateY(0) scale(1)';
            stage.style.boxShadow = '0 20px 40px rgba(191, 164, 107, 0.2)';
        });
    });
}

// ===== ИНИЦИАЛИЗАЦИЯ ДОПОЛНИТЕЛЬНЫХ МОДУЛЕЙ =====
document.addEventListener('DOMContentLoaded', function() {
    // Запускаем дополнительные анимации
    setTimeout(() => {
        initOfflineEventsCarousel();
        initTypingEffect();
        initStagesTransitions();
    }, 1000);
});

// ===== УТИЛИТЫ =====
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Оптимизированный обработчик скролла
window.addEventListener('scroll', debounce(() => {
    // Дополнительная логика при скролле
}, 10)); 

function initOfflineEventsCarouselV2() {
    // Используем события из Flask или статические по умолчанию
    const slides = window.eventsData && window.eventsData.length > 0 ? window.eventsData : [
        {
            title: 'Москва',
            desc: 'Столичный слёт. Город силы и встреч.',
            image: '/static/img/Moscow.png'
        },
        {
            title: 'Грузия: женская линия',
            desc: 'Уникальный женский круг. Горы, ритуалы, поддержка.',
            image: '/static/img/Georgia.png'
        },
        {
            title: 'Латвия 2025',
            desc: 'Сбор в лесу. Единение с природой и собой.',
            image: '/static/img/Latvia.png'
        }
    ];
    let current = 0;

    const bg = document.getElementById('offlineEventsBg');
    const title = document.getElementById('offlineEventTitle');
    const desc = document.getElementById('offlineEventDesc');
    const prev = document.getElementById('offlinePrev');
    const next = document.getElementById('offlineNext');

    if (!bg || !title || !desc || !prev || !next) {
        console.error('Элементы карусели событий не найдены');
        return;
    }

    function showSlide(idx) {
        // Анимация исчезновения
        title.style.opacity = 0;
        desc.style.opacity = 0;
        setTimeout(() => {
            // Проверяем, начинается ли путь с /static/
            let imagePath = slides[idx].image;
            if (!imagePath.startsWith('/static/') && !imagePath.startsWith('http')) {
                imagePath = '/static/' + imagePath;
            }
            bg.style.backgroundImage = `url(${imagePath})`;
            bg.style.backgroundSize = 'cover';
            bg.style.backgroundPosition = 'center';
            bg.style.backgroundRepeat = 'no-repeat';
            title.textContent = slides[idx].title;
            desc.textContent = slides[idx].desc;
            // Анимация появления
            title.style.opacity = 1;
            desc.style.opacity = 1;
        }, 250);
    }

    prev.addEventListener('click', () => {
        current = (current - 1 + slides.length) % slides.length;
        showSlide(current);
    });
    next.addEventListener('click', () => {
        current = (current + 1) % slides.length;
        showSlide(current);
    });

    // Инициализация
    showSlide(current);
} 

function initMissionMap() {
    console.log('Инициализация карты mission-cities...');
    const mapEl = document.getElementById('map');
    if (!mapEl) {
        console.error('Элемент карты не найден!');
        return;
    }
    console.log('Элемент карты найден:', mapEl);
    
    if (typeof L === 'undefined') {
        console.error('Leaflet.js не загружен!');
        return;
    }
    console.log('Leaflet.js загружен');
    
    // Получаем точки карты из глобальной переменной или используем статические данные
    const mapPoints = window.mapPoints || [
        { name: 'Красноярск', lat: 56.0184, lng: 92.8672, country: 'Россия', description: 'Столица Сибири. Город силы и встреч.' },
        { name: 'Тбилиси', lat: 41.7151, lng: 44.8271, country: 'Грузия', description: 'Уникальный женский круг. Горы, ритуалы, поддержка.' },
        { name: 'Рига', lat: 56.9496, lng: 24.1052, country: 'Латвия', description: 'Сбор в лесу. Единение с природой и собой.' }
    ];
    
    // Центр карты (примерно центр всех точек)
    const centerCoords = [55.0, 30.0];
    
    const map = L.map('map', {
        center: centerCoords,
        zoom: 3,
        scrollWheelZoom: true, // Включаем масштабирование колесиком мыши
        dragging: true,
        zoomControl: true,
        attributionControl: false,
        minZoom: 2,
        maxZoom: 18
    });
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: 'Leaflet | © OpenStreetMap contributors'
    }).addTo(map);
    
    // Добавляем маркеры для всех точек
    mapPoints.forEach(point => {
        const marker = L.marker([point.lat, point.lng]).addTo(map);
        
        // Создаем popup для каждой точки
        const popupContent = `
            <div class="city-popup-content">
                <div class="city-name">${point.name}</div>
                <div class="city-country">${point.country}</div>
                <div class="city-description">${point.description}</div>
            </div>
        `;
        
        marker.bindPopup(popupContent, {
            className: 'city-popup',
            closeButton: true
        });
    });
    
    console.log('Карта инициализирована успешно с', mapPoints.length, 'точками');
} 

function initMobileSidebar() {
    const burger = document.getElementById('headerBurger');
    const sidebar = document.getElementById('sidebarMenu');
    const closeBtn = document.getElementById('sidebarClose');
    const backdrop = document.getElementById('sidebarBackdrop');
    if (!burger || !sidebar || !closeBtn || !backdrop) return;

    function openSidebar() {
        sidebar.classList.add('open');
        backdrop.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
    function closeSidebar() {
        sidebar.classList.remove('open');
        backdrop.style.display = 'none';
        document.body.style.overflow = '';
    }
    burger.addEventListener('click', openSidebar);
    closeBtn.addEventListener('click', closeSidebar);
    backdrop.addEventListener('click', closeSidebar);
    // Закрытие по ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeSidebar();
    });
    // Закрытие по клику на ссылку
    sidebar.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', closeSidebar);
    });
} 

// ===== КАРУСЕЛЬ УЧАСТНИКОВ =====
function initPortraitsCarousel() {
    const slides = document.querySelectorAll('.portrait-slide');
    const dots = document.querySelectorAll('.portrait-dot');
    const prevBtn = document.getElementById('portraitPrev');
    const nextBtn = document.getElementById('portraitNext');
    
    let currentSlide = 0;
    const totalSlides = slides.length;
    
    function showSlide(index) {
        // Скрываем все слайды
        slides.forEach(slide => {
            slide.classList.remove('active');
        });
        
        // Убираем активный класс со всех точек
        dots.forEach(dot => {
            dot.classList.remove('active');
        });
        
        // Показываем нужный слайд
        slides[index].classList.add('active');
        dots[index].classList.add('active');
        
        // Убираем блокировку кнопок для бесконечной карусели
        // prevBtn.disabled = index === 0;
        // nextBtn.disabled = index === totalSlides - 1;
    }
    
    // Обработчики для кнопок с бесконечным переключением
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
            showSlide(currentSlide);
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            currentSlide = (currentSlide + 1) % totalSlides;
            showSlide(currentSlide);
        });
    }
    
    // Обработчики для точек
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            showSlide(currentSlide);
        });
    });
    
    // Автоматическое переключение каждые 5 секунд
    setInterval(() => {
        currentSlide = (currentSlide + 1) % totalSlides;
        showSlide(currentSlide);
    }, 10000);
    
    // Инициализация первого слайда
    showSlide(0);
} 

// ===== КАРУСЕЛЬ ОРГАНИЗАТОРОВ =====
function initOrganizersCarousel() {
    console.log('Инициализация карусели организаторов...');
    const list = document.querySelector('.organizers-list');
    const dots = document.querySelectorAll('.dot[data-index]');
    const prevBtn = document.getElementById('organizerPrev');
    const nextBtn = document.getElementById('organizerNext');
    
    if (!list) {
        console.log('Список организаторов не найден!');
        return;
    }
    
    console.log('Найдено точек:', dots.length);
    
    function next() {
        console.log('Следующий слайд');
        
        // Получаем все элементы организаторов
        const items = document.querySelectorAll('.organizer-item');
        const totalItems = items.length;
        
        if (totalItems === 0) return;
        
        // Находим текущий активный индекс
        let currentIndex = 0;
        items.forEach((item, index) => {
            if (item.classList.contains('act')) {
                currentIndex = index;
            }
        });
        
        // Вычисляем новые индексы
        const nextIndex = (currentIndex + 1) % totalItems;
        const prevIndex = (currentIndex - 1 + totalItems) % totalItems;
        const newNextIndex = (currentIndex + 2) % totalItems;
        
        // Убираем все классы
        items.forEach(item => {
            item.classList.remove('act', 'prev', 'next', 'new-next', 'hide');
        });
        
        // Устанавливаем новые классы
        items[currentIndex].classList.add('prev');
        items[nextIndex].classList.add('act');
        items[newNextIndex].classList.add('next');
        
        // Обновляем точки навигации
        updateDots(nextIndex);
    }

    function prev() {
        console.log('Предыдущий слайд');
        
        // Получаем все элементы организаторов
        const items = document.querySelectorAll('.organizer-item');
        const totalItems = items.length;
        
        if (totalItems === 0) return;
        
        // Находим текущий активный индекс
        let currentIndex = 0;
        items.forEach((item, index) => {
            if (item.classList.contains('act')) {
                currentIndex = index;
            }
        });
        
        // Вычисляем новые индексы
        const prevIndex = (currentIndex - 1 + totalItems) % totalItems;
        const newPrevIndex = (currentIndex - 2 + totalItems) % totalItems;
        
        // Убираем все классы
        items.forEach(item => {
            item.classList.remove('act', 'prev', 'next', 'new-next', 'hide');
        });
        
        // Устанавливаем новые классы
        items[newPrevIndex].classList.add('prev');
        items[prevIndex].classList.add('act');
        items[currentIndex].classList.add('next');
        
        // Обновляем точки навигации
        updateDots(prevIndex);
    }

    function updateDots(activeIndex) {
        // Убираем активный класс у всех точек
        dots.forEach(dot => dot.classList.remove('active'));
        
        // Активируем нужную точку
        if (dots[activeIndex]) {
            dots[activeIndex].classList.add('active');
        }
    }
    
    function slide(element) {
        /* Next slide */
        if (element.classList.contains('next')) {
            next();
        /* Previous slide */
        } else if (element.classList.contains('prev')) {
            prev();
        }
    }

    // Обработчики для кнопок
    if (prevBtn) {
        prevBtn.addEventListener('click', prev);
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', next);
    }
    
    // Обработчики для кликов по элементам
    list.addEventListener('click', (event) => {
        slide(event.target);
    });
    
    // Обработчики для точек
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            console.log('Клик по точке:', index);
            
            // Получаем все элементы организаторов
            const items = document.querySelectorAll('.organizer-item');
            const totalItems = items.length;
            
            if (totalItems === 0) return;
            
            // Убираем все классы
            items.forEach(item => {
                item.classList.remove('act', 'prev', 'next', 'new-next', 'hide');
            });
            
            // Вычисляем индексы для показа 3 элементов
            const prevIndex = (index - 1 + totalItems) % totalItems;
            const nextIndex = (index + 1) % totalItems;
            
            // Устанавливаем новые классы
            items[prevIndex].classList.add('prev');
            items[index].classList.add('act');
            items[nextIndex].classList.add('next');
            
            // Обновляем точки навигации
            updateDots(index);
        });
    });
    
    // Принудительная инициализация начального состояния
    console.log('Принудительная инициализация карусели организаторов...');
    const items = document.querySelectorAll('.organizer-item');
    const totalItems = items.length;
    
    if (totalItems > 0) {
        // Устанавливаем активным 2-й организатор (индекс 1)
        const activeIndex = 1;
        const prevIndex = (activeIndex - 1 + totalItems) % totalItems;
        const nextIndex = (activeIndex + 1) % totalItems;
        
        // Убираем все классы
        items.forEach(item => {
            item.classList.remove('act', 'prev', 'next', 'new-next', 'hide');
        });
        
        // Устанавливаем новые классы
        items[prevIndex].classList.add('prev');
        items[activeIndex].classList.add('act');
        items[nextIndex].classList.add('next');
        
        // Обновляем точки навигации
        updateDots(activeIndex);
        
        console.log('Карусель инициализирована с активным индексом:', activeIndex);
    }
} 

// ===== КАРУСЕЛЬ ПРОГРАММ =====
function initProgramsCarousel() {
    const slides = document.querySelectorAll('.program-slide');
    const dots = document.querySelectorAll('.program-dot');
    const prevBtn = document.getElementById('programPrev');
    const nextBtn = document.getElementById('programNext');
    
    if (!slides.length) return; // Если нет слайдов, выходим
    
    let currentSlide = 0;
    const totalSlides = slides.length;
    
    function showSlide(index) {
        // Скрываем все слайды
        slides.forEach(slide => {
            slide.classList.remove('active');
        });
        
        // Убираем активный класс со всех точек
        dots.forEach(dot => {
            dot.classList.remove('active');
        });
        
        // Показываем нужный слайд
        slides[index].classList.add('active');
        dots[index].classList.add('active');
    }
    
    // Обработчики для кнопок с бесконечным переключением
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
            showSlide(currentSlide);
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            currentSlide = (currentSlide + 1) % totalSlides;
            showSlide(currentSlide);
        });
    }
    
    // Обработчики для точек
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            showSlide(currentSlide);
        });
    });
    
    // Автоматическое переключение каждые 8 секунд (медленнее чем участники)
    setInterval(() => {
        currentSlide = (currentSlide + 1) % totalSlides;
        showSlide(currentSlide);
    }, 8000);
    
    // Инициализация первого слайда
    showSlide(0);
} 

// ===== МОДАЛЬНЫЕ ОКНА =====
function initModals() {
    const modalTriggers = document.querySelectorAll('[data-modal]');
    const modals = document.querySelectorAll('.modal');
    const modalCloses = document.querySelectorAll('.modal__close');
    
    // Открытие модального окна
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            const modalId = trigger.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            
            if (modal) {
                modal.classList.add('active');
                document.body.style.overflow = 'hidden'; // Блокируем скролл
            }
        });
    });
    
    // Закрытие модального окна по кнопке
    modalCloses.forEach(closeBtn => {
        closeBtn.addEventListener('click', () => {
            const modalId = closeBtn.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            
            if (modal) {
                modal.classList.remove('active');
                document.body.style.overflow = ''; // Возвращаем скролл
            }
        });
    });
    
    // Закрытие модального окна по клику на оверлей
    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal || e.target.classList.contains('modal__overlay')) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });
    
    // Закрытие модального окна по ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const activeModal = document.querySelector('.modal.active');
            if (activeModal) {
                activeModal.classList.remove('active');
                document.body.style.overflow = '';
            }
        }
    });
} 