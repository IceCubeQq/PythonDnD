document.addEventListener('DOMContentLoaded', function() {
    const levelInput = document.getElementById('id_level');
    const form = document.getElementById('spellForm');

    if (!form) return;

    if (levelInput) {
        levelInput.addEventListener('change', function() {
            validateLevelInput(this);
        });

        levelInput.addEventListener('input', function() {
            validateLevelInput(this);
        });
    }

    form.addEventListener('submit', function(e) {
        const validationResult = validateSpellForm(form, levelInput);

        if (!validationResult.isValid) {
            e.preventDefault();
            alert('Исправьте следующие ошибки:\n\n' + validationResult.errors.join('\n'));
        } else {
            const isHomebrew = form.dataset.isHomebrew === 'true';
            const isAdmin = form.dataset.isAdmin === 'true';

            if (!isAdmin && isHomebrew) {
                if (!confirm('После сохранения заклинание будет отправлено на повторное рассмотрение администратором. Продолжить?')) {
                    e.preventDefault();
                    return;
                }
            }

            disableSubmitButton(form);
        }
    });

    function validateLevelInput(input) {
        if (!input.value.trim()) {
            input.classList.remove('is-invalid');
            return;
        }

        const level = parseInt(input.value);
        if (isNaN(level) || level < 0 || level > 9) {
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    }
    function validateSpellForm(form, levelInput) {
        let isValid = true;
        const errors = [];
        const requiredInputs = form.querySelectorAll('[required]');
        requiredInputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add('is-invalid');
                const fieldName = getFieldLabel(input) || input.name;
                errors.push(`Поле "${fieldName}" обязательно для заполнения`);
            }
        });

        if (levelInput && levelInput.value.trim()) {
            const level = parseInt(levelInput.value);
            if (isNaN(level) || level < 0 || level > 9) {
                isValid = false;
                levelInput.classList.add('is-invalid');
                errors.push('Уровень заклинания должен быть от 0 до 9');
            }
        }

        const componentCheckboxes = form.querySelectorAll('input[name="components"]:checked');
        if (componentCheckboxes.length === 0) {
            isValid = false;
            errors.push('Необходимо выбрать хотя бы один компонент заклинания');
        }

        return {
            isValid: isValid,
            errors: errors
        };
    }

    function getFieldLabel(input) {
        const label = input.previousElementSibling;
        if (label && label.tagName === 'LABEL') {
            return label.textContent;
        }

        const labelById = document.querySelector(`label[for="${input.id}"]`);
        if (labelById) {
            return labelById.textContent;
        }

        return null;
    }

    function disableSubmitButton(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Сохранение...';
        }
    }

    const componentCheckboxes = form.querySelectorAll('input[name="components"]');
    componentCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const checkedCount = form.querySelectorAll('input[name="components"]:checked').length;
            if (checkedCount === 0) {
                console.log('Необходимо выбрать хотя бы один компонент');
            }
        });
    });
});