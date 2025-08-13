// Navigation
let menuButton = document.getElementById('menu-button');
let menuElement = document.getElementById('menu-element');
let homeDiv = document.getElementById('home');
let aboutDiv = document.getElementById('about');
let shopDiv = document.getElementById('shop');
let reviewsDiv = document.getElementById('reviews');
let contactDiv = document.getElementById('contact');
let homeButton = document.getElementById('home-button');
let aboutButton = document.getElementById('about-button');
let shopButton = document.getElementById('shop-button');
let reviewsButton = document.getElementById('reviews-button');
let contactButton = document.getElementById('contact-button');
let closeButton = document.getElementById('close-button');


menuButton.onclick = () => {
    menuElement.style.display = 'flex';
}

closeButton.onclick = () => {
    menuElement.style.display = 'none';
}

homeButton.onclick = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    menuElement.style.display = 'none';
}

aboutButton.onclick = () => {
    aboutDiv.scrollIntoView({ behavior: 'smooth' })
    menuElement.style.display = 'none';
}

shopButton.onclick = () => {
    shopDiv.scrollIntoView({ behavior: 'smooth' })
    menuElement.style.display = 'none';
}

reviewsButton.onclick = () => {
    reviewsDiv.scrollIntoView({ behavior: 'smooth' })
    menuElement.style.display = 'none';
}

contactButton.onclick = () => {
    contactDiv.scrollIntoView({ behavior: 'smooth' })
    menuElement.style.display = 'none';
}
