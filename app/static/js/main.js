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
    initMissionMap();
    initMobileSidebar();
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
function initStagesAnimation() {
    const stages = document.querySelectorAll('.stage');
    let currentStage = 0;
    
    // Функция показа следующего этапа
    function showNextStage() {
        if (currentStage < stages.length) {
            stages[currentStage].classList.add('visible');
            currentStage++;
            
            // Плавный переход к следующему этапу через 1 секунду
            if (currentStage < stages.length) {
                setTimeout(showNextStage, 1000);
            }
        }
    }
    
    // Запускаем анимацию при скролле к секции этапов
    const stagesSection = document.querySelector('.stages');
    if (stagesSection) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    showNextStage();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });
        
        observer.observe(stagesSection);
    }
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
    const animatedElements = document.querySelectorAll('.portrait, .value, .event-slide');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(element);
    });
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
    const slides = [
        {
            title: 'Москва',
            desc: 'Столичный слёт. Город силы и встреч.',
            bg: 'linear-gradient(120deg, #666 0%, #222 100%)'
        },
        {
            title: 'Грузия: женская линия',
            desc: 'Уникальный женский круг. Горы, ритуалы, поддержка.',
            bg: 'linear-gradient(120deg, #3a3a3a 0%, #6e5e4a 100%)'
        },
        {
            title: 'Латвия 2025',
            desc: 'Сбор в лесу. Единение с природой и собой.',
            bg: 'linear-gradient(120deg, #2a2a2a 0%, #4a6e5e 100%)'
        }
    ];
    let current = 0;

    const bg = document.getElementById('offlineEventsBg');
    const title = document.getElementById('offlineEventTitle');
    const desc = document.getElementById('offlineEventDesc');
    const prev = document.getElementById('offlinePrev');
    const next = document.getElementById('offlineNext');

    function showSlide(idx) {
        // Анимация исчезновения
        title.style.opacity = 0;
        desc.style.opacity = 0;
        setTimeout(() => {
            bg.style.background = slides[idx].bg;
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
    const mapEl = document.getElementById('communityMap');
    if (!mapEl) return;
    if (typeof L === 'undefined') {
        console.error('Leaflet.js не загружен!');
        return;
    }
    // Координаты Москвы
    const moscow = [55.751244, 37.618423];
    const map = L.map('communityMap', {
        center: moscow,
        zoom: 5,
        scrollWheelZoom: false,
        dragging: true,
        zoomControl: true,
        attributionControl: false
    });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(map);
    // Можно добавить маркер: L.marker(moscow).addTo(map)
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