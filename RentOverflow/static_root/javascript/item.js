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

    const count = listing.querySelector('.listing-count-number'); 
    count.textContent = '1/' + slides.length
});

// popup open
share = document.querySelector(".btn--share");
share.onclick = function() {
    var popup = document.querySelector('.popup');
    popup.classList.toggle('active');
}

// popup close
function closePopup(event) {
    var popup = document.querySelector('.popup');
    popup.classList.toggle('active');
}

cancelButton = document.querySelector(".cancel");
cancelButton.addEventListener('click', closePopup)

xButton = document.querySelector(".popup-box--close");
xButton.addEventListener('click', closePopup)

// popup link url
function copyURL(event) {
    // Get the URL text from the span
    const urlSpan = document.getElementById('urlToCopy');
    const urlText = urlSpan.innerText;
    
    // Create a temporary input element to copy the text
    const tempInput = document.createElement('input');
    tempInput.setAttribute('value', urlText);
    document.body.appendChild(tempInput);
    
    // Select and copy the text
    tempInput.select();
    document.execCommand('copy');
    
    // Remove the temporary input element
    document.body.removeChild(tempInput);

    var popup = document.querySelector('.popup');
    popup.classList.toggle('active');
}

copyButton = document.querySelector(".btn--copy");
copyButton.addEventListener('click', copyURL)