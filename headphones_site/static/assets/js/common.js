document.addEventListener('DOMContentLoaded', function () {
  const sideLogo = document.getElementById('sideLogo');
  const hero = document.querySelector('.hero');
  const container = document.querySelector('.hero .container');
  const topElement = document.getElementById('top');

  // Плавная прокрутка к верху по клику + редирект на главную
  if (sideLogo && topElement) {
    sideLogo.addEventListener('click', function(e) {
      e.preventDefault();
      if (window.location.pathname === '/') {
        topElement.scrollIntoView({ behavior: 'smooth' });
      } else {
        window.location.href = '/';
      }
    });

    sideLogo.addEventListener('mousedown', function() {
      this.style.transform = 'scale(0.98)';
    });

    sideLogo.addEventListener('mouseup', function() {
      this.style.transform = 'scale(1)';
    });

    sideLogo.addEventListener('mouseleave', function() {
      this.style.transform = 'scale(1)';
    });
  }

  const GAP = 2;

  function applyFixedLeft() {
    if (!sideLogo || !container) return;
    if (window.innerWidth <= 768) {
      sideLogo.style.left = '';
      return;
    }
    const containerRect = container.getBoundingClientRect();
    const logoWidth = sideLogo.offsetWidth;

    if (containerRect.left > 0 && logoWidth > 0) {
      const newLeft = containerRect.left - logoWidth - GAP;
      if (newLeft > 0) {
        sideLogo.style.left = newLeft + 'px';
      }
    }
  }

  function onScroll() {
    if (!sideLogo || !hero) return;
    const heroTop = hero.getBoundingClientRect().top + window.pageYOffset;

    // Мобильная логика
    if (window.innerWidth <= 768) {
      if (window.pageYOffset > 100) {
        sideLogo.classList.add('is-fixed');
      } else {
        sideLogo.classList.remove('is-fixed');
      }
      sideLogo.style.left = '';
      return;
    }

    // Десктопная логика
    if (window.pageYOffset >= heroTop) {
      sideLogo.classList.add('is-fixed');
      applyFixedLeft();
    } else {
      sideLogo.classList.remove('is-fixed');
      sideLogo.style.left = '';
    }
  }

  function onResize() {
    if (window.innerWidth <= 768) {
      if (sideLogo) {
        // Не удаляем класс is-fixed на мобильных
        sideLogo.style.left = '';
      }
      return;
    }
    if (sideLogo && sideLogo.classList.contains('is-fixed')) {
      applyFixedLeft();
    }
  }

  // Используем throttling для оптимизации scroll событий
  let ticking = false;
  function updateScroll() {
    onScroll();
    ticking = false;
  }

  function requestScrollUpdate() {
    if (!ticking) {
      requestAnimationFrame(updateScroll);
      ticking = true;
    }
  }

  // Добавляем поддержку touch событий для мобильных
  window.addEventListener('scroll', requestScrollUpdate, { passive: true });
  window.addEventListener('touchmove', requestScrollUpdate, { passive: true });

  window.addEventListener('resize', onResize);

  // Инициализация
  function initPosition() {
    if (sideLogo && sideLogo.classList.contains('is-fixed')) {
      applyFixedLeft();
    }
  }

  setTimeout(initPosition, 50);
  window.addEventListener('load', initPosition);

  // Эффекты наведения
  document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-4px)';
    });

    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });

  document.querySelectorAll('.tag, .badge').forEach(element => {
    element.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-2px)';
    });

    element.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });

  // Прокрутка карточек
  document.querySelectorAll('.card--scrollable').forEach(card => {
    card.addEventListener('scroll', function() {
      if (this.scrollLeft + this.clientWidth >= this.scrollWidth - 5) {
        this.setAttribute('data-scrolled', 'end');
      } else {
        this.removeAttribute('data-scrolled');
      }
    });

    if (card.scrollLeft + card.clientWidth >= card.scrollWidth - 5) {
      card.setAttribute('data-scrolled', 'end');
    }
  });
});
