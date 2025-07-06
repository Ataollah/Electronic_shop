from django import template

from cart.models import Cart

register = template.Library()


@register.simple_tag(takes_context=True)
def cartItemsCount(context):
    user = context['request'].user
    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()
        print('cart : ',cart)
        if cart:
            return cart.items.count()
    return 0


@register.inclusion_tag('Layout/Base/Components/Header/Components/mini_cart.html',takes_context=True)
def mini_cart(context):
    user = context['request'].user
    try:
        if user.is_authenticated:
            cart = Cart.objects.filter(user=user).first()
            cart_items = cart.items.all()
            total_price = sum(item.get_total_price() for item in cart_items)
            return {'total_price': total_price, 'cart_items': cart_items}
    except Exception as e :
        return {}
    return {}




