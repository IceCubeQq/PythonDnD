document.addEventListener('DOMContentLoaded', function() {
    const statInputs = document.querySelectorAll('.stat-input');

    function calculateModifier(value) {
        return Math.floor((value - 10) / 2);
    }

    function updateModifierDisplay(input) {
        const value = parseInt(input.value) || 0;
        const modifier = calculateModifier(value);
        const label = input.parentElement.querySelector('label');
        const modifierText = modifier >= 0 ? `+${modifier}` : modifier.toString();
        const existingModifier = label.querySelector('.modifier-badge');

        if (existingModifier) {
            existingModifier.remove();
        }

        const badge = document.createElement('span');
        badge.className = `modifier-badge badge ms-2 ${modifier >= 0 ? 'bg-success' : 'bg-danger'}`;
        badge.textContent = modifierText;
        label.appendChild(badge);
    }
    statInputs.forEach(input => {
        input.addEventListener('input', function() {
            updateModifierDisplay(this);
        });

        if (input.value) {
            updateModifierDisplay(input);
        }
    });
    const form = document.getElementById('monsterForm');
    form.addEventListener('submit', function(e) {
        let isValid = true;
        const errorMessages = [];
        const requiredInputs = form.querySelectorAll('input[required], select[required]');
        requiredInputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add('is-invalid');
                errorMessages.push(`Поле "${input.previousElementSibling?.textContent || 'Неизвестное поле'}" обязательно для заполнения`);
            } else {
                input.classList.remove('is-invalid');
            }
        });
        const numberInputs = form.querySelectorAll('input[type="number"]');
        numberInputs.forEach(input => {
            if (input.value) {
                const value = parseInt(input.value);
                const min = parseInt(input.min) || -Infinity;
                const max = parseInt(input.max) || Infinity;

                if (value < min || value > max) {
                    isValid = false;
                    input.classList.add('is-invalid');
                    errorMessages.push(`Значение в поле "${input.previousElementSibling?.textContent || 'Неизвестное поле'}" должно быть от ${min} до ${max}`);
                }
            }
        });

        if (!isValid) {
            e.preventDefault();
            alert('Пожалуйста, исправьте следующие ошибки:\n\n' + errorMessages.join('\n'));
        }
    });
    statInputs.forEach(input => {
        input.addEventListener('mouseenter', function() {
            const value = parseInt(this.value) || 0;
            const modifier = calculateModifier(value);
            const tooltipText = `Модификатор: ${modifier >= 0 ? '+' : ''}${modifier}`;
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip bs-tooltip-top';
            tooltip.innerHTML = `
                <div class="tooltip-arrow"></div>
                <div class="tooltip-inner">${tooltipText}</div>
            `;

            const rect = this.getBoundingClientRect();
            tooltip.style.position = 'fixed';
            tooltip.style.top = (rect.top - 40) + 'px';
            tooltip.style.left = (rect.left + rect.width/2) + 'px';
            tooltip.style.transform = 'translateX(-50%)';

            this.tooltipElement = tooltip;
            document.body.appendChild(tooltip);
        });

        input.addEventListener('mouseleave', function() {
            if (this.tooltipElement) {
                this.tooltipElement.remove();
                this.tooltipElement = null;
            }
        });
    });
    function autoFillStats() {
        const autoFillBtn = document.createElement('button');
        autoFillBtn.type = 'button';
        autoFillBtn.className = 'btn btn-sm btn-outline-secondary mb-3';
        autoFillBtn.innerHTML = '<i class="bi bi-magic"></i> Заполнить стандартные значения';
        autoFillBtn.onclick = function() {
            document.getElementById('id_strength').value = 10;
            document.getElementById('id_dexterity').value = 10;
            document.getElementById('id_constitution').value = 10;
            document.getElementById('id_intelligence').value = 10;
            document.getElementById('id_wisdom').value = 10;
            document.getElementById('id_charisma').value = 10;
            statInputs.forEach(input => updateModifierDisplay(input));
        };

        const statsSection = document.querySelector('.border-bottom + .row');
        statsSection.parentNode.insertBefore(autoFillBtn, statsSection);
    }
    autoFillStats();
});