let addButtons = document.querySelectorAll('.update-cart')


for (let i = 0; i < addButtons.length; i++) {
    addButtons[i].addEventListener('click', () => {

        // this dataset is html method to access custom attribute
        // it is coming from home.html >> data-product="{{ product.id }}"
        let productId = addButtons[i].dataset.product
        let action = addButtons[i].dataset.action
        //console.log('productId :', productId, 'action :', action)        //updateCartTotal()

        // user variable is coming from home.html
        // from within script tag where user is defined with requst.user
        // since user is declared within script tag and globally available
        // user variable is readilly available for usage
        console.log('User :', user)
        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)

        } else {
            updateUserOrder(productId, action);
        }
    })
}

function updateUserOrder(productId, action) {
    console.log("User is authenticated, sending data...");
    var url = "/update_item/";
    fetch(url, {
        method: 'POST',
        headers: {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log("data:", data)
            // reload the page
            location.reload()
        })
}


function addCookieItem(productId, action) {


    if (action == 'add') {

        console.log("cart[productId] : ", cart[productId])

        // this 'cart' is coming from base.html where it is declared 
        // and available globallly
        if (cart[productId] == undefined) {
            // create new cookie for that productId with js object
            cart[productId] = { 'quantity': 1 }

        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <= 0) {
            console.log('Remove Item')
            delete cart[productId]

        }

    }
    console.log('cart:', cart)
    document.cookie = `cart= ${JSON.stringify(cart)};domain=;path=/`
    location.reload()
}