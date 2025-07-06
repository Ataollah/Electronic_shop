from django.shortcuts import render, redirect
from django.urls import reverse
from product.models import Product
from siteInfo.cache.site_info_cache import getSiteInfo
from .models import CartItem,Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from appuser.mixin import CustomerRequiredMixin
from django.shortcuts import render
from django.views import View
# Create your views here.


class AddToCartView(LoginRequiredMixin,CustomerRequiredMixin,View):
    def post(self, request):
        if not getSiteInfo().is_selling:
            return redirect(reverse('home'))
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('qty', 1))
        print('product_id and qty in add to cart')
        print(product_id)
        print(quantity)

        cart, created = Cart.objects.get_or_create(user=request.user)

        product = Product.objects.get(id=product_id)
        product.inventory = product.inventory - quantity
        product.save()
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
            price=product.current_price,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect(reverse('cart-items'))



class CartView(LoginRequiredMixin,CustomerRequiredMixin,View):
    template_name = 'cart/CartItem/cart_items.html'

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        context = {'total_price':cart.totalPrice(),'cart_items':cart_items}
        return render(self.request, self.template_name, context)

    def post(self, request):
        cart_item_id = request.POST.get('cart_item_id')
        print('cart_item_id ro delete : ', cart_item_id)
        CartItem.objects.get(id=cart_item_id).delete()
        return self.get(request)


class DeleteMiniCartItemView(LoginRequiredMixin, CustomerRequiredMixin, View):
    # python
    def get_redirect_url(self, request):
        return request.META.get('HTTP_REFERER', reverse('cart-items'))

    def post(self, request):
        cart_item_id = request.POST.get('cart_item_id')
        CartItem.objects.get(id=cart_item_id).delete()
        return redirect(self.get_redirect_url(request))

class DeleteAllCartItems(LoginRequiredMixin,CustomerRequiredMixin,View):

    def post(self, request):
        cart = request.user.cart
        cart_items = cart.items.all()
        for item in cart_items:
            item.delete()
        return redirect('cart-items')
