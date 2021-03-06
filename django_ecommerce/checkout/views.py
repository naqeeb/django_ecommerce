from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import redirect, render, get_object_or_404
from django.template import RequestContext

import random
from core.models import Store, Order, OrderItem
from cart.models import Cart, CartItem
from core.services import CreateOrderService

@login_required
def checkout(request, template_name='checkout/complete.html'):
    response = {
        'store': None,
        'order': None,
        'order_items': None
    }

    # Get the current store
    store = Store.objects.get(id=1)

    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Create Order
    create_order_service = CreateOrderService(request.user, store)
    order = create_order_service.create(cart.total)
    response['order'] = order

    # Convert cart to order
    order_items = []
    for cart_item in cart_items:
        order_item = OrderItem.objects.create(order=order,
                                              quantity=cart_item.quantity,
                                              price=cart_item.product.price,
                                              product=cart_item.product)
        order_items.append(order_item)
        cart_item.delete()

    response['order_items'] = order_items
    cart.delete()

    return render(request, template_name, context=response)
