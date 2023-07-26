// hamburger 
hamburger = document.querySelector(".navbar-hamburger");
hamburger.onclick = function() {
    var navmain = document.querySelector('.navbar-main');
    navmain.classList.toggle('active');
}

// click on a
const navLis = document.querySelectorAll('.navbar-li')
navLis.forEach(navLi => {
    navLi.addEventListener('click', function() {
        const navA = this.querySelector('.navbar-a');
        if (navA) {
            navA.click();
        }
    })
})