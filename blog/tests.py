from django.test import TestCase
from django.urls import reverse

from blog.data.articles import ARTICLES


class BlogTests(TestCase):
    def test_blog_list_loads(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Study Smarter, Not Harder")

    def test_blog_list_shows_articles(self):
        response = self.client.get(reverse("blog:post_list"))
        for article in ARTICLES[:3]:
            self.assertContains(response, article["title"])

    def test_blog_search_works(self):
        response = self.client.get(reverse("blog:post_list"), {"q": "timetable"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Study Timetable")

    def test_blog_search_no_results(self):
        response = self.client.get(reverse("blog:post_list"), {"q": "xyznotarealterm123"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No articles found")

    def test_blog_category_filter(self):
        response = self.client.get(reverse("blog:post_list"), {"category": "study-planning"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Study Planning")

    def test_every_article_has_detail_page(self):
        for article in ARTICLES:
            response = self.client.get(reverse("blog:post_detail", args=[article["slug"]]))
            self.assertEqual(response.status_code, 200, msg=f"Failed for slug: {article['slug']}")
            self.assertContains(response, article["title"])

    def test_article_detail_has_breadcrumbs(self):
        article = ARTICLES[0]
        response = self.client.get(reverse("blog:post_detail", args=[article["slug"]]))
        self.assertContains(response, "Home")
        self.assertContains(response, "Blog")

    def test_article_detail_has_faqs(self):
        article = ARTICLES[0]
        response = self.client.get(reverse("blog:post_detail", args=[article["slug"]]))
        self.assertContains(response, "Frequently Asked Questions")

    def test_article_detail_has_related(self):
        article = ARTICLES[0]
        response = self.client.get(reverse("blog:post_detail", args=[article["slug"]]))
        self.assertContains(response, "Related Articles")

    def test_unknown_article_returns_404(self):
        response = self.client.get(reverse("blog:post_detail", args=["non-existent-article"]))
        self.assertEqual(response.status_code, 404)

    def test_blog_list_has_seo_meta(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertContains(response, 'rel="canonical"')
        self.assertContains(response, "og:title")
        self.assertContains(response, "application/ld+json")

    def test_article_detail_has_seo_meta(self):
        article = ARTICLES[0]
        response = self.client.get(reverse("blog:post_detail", args=[article["slug"]]))
        self.assertContains(response, 'rel="canonical"')
        self.assertContains(response, "og:type")
        self.assertContains(response, "BlogPosting")
        self.assertContains(response, "BreadcrumbList")

    def test_sitemap_exists(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        for article in ARTICLES:
            self.assertContains(response, article["slug"])

    def test_robots_txt_exists(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sitemap:")
        self.assertContains(response, "Allow: /")
