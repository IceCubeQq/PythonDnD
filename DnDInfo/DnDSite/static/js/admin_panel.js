document.addEventListener('DOMContentLoaded', function() {
    function getCsrfToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return decodeURIComponent(value);
            }
        }
        return '';
    }

    const csrfToken = getCsrfToken();

    function setupCheckboxHandlers(selectAllBtnId, checkAllId, checkboxClass, counterId) {
        const selectAllBtn = document.getElementById(selectAllBtnId);
        const checkAll = document.getElementById(checkAllId);
        const checkboxes = document.querySelectorAll(`.${checkboxClass}`);
        const counter = document.getElementById(counterId);

        function updateCounter() {
            const checkedCount = document.querySelectorAll(`.${checkboxClass}:checked`).length;
            if (counter) counter.textContent = checkedCount;
        }
        if (selectAllBtn) {
            selectAllBtn.addEventListener('click', function() {
                const allChecked = Array.from(checkboxes).every(cb => cb.checked);
                checkboxes.forEach(cb => {
                    cb.checked = !allChecked;
                });
                if (checkAll) checkAll.checked = !allChecked;
                updateCounter();
            });
        }
        if (checkAll) {
            checkAll.addEventListener('change', function() {
                checkboxes.forEach(cb => {
                    cb.checked = this.checked;
                });
                updateCounter();
            });
        }
        checkboxes.forEach(cb => {
            cb.addEventListener('change', function() {
                const allChecked = Array.from(checkboxes).every(c => c.checked);
                if (checkAll) checkAll.checked = allChecked;
                updateCounter();
            });
        });

        updateCounter();
    }

    setupCheckboxHandlers('selectAllMonsters', 'checkAllMonsters', 'monster-checkbox', 'selectedCountMonsters');
    setupCheckboxHandlers('selectAllSpells', 'checkAllSpells', 'spell-checkbox', 'selectedCountSpells');
    setupCheckboxHandlers('selectAllEquipment', 'checkAllEquipment', 'equipment-checkbox', 'selectedCountEquipment');

    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('approve-btn') ||
            (e.target.parentElement && e.target.parentElement.classList.contains('approve-btn'))) {
            e.preventDefault();
            const btn = e.target.classList.contains('approve-btn') ? e.target : e.target.parentElement;
            const type = btn.dataset.type;
            const id = btn.dataset.id;

            const typeNames = {
                'monster': 'монстра',
                'spell': 'заклинание',
                'equipment': 'снаряжение'
            };

            const typeName = typeNames[type] || 'элемент';

            if (confirm(`Одобрить этот ${typeName}?`)) {
                const originalHtml = btn.innerHTML;
                btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
                btn.disabled = true;

                fetch(`/admin-panel/approve/${type}/${id}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `csrfmiddlewaretoken=${encodeURIComponent(csrfToken)}`
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const row = btn.closest('tr');
                        if (row) {
                            row.style.opacity = '0.5';
                            setTimeout(() => {
                                row.remove();
                                updateTableCounters(type);
                                location.reload();
                            }, 500);
                        }
                        showToast('success', data.message);
                    } else {
                        showToast('error', `Ошибка: ${data.error}`);
                        btn.innerHTML = originalHtml;
                        btn.disabled = false;
                    }
                })
                .catch(error => {
                    showToast('error', `Ошибка сети: ${error}`);
                    btn.innerHTML = originalHtml;
                    btn.disabled = false;
                });
            }
        }

        if (e.target.classList.contains('reject-btn') ||
            (e.target.parentElement && e.target.parentElement.classList.contains('reject-btn'))) {
            e.preventDefault();
            const btn = e.target.classList.contains('reject-btn') ? e.target : e.target.parentElement;
            const type = btn.dataset.type;
            const id = btn.dataset.id;

            const typeNames = {
                'monster': 'монстра',
                'spell': 'заклинание',
                'equipment': 'снаряжение'
            };

            const typeName = typeNames[type] || 'элемент';

            if (confirm(`Отклонить этот ${typeName}? Это действие нельзя отменить.`)) {
                const originalHtml = btn.innerHTML;
                btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
                btn.disabled = true;

                fetch(`/admin-panel/reject/${type}/${id}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `csrfmiddlewaretoken=${encodeURIComponent(csrfToken)}`
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const row = btn.closest('tr');
                        if (row) {
                            row.style.opacity = '0.5';
                            setTimeout(() => {
                                row.remove();
                                updateTableCounters(type);
                                location.reload();
                            }, 500);
                        }
                        showToast('success', data.message);
                    } else {
                        showToast('error', `Ошибка: ${data.error}`);
                        btn.innerHTML = originalHtml;
                        btn.disabled = false;
                    }
                })
                .catch(error => {
                    showToast('error', `Ошибка сети: ${error}`);
                    btn.innerHTML = originalHtml;
                    btn.disabled = false;
                });
            }
        }
    });

    function updateTableCounters(type) {
        const counters = {
            'monster': {
                badge: document.querySelector('#monsters-tab .badge'),
                table: document.querySelectorAll('.monster-checkbox').length
            },
            'spell': {
                badge: document.querySelector('#spells-tab .badge'),
                table: document.querySelectorAll('.spell-checkbox').length
            },
            'equipment': {
                badge: document.querySelector('#equipment-tab .badge'),
                table: document.querySelectorAll('.equipment-checkbox').length
            }
        };

        if (counters[type]) {
            const counter = counters[type];
            if (counter.badge) {
                counter.badge.textContent = counter.table;
            }
        }
    }

    function showToast(type, message) {
        let toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                max-width: 350px;
            `;
            document.body.appendChild(toastContainer);
        }

        const toastId = 'toast-' + Date.now();
        const toast = document.createElement('div');
        toast.id = toastId;
        toast.className = `toast align-items-center text-white bg-${type === 'success' ? 'success' : 'danger'} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        toastContainer.appendChild(toast);

        const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
        bsToast.show();

        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    }

    const bulkForms = document.querySelectorAll('form[id$="Form"]');
    bulkForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const selectedItems = this.querySelectorAll('input[name="selected_items"]:checked');
            if (selectedItems.length === 0) {
                e.preventDefault();
                showToast('error', 'Выберите хотя бы один элемент.');
                return;
            }

            const actionBtn = e.submitter;
            const action = actionBtn.value;
            const content_type = this.querySelector('input[name="content_type"]').value;

            const typeNames = {
                'monster': 'монстров',
                'spell': 'заклинаний',
                'equipment': 'предметов снаряжения'
            };

            const typeName = typeNames[content_type] || 'элементов';
            const actionText = action === 'approve' ? 'одобрить' : 'отклонить';

            if (!confirm(`Вы уверены, что хотите ${actionText} ${selectedItems.length} ${typeName}?`)) {
                e.preventDefault();
            } else {
                actionBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Обработка...';
                actionBtn.disabled = true;
            }
        });
    });

    const moderationTabs = document.querySelectorAll('#moderationTabs button[data-bs-toggle="tab"]');
    moderationTabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function(e) {
            localStorage.setItem('activeModerationTab', e.target.id);
        });
    });

    const activeTabId = localStorage.getItem('activeModerationTab');
    if (activeTabId) {
        const activeTab = document.getElementById(activeTabId);
        if (activeTab) {
            const tab = new bootstrap.Tab(activeTab);
            tab.show();
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        const urlParams = new URLSearchParams(window.location.search);
        const activeTabParam = urlParams.get('tab');

        if (activeTabParam) {
            const tabElement = document.getElementById(`${activeTabParam}-tab`);
            if (tabElement) {
                const tab = new bootstrap.Tab(tabElement);
                tab.show();
            }
        }
        const bulkForms = document.querySelectorAll('form[id$="Form"]');
        bulkForms.forEach(form => {
            form.addEventListener('submit', function() {
                const activeTab = document.querySelector('#moderationTabs .nav-link.active');
                if (activeTab) {
                    const tabId = activeTab.id.replace('-tab', '');

                    const originalAction = this.action;
                    const separator = originalAction.includes('?') ? '&' : '?';
                    this.action = originalAction + separator + 'tab=' + tabId;
                }
            });
        });
    });
});