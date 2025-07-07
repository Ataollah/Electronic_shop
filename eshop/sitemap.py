from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):

    def items(self):
        return ["about-us", "contact-us", "faq","home","privacy-policy","term-of-use"]

    def location(self, obj):
        return reverse(obj)

