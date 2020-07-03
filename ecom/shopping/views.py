from .models import *
import json
import datetime
from ecom import settings
from django.shortcuts import render
from django.http import JsonResponse
from .utils import *


def home(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'cartItems': cartItems, 'products': products}
    return render(request, 'shopping/home.html', context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context = {'cartItems': cartItems, 'items': items, 'order': order}
    return render(request, 'shopping/cart.html', context)


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'shopping/checkout.html', context)


def processOrder(request):

    transactionId = datetime.datetime.now().timestamp()
    data = json.loads(request.body.decode('utf-8'))
    print(f'data: {data}')

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:

        customer, order = guestOrder(request, data)

    total = data['form']['total']
    order.transaction_id = transactionId

    print(f'total: {total}')
    print(f'order.get_cart_total_price: {order.get_cart_total_price}')
    print(total == order.get_cart_total_price)
    if total == float(order.get_cart_total_price):
        order.complete = True
    order.save()

    if order.shipping == True:

        customer = customer
        order = order
        address = data['shippingInfo']['address']
        address2 = data['shippingInfo']['address2']
        city = data['shippingInfo']['city']
        state = data['shippingInfo']['state']
        zipcode = data['shippingInfo']['zip']

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=address,
            address2=address2,
            city=city,
            state=state,
            zipcode=zipcode

        )

    return JsonResponse("Processed Order", safe=False)


def updateItem(request):

    # this 'request.body' is coming from '
    # cart.js >> updateUserOrder >>  body: JSON.stringify({ 'productId': productId, 'action': action })
    # whenever we click Add to Cart button this json body is available to use thru addEventListener
    # this data is coming as dictionary
    data = json.loads(request.body.decode('utf-8'))
    productId = data['productId']
    action = data['action']

    # get the customer
    customer = request.user.customer

    # get the product that customer added to cart
    product = Product.objects.get(id=productId)

    # create an order if not exist with this customer and complete=false
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    # create or get orderitem with above order
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    print(orderItem)

    # logic to add or remove item in cart
    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)


def confirmOrder(request):
    # data = json.loads(request.body.decode('utf-8'))
    # print(data)
    context = {}
    return render(request, 'shopping/confirmation.html', context)
