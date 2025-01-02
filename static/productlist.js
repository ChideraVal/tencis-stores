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

// Add to cart
$(document).ready(function () {
    $('.add-to-cart').click(function (e) {
        e.preventDefault();
        var product_id = $(this).data('id');
        var button = $(this);
        // Get the product ID from the button's data attribute
        $.ajax({
            type: 'POST',
            url: `/add-to-cart/${product_id}/`, // Django URL for adding to cart
            success: function (response) {
                alert(response.message); // Show a message when the item is added to the cart
                if (response.status === 'added') {
                    button.text('Added To Cart');
                    button.css({
                        'background-color': '#ddd', // Change background
                        'color': 'black', // Change text color
                    });
                } else {
                    button.text('Add To Cart');
                    button.css({
                        'background-color': 'black', // Change background
                        'color': 'white', // Change text color
                    });
                }
                $('#cart-count').text(response.cartItemCount); // Update cart count if necessary
            },
            error: function (xhr, status, error) {
                console.error(error); // Handle errors
            }
        });
    });
});