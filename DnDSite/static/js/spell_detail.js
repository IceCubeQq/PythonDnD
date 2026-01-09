document.addEventListener('DOMContentLoaded', function() {
    const favoriteBtn = document.getElementById('favoriteBtn');
    const favoriteText = document.getElementById('favoriteText');

    if (favoriteBtn) {
        const contentType = favoriteBtn.dataset.type;
        const objectId = favoriteBtn.dataset.id;

        checkFavoriteStatus(contentType, objectId);
        favoriteBtn.addEventListener('click', function() {
            const action = this.dataset.action;
            toggleFavorite(contentType, objectId, action, this);
        });
    }

    function checkFavoriteStatus(contentType, objectId) {
        fetch(`/favorites/check/${contentType}/${objectId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.is_favorite) {
                    favoriteBtn.dataset.action = 'remove';
                    favoriteBtn.innerHTML = '<i class="bi bi-star-fill"></i> <span id="favoriteText">В избранном</span>';
                    favoriteBtn.classList.add('active');
                }
            });
    }

    function toggleFavorite(contentType, objectId, action, btn) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
        const originalHtml = btn.innerHTML;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
        btn.disabled = true;

        fetch('/favorites/toggle/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `content_type=${contentType}&object_id=${objectId}&action=${action}&csrfmiddlewaretoken=${csrfToken}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.action === 'added') {
                    btn.dataset.action = 'remove';
                    btn.innerHTML = '<i class="bi bi-star-fill"></i> <span id="favoriteText">В избранном</span>';
                    btn.classList.add('active');
                    showToast('success', data.message);
                } else if (data.action === 'removed') {
                    btn.dataset.action = 'add';
                    btn.innerHTML = '<i class="bi bi-star"></i> <span id="favoriteText">В избранное</span>';
                    btn.classList.remove('active');
                    showToast('success', data.message);
                }
            } else {
                showToast('error', data.message || 'Ошибка');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('error', 'Ошибка сети');
        })
        .finally(() => {
            btn.disabled = false;
        });
    }

    function showToast(type, message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
        alertDiv.style.zIndex = '9999';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alertDiv);

        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }
});