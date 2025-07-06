from curses.ascii import controlnames
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from product.models import Product, Category
from siteInfo.cache.site_info_cache import getSiteInfo


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

        if category:
            products = products.filter(category=category)

        if search:
            products = products.filter(title__icontains=search)

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
        context['categories'] = Category.objects.annotate(product_count=Count('product')).order_by('order')
        context['selected_category'] = self.request.GET.get('category', None)
        context['number_of_products'] = Product.objects.all().count()
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








