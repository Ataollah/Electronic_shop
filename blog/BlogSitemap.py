from django.contrib.sitemaps import Sitemap
from .models import Post


class BlogSiteMap(Sitemap):

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.createdAt
