const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
const html = document.documentElement;
const savedTheme = localStorage.getItem('theme') || 'light';
if (savedTheme === 'dark') {
    html.setAttribute('data-bs-theme', 'dark');
    themeIcon.className = 'bi bi-sun-fill';
} else {
    html.setAttribute('data-bs-theme', 'light');
    themeIcon.className = 'bi bi-moon-fill';
}

themeToggle.addEventListener('click', () => {
    if (html.getAttribute('data-bs-theme') === 'dark') {
        html.setAttribute('data-bs-theme', 'light');
        themeIcon.className = 'bi bi-moon-fill';
        localStorage.setItem('theme', 'light');
    } else {
        html.setAttribute('data-bs-theme', 'dark');
        themeIcon.className = 'bi bi-sun-fill';
        localStorage.setItem('theme', 'dark');
    }
    updateThemeDependentElements();
});

function updateThemeDependentElements() {
    const customCards = document.querySelectorAll('.card.bg-light, .card.bg-white');
    customCards.forEach(card => {
        card.classList.toggle('bg-dark', html.getAttribute('data-bs-theme') === 'dark');
        card.classList.toggle('text-white', html.getAttribute('data-bs-theme') === 'dark');
    });
}

setTimeout(function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    });
}, 5000);

$(document).ready(function() {
    const currentPath = window.location.pathname + window.location.search;
    $('.nav-link, .dropdown-item').each(function() {
        const linkPath = $(this).attr('href');
        if (linkPath && currentPath.includes(linkPath.split('?')[0]) && linkPath !== '/') {
            $(this).addClass('active');
            $(this).parents('.dropdown').find('.dropdown-toggle').addClass('active');
        }
    });
});

document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
        const submitButton = this.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Обработка...';
        }
    });
});