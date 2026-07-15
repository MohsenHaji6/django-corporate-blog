const header = document.getElementById('header');
const container = document.getElementById('container');
const logo = document.getElementById('logo');

window.addEventListener('scroll', () => {
    if (window.scrollY > 85) {
        header.classList.add('top-0');
        container.classList.remove('h-22', 'bg-white');
        container.classList.add('h-16', 'backdrop-blur-xs');
        logo.classList.add('w-35');
    } else {
        header.classList.remove('top-0');
        container.classList.remove('h-16');
        container.classList.add('h-22', 'bg-white');
        logo.classList.remove('w-35');
    }
});
