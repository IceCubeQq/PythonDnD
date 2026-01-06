document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('equipmentForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;

            const nameInput = document.getElementById('id_name');
            if (!nameInput.value.trim()) {
                isValid = false;
                nameInput.classList.add('is-invalid');
            } else {
                nameInput.classList.remove('is-invalid');
            }

            const weightInput = document.getElementById('id_weight');
            if (weightInput.value && parseFloat(weightInput.value) < 0) {
                isValid = false;
                weightInput.classList.add('is-invalid');
            } else {
                weightInput.classList.remove('is-invalid');
            }

            const costInput = document.getElementById('id_cost_quantity');
            if (costInput.value && parseFloat(costInput.value) < 0) {
                isValid = false;
                costInput.classList.add('is-invalid');
            } else {
                costInput.classList.remove('is-invalid');
            }

            if (!isValid) {
                e.preventDefault();
                alert('Пожалуйста, проверьте правильность заполнения полей.');
            }
        });
    }
});