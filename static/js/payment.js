// Navigation
let menuButton = document.getElementById('menu-button');
let menuElement = document.getElementById('menu-element');
let homeDiv = document.getElementById('home');
let shopDiv = document.getElementById('shop');
let aboutDiv = document.getElementById('about');
let reviewsDiv = document.getElementById('reviews');
let contactDiv = document.getElementById('contact');
let homeButton = document.getElementById('home-button');
let shopButton = document.getElementById('shop-button');
let aboutButton = document.getElementById('about-button');
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
    open('/#', '_parent')
}

aboutButton.onclick = () => {
    open('/#about', '_parent')
}

shopButton.onclick = () => {
    open('/#shop', '_parent')
}

reviewsButton.onclick = () => {
    open('/#reviews', '_parent')
}

contactButton.onclick = () => {
    contactDiv.scrollIntoView({ behavior: 'smooth' })
    menuElement.style.display = 'none';
}
