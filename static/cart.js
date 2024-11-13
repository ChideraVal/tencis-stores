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

$(document).ready(function () {
    // Add to cart

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
                    button.text('Remove From Cart');
                    button.css({
                        'background-color': '#ddd', // Change background
                        'color': 'red', // Change text color
                    });
                } else {
                    button.text('Add To Cart');
                    button.css({
                        'background-color': 'black', // Change background
                        'color': 'white', // Change text color
                    });
                }
                console.log(response.cartItemCount);
                $('#cart-count').text(response.cartItemCount);
                $('#cart-count-2').text(`${response.cartItemCount} product${response.cartItemCount === 1 ? '' : 's'}`);
                document.getElementById(`cart-total-items`).textContent = `${response.cartTotalItems}`;
                document.getElementById(`cart-total-price`).textContent = `₦${response.cartTotalPrice}`;
                // Update cart count if necessary
                document.getElementById(`div-${product_id}`).style.display = 'none';
                if (response.cartItemCount === 0) {
                    $('#checkout-button').prop('disabled', true);
                    $('#checkout-button').css({
                        'background-color': '#ddd', // Change background
                        'color': '#999', // Change text color
                    });
                }
            },
            error: function (xhr, status, error) {
                console.error(error); // Handle errors
            }
        });
    });

    // Increase quantity
    $('.incr').click(function (e) {
        e.preventDefault();
        var cartproduct_id = $(this).data('id');
        // Get the cartproduct ID from the button's data attribute
        $.ajax({
            type: 'POST',
            url: `/increase/${cartproduct_id}/`, // Django URL for increasing quantity

            success: function (response) {
                document.getElementById(`qty-${cartproduct_id}`).textContent = response.cartProductCount;
                document.getElementById(`price-${cartproduct_id}`).textContent = `₦${response.totalPrice}`;
                document.getElementById(`cart-total-items`).textContent = `${response.cartTotalItems}`;
                document.getElementById(`cart-total-price`).textContent = `₦${response.cartTotalPrice}`;
                // document.getElementById(`info-price`).textContent = `$${response.cartTotalPrice}`;
            },
            error: function (xhr, status, error) {
                console.error(error); // Handle errors
            }
        });
    });

    // Decrease quantity
    $('.decr').click(function (e) {
        e.preventDefault();
        var cartproduct_id = $(this).data('id');
        let qty = document.getElementById(`qty-${cartproduct_id}`).textContent;
        if (qty == 1) {
            alert('Quantity cannot be less than 1!')
            return;
        }
        // Get the cartproduct ID from the button's data attribute
        $.ajax({
            type: 'POST',
            url: `/decrease/${cartproduct_id}/`, // Django URL for increasing quantity

            success: function (response) {
                document.getElementById(`qty-${cartproduct_id}`).textContent = response.cartProductCount;
                document.getElementById(`price-${cartproduct_id}`).textContent = `₦${response.totalPrice}`;
                document.getElementById(`cart-total-items`).textContent = `${response.cartTotalItems}`;
                document.getElementById(`cart-total-price`).textContent = `₦${response.cartTotalPrice}`;
                // document.getElementById(`info-price`).textContent = `$${response.cartTotalPrice}`;
            },
            error: function (xhr, status, error) {
                console.error(error); // Handle errors
            }
        });
    });
});