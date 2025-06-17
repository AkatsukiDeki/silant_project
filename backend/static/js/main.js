document.addEventListener('DOMContentLoaded', function() {
    // Активация фильтров в таблицах
    const filterForms = document.querySelectorAll('.filter-form');
    filterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const params = new URLSearchParams(formData);
            window.location.search = params.toString();
        });
    });

    // Сброс фильтров
    const resetButtons = document.querySelectorAll('.reset-filters');
    resetButtons.forEach(button => {
        button.addEventListener('click', function() {
            window.location.search = '';
        });
    });

    // Подтверждение удаления
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить эту запись?')) {
                e.preventDefault();
            }
        });
    });
});