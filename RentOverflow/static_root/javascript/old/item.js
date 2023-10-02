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

    const count = listing.querySelector('.listing-count-number'); 
    count.textContent = '1/' + slides.length
});

// hamburger 
hamburger = document.querySelector(".navbar-hamburger");
hamburger.onclick = function() {
    var navmain = document.querySelector('.navbar-main');
    navmain.classList.toggle('active');

}