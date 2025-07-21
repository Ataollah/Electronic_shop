from curses.ascii import controlnames

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from Utility.SmsSender import SmsSender
from appuser.mixin import CustomerRequiredMixin
from product.models import Product, Category, ProductVisit, Brands
from siteInfo.cache.site_info_cache import getSiteInfo
from .models import PriceInquiryRequest


# Create your views here.


class ShopListView(ListView):
    model = Product
    template_name = 'product/Shop/shop.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        products = Product.objects.all()
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        sort = self.request.GET.get('SortBy', 'manual')
        brand_ids = self.request.GET.getlist('brands')

        if category:
            products = products.filter(category=category)

        if search:
            products = products.filter(title__icontains=search)

        if brand_ids:
            products = products.filter(brand__id__in=brand_ids)

        if sort == 'title-ascending':
            products = products.order_by('title')
        elif sort == 'title-descending':
            products = products.order_by('-title')
        elif sort == 'price-ascending':
            products = products.order_by('current_price')
        elif sort == 'price-descending':
            products = products.order_by('-current_price')
        elif sort == 'created-ascending':
            products = products.order_by('id')
        elif sort == 'created-descending':
            products = products.order_by('-id')

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand_ids = self.request.GET.getlist('brands')
        context['categories'] = Category.objects.annotate(product_count=Count('product')).order_by('order')
        context['selected_category'] = self.request.GET.get('category', None)
        context['number_of_products'] = Product.objects.all().count()
        context['brands'] = Brands.objects.all().order_by('order')
        context['selected_brands'] = brand_ids
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/SingleProduct/single_product.html'
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(category=self.object.category).exclude(
            id=self.object.id).order_by('?')[:4]
        context['siteInfo'] = getSiteInfo()
        context['questions'] = self.object.questions.all().order_by('order')

        return context

    def get(self,request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        product = self.get_object()
        user = request.user if request.user.is_authenticated else None
        ip = request.META.get('REMOTE_ADDR')
        device = request.META.get('HTTP_USER_AGENT', '')
        ProductVisit.objects.create(
            user=user,
            product=product,
            ip_address=None if user else ip,
            device_info=device
        )
        return response



class PriceInquiryRequestView(LoginRequiredMixin, CustomerRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=request.POST.get('product_id'))
        user = request.user

        inquiry = PriceInquiryRequest.objects.filter(user=user, product=product, status='waiting').first()
        if inquiry:
            return render(request, 'product/InquiryExisted/already_existed.html', {'inquiry': inquiry})

        PriceInquiryRequest.objects.create(user=user, product=product, status='waiting')
        sender = SmsSender()
        sender.send_sms(
            to=user.username,
            message=f'درخواست استعلام قیمت برای محصول {product.title} با موفقیت ثبت شد. منتظر تماس ما باشید.'
        )
        sender.send_sms(
            to=getSiteInfo().sell_mobile,
            message=f'درخواست استعلام قیمت برای محصول {product.title} توسط مشتری {user.username}ثبت شده است '
        )

        return render(request, 'product/InquirySuccess/inquiry_success.html', {'product': product})