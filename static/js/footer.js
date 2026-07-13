document.getElementById('subscribe-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch(this.action, {
        method: 'POST',
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            const error = document.getElementById('phone_number_error');
            const msg = document.getElementById('message');
            if (data.success) {
                error.innerHTML = '';
                msg.innerHTML = '✅ ' + data.message;
                this.reset();
            } else {
                msg.innerHTML = '';
                error.innerHTML = '❌ ' + data.errors.phone_number[0];
            }
        });
});
