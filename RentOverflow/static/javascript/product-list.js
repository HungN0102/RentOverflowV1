// screenwidth
let screenWidth; 

function handleResize() {
    screenWidth = window.innerWidth; 
    const labelMinPrice = document.querySelector('#label-min-price');
    const labelMaxPrice = document.querySelector('#label-max-price');
    const labelMinBed = document.querySelector('#label-min-bed');
    const labelMaxBed = document.querySelector('#label-max-bed');

    const MinPrice = document.querySelector('#min-price');
    const MaxPrice = document.querySelector('#max-price');
    const MinBed = document.querySelector('#min-bed');
    const MaxBed = document.querySelector('#max-bed');

    if (screenWidth < 1000) {
        labelMinPrice.textContent = (MinPrice.value === 'Choose...') ? 'Min Price' : 'From ' + MinPrice.value + ' PCM';
        labelMaxPrice.textContent = (MaxPrice.value === 'Choose...') ? 'Max Price' : 'To ' + MaxPrice.value + ' PCM';
        labelMinBed.textContent = (MinBed.value === 'Choose...') ? 'Min Bed' : 'From ' + MinBed.value;
        labelMaxBed.textContent = (MaxBed.value === 'Choose...') ? 'Max Bed' : 'To ' + MaxBed.value;
    } else {
        labelMinPrice.textContent ='Min Price'
        labelMaxPrice.textContent ='Max Price'
        labelMinBed.textContent ='Min Bed'
        labelMaxBed.textContent ='Max Bed'
    }
}

handleResize();
window.addEventListener("resize", handleResize);


// hamburger 
hamburger = document.querySelector(".navbar-hamburger");
hamburger.onclick = function() {
    var navmain = document.querySelector('.navbar-main');
    navmain.classList.toggle('active');

}

// filter option 
filterBtn = document.querySelector(".header__form-filter");
filterBtn.onclick = function() {
    var collapseSec = document.querySelector('.header__form-collapse');
    collapseSec.classList.toggle('active');
}

// label show selected option
const selects = document.querySelectorAll('.form-control');
selects.forEach((select) => {
    const group = select.closest('.collapse__group');
    const label = group.querySelector('label');

    select.addEventListener('change', () => {
        if ((screenWidth <= 1000) && (select.value !== 'Choose...') && (select.classList.contains('min-price')))  {
            label.textContent = 'From ' + select.value + ' PCM';
        } else if ((screenWidth <= 1000) && (select.value !== 'Choose...') && (select.classList.contains('max-price')))  {
            label.textContent = 'To ' + select.value + ' PCM';
        } else if ((screenWidth <= 1000) && (select.value !== 'Choose...') && (select.classList.contains('min-bed')))  {
            label.textContent = 'From ' + select.value;
        } else if ((screenWidth <= 1000) && (select.value !== 'Choose...') && (select.classList.contains('max-bed')))  {
            label.textContent = 'To ' + select.value;
        } else if ((screenWidth <= 1000) && (select.value === 'Choose...') && (select.classList.contains('min-price')))  {
            label.textContent = 'Min Price'
        } else if ((screenWidth <= 1000) && (select.value === 'Choose...') && (select.classList.contains('max-price')))  {
            label.textContent = 'Max Price'
        } else if ((screenWidth <= 1000) && (select.value === 'Choose...') && (select.classList.contains('min-bed')))  {
            label.textContent = 'Min Bed'
        } else if ((screenWidth <= 1000) && (select.value === 'Choose...') && (select.classList.contains('max-bed')))  {
            label.textContent = 'Max Bed'
        } 
    })
})


// sliding pictures

const listings = document.querySelectorAll('.listing');

const goNext = (button) => {
    const listing = button.closest('.listing');
    const slides = listing.querySelectorAll('.slide');
    const count = listing.querySelector('.listing-count-number');
    const counter = parseInt(listing.dataset.counter) || 0;

    if (counter <= slides.length - 2) {
        listing.dataset.counter = counter + 1;
        count.textContent = String(counter+2) + '/' + slides.length;
        slideImage(listing);
    }
};

const goPrev = (button) => {
    const listing = button.closest('.listing');
    const slides = listing.querySelectorAll('.slide');
    const count = listing.querySelector('.listing-count-number');
    const counter = parseInt(listing.dataset.counter) || 0;

    if (counter > 0) {
        listing.dataset.counter = counter - 1;
        count.textContent = String(counter) + '/' + slides.length;
        slideImage(listing)
    } 
};

const slideImage = (listing) => {
    const slides = listing.querySelectorAll('.slide');
    const counter = parseInt(listing.dataset.counter) || 0;

    slides.forEach((slide) => {
        slide.style.transform = `translateX(-${counter * 100}%)`;
    });
};

listings.forEach((listing) => {
    const slides = listing.querySelectorAll('.slide');
    slides.forEach((slide, index) => {
        slide.style.left = `${index * 100}%`;
    });

    const counts = listing.querySelectorAll('.listing-count-number'); 
    counts.forEach((count, index) => {
        count.textContent = '1/' + slides.length
    });
});

// shorten text in text-sub
function limitTextBasedOnScreenWidth() {
    var textSubElements = document.getElementsByClassName('text-sub');
    var screenWidth = window.innerWidth;
    
    Array.from(textSubElements).forEach(function(element) {
        var text = element.innerText;
        var words = text.split(' ');
        var limitedText = '';
        if (screenWidth >= 1500) {
            console
            if (words.length > 40) {
                limitedText = words.slice(0, 40).join(' ') + '...';
            }
        } else if (screenWidth <= 911) {
            if (words.length > 25) {
                limitedText = words.slice(0, 20).join(' ') + '...';
            }
        } else if (screenWidth <=1100) {
            if (words.length > 30) {
                limitedText = words.slice(0, 30).join(' ') + '...';
            }
        } 

        if (limitedText) {
            element.innerText = limitedText;
        }
    });
}

// Call the function initially
limitTextBasedOnScreenWidth();

// Add event listener for window resize
window.addEventListener('resize', limitTextBasedOnScreenWidth);


// map leaflet
var map = L.map('map').setView([51.505, -0.09], 8);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// sort
const selectElement = document.getElementById('sort');
selectElement.addEventListener('change', function () {
    let sortOption = document.getElementById('sortOption')
    sortOption.value = selectElement.value
    sortOption.text = selectElement.value

    const button = document.querySelector('.submit');
    button.click()
});