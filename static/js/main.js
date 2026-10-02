document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-confirm]').forEach(function (button) {
        button.addEventListener('click', function (event) {
            const message = button.getAttribute('data-confirm');
            if (!window.confirm(message)) {
                event.preventDefault();
            }
        });
    });

    document.querySelectorAll('.alert').forEach(function (alertBox) {
        setTimeout(function () {
            if (alertBox && alertBox.parentNode) {
                alertBox.classList.remove('show');
                setTimeout(function () {
                    alertBox.remove();
                }, 300);
            }
        }, 5000);
    });

    document.querySelectorAll('[data-password-toggle]').forEach(function (button) {
        button.addEventListener('click', function () {
            const targetId = button.getAttribute('data-password-toggle');
            const targetField = document.getElementById(targetId);
            if (!targetField) {
                return;
            }

            const isPassword = targetField.type === 'password';
            targetField.type = isPassword ? 'text' : 'password';
            button.textContent = isPassword ? 'Hide' : 'Show';
        });
    });
});
