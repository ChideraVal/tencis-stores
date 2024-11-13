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

// Make payment on flutterwave
function makePayment() {
    FlutterwaveCheckout({
        public_key: "FLWPUBK-4665a5bfdd9fe8535fa8c74f0d845b09-X",
        tx_ref: "{{ order.order_id }}",
        amount: Number("{{ order.get_total_price }}"),
        currency: "NGN",
        payment_options: "card, mobilemoneyghana, ussd",
        customer: {
            email: "{{ order.email }}",
            phone_number: Number("{{ order.phone }}"),
            name: "{{ order.first_name }} {{ order.last_name }}",
        },
        customizations: {
            title: "Tencis Stores",
            description: "Pay now to complete your purchase and verify your order.",
        },
        callback: function (payment) {
            open(`https://tencis-stores.onrender.com/verify/{{ order.id }}/${payment.transaction_id}`, '_parent')
        },
    });
}