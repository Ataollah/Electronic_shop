from django.urls import path
from .views import AddToCartView, CartView, DeleteMiniCartItemView, DeleteAllCartItems

urlpatterns = [
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart-items/', CartView.as_view(), name='cart-items'),
    path('delete-mini-cart-item/', DeleteMiniCartItemView.as_view(), name='delete-mini-cart-item'),
    path('delete-all-items/',DeleteAllCartItems.as_view(), name='delete-all-items'),
]
