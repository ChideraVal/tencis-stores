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
    let orderIdValue = document.getElementById('order_id').value;
    let amountValue = document.getElementById('amount').value;
    let emailValue = document.getElementById('email').value;
    let phoneValue = document.getElementById('phone').value;
    let firstNameValue = document.getElementById('first_name').value;
    let lastNameValue = document.getElementById('last_name').value;

    FlutterwaveCheckout({
        public_key: "FLWPUBK-4665a5bfdd9fe8535fa8c74f0d845b09-X",
        tx_ref: `${orderIdValue}`,
        amount: Number(amountValue),
        currency: "NGN",
        payment_options: "card, ussd, banktransfer, account, internetbanking, nqr, applepay, googlepay, enaira, opay",
        customer: {
            email: `${emailValue}`,
            phone_number: Number(phoneValue),
            name: `${firstNameValue} ${lastNameValue}`,
        },
        customizations: {
            title: "Tencis Stores",
            description: "Pay now to complete your purchase and verify your order.",
        },
        callback: function (payment) {
            open(`https://store.tencis.online/verify/${orderIdValue}/${payment.transaction_id}/`, '_parent')
        },
    });
}
