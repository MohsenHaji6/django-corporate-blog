document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.querySelectorAll('.toast').forEach((el) => {
            el.remove();
        });
    }, 4000);

    const form = document.getElementById('form');

    if (form?.dataset.scroll === 'true') {
        form.scrollIntoView();
    }
});
