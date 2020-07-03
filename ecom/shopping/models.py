from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinLengthValidator, MaxLengthValidator
from phone_field import PhoneField


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    phone = phone = PhoneField(blank=True)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(default='default.png')

    def __str__(self):
        return self.name


# This refers to the Cart
class Order(models.Model):

    # this is ManyToOne Relationship with Customer model
    # meaning one customer can have multiple orders
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(default=timezone.now)
    complete = models.BooleanField(default=False, null=True)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    # checking which products needs to ship physically

    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()

        for i in orderItems:
            if i.product.digital == False:
                shipping = True

        print(f'orderItems >>>>: {orderItems} ')
        print(f'shipping >>>>>: {shipping} ')
        return shipping

    @property
    def get_cart_total_price(self):
        items = self.orderitem_set.all()

        # now items has all property available from OrderItem
        return sum([item.total_price for item in items])

    @property
    def get_cart_total_item(self):

        items = self.orderitem_set.all()
        # now items has all property available from OrderItem
        return sum([item.quantity for item in items])


# this refers the item in cart
class OrderItem(models.Model):

    # this is ManyToOne Relationship with Order(cart) model
    # meaning one cart can have multiple items
    # one order can have multiple item
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,  null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,  null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    # date that added that ite
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL,  null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,  null=True)
    address = models.CharField(max_length=200, null=False)
    address2 = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=50, null=False)
    zipcode = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
