document.addEventListener('DOMContentLoaded', function () {
    const title = document.getElementById('id_title');
    const metaTitle = document.getElementById('id_meta_title');

    let autoFill = true;

    metaTitle.addEventListener('input', function () {
        autoFill = false;
    });

    title.addEventListener('input', function () {
        if (autoFill) {
            metaTitle.value = title.value;
        }
    });
});