document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.querySelectorAll('.toast').forEach((el) => {
            el.remove();
        });
    }, 3000);
});
