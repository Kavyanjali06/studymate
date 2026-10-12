from django.contrib.sitemaps import Sitemap

from .data.articles import ARTICLES
from .utils import PRODUCTION_DOMAIN


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ARTICLES

    def location(self, item):
        return f"/blog/{item['slug']}/"

    def lastmod(self, item):
        return item.get("updated_date") or item.get("published_date")
