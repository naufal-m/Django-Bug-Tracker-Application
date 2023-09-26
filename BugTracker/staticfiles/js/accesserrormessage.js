  document.addEventListener('DOMContentLoaded', function() {
            const formFields = document.querySelectorAll('.form-field');

            formFields.forEach(field => {
                field.addEventListener('input', () => {
                    if (field.validity.valid) {
                        field.classList.remove('invalid');
                    } else {
                        field.classList.add('invalid');
                    }
                });

                field.addEventListener('focus', () => {
                    field.classList.add('focus');
                });

                field.addEventListener('blur', () => {
                    field.classList.remove('focus');
                });
            });
        });