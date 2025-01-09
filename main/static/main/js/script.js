document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('.profile-pic').onclick = function() {
        const popup = document.querySelector('.profile-popup');
        if (popup.style.display === 'none' || popup.style.display === '') {
            popup.style.display = 'flex';
        }
        else {
            popup.style.display = 'none';
        }
    };
});