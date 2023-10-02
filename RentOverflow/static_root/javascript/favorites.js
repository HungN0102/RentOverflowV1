var map = L.map('map').setView([51.505, -0.09], 8);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


////// heart button
const heartButtons = document.querySelectorAll('.btn--heart');
heartButtons.forEach(button => {
    button.addEventListener('click', function (e) {
        e.preventDefault();

        const heartIcon = this.querySelector('.fa-heart'); // Find the .fa-heart icon within the clicked button
        heartIcon.classList.toggle('fa-heart-o');
        heartIcon.classList.toggle('color-red');
    });
});