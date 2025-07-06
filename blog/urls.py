from django.urls import path, re_path
from blog.views import  BlogView, BlogDetailView

urlpatterns = [
    path('list/', BlogView.as_view(), name='blog-view'),
  #  path('<slug:slug>/', blog_detail_view, name='blog-detail-view'),
    re_path(r'^detail/(?P<slug>[-\w]+)/', BlogDetailView.as_view(), name='blog-detail-view'),

]