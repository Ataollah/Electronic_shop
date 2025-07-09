from django.urls import path, re_path
from product.views import ShopListView, ProductDetailView,PriceInquiryRequestView

urlpatterns = [
    path('shop/',ShopListView.as_view(),name='shop-view'),
    path('price-inquiry/', PriceInquiryRequestView.as_view(), name='price-inquiry-view'),
    re_path(r'^detail/(?P<slug>[-\w]+)/', ProductDetailView.as_view(), name='product-detail-view'),
]