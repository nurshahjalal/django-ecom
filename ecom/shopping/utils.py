import json
from .models import *


def cookieCart(request):
    """
    we need to update the get_cart_total_item and get_cart_total_price

    """
    try:
        # get the cart cookies
        cartCookie = json.loads(request.COOKIES['cart'])
    except:
        cartCookie = {}

    # Create empty cart for now for non-logged in user
    items = []
    order = {'get_cart_total': 0,
             'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for cookie in cartCookie:

        try:

            # get all cart items count
            cartItems += cartCookie[cookie]['quantity']

            # get the product with id
            product = Product.objects.get(id=cookie)

            # get total price of each item
            total = product.price * cartCookie[cookie]['quantity']

            order['get_cart_total'] += total
            order['get_cart_items'] += cartCookie[cookie]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'price': product.price,
                    'image': product.image,
                    'name': product.name
                },
                'quantity': cartCookie[cookie]['quantity'],
                'total_price': total
            }

            items.append(item)

            if product.digital == False:
                order['shipping'] = True

        except:
            pass

    return {'cartItems': cartItems, 'items': items, 'order': order}


def cartData(request):

    if request.user.is_authenticated:

        # Customer and User has one to one relationship
        customer = request.user.customer

        # get the customer order if not create one
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

        # orderitem is the child model of order
        # get all items from that particular order
        items = order.orderitem_set.all()

        print(f'items: {items}')
        cartItems = order.get_cart_total_item
        #print(f'cartItems: {cartItems}')

    else:
        # ======================================
        # for guest user
        # ======================================
        carts = cookieCart(request)
        cartItems = carts['cartItems']
        items = carts['items']
        order = carts['order']

    return {'cartItems': cartItems, 'items': items, 'order': order}


def guestOrder(request, data):

    print(f'User is not logged in')

    # print(f'Cookies: {request.COOKIES}')

    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    # print(f'items: {items}')

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    # print(f'customer: {customer}')

    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer,
                                 complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(product=product,
                                             order=order, quantity=item['quantity'])

    return customer, order
