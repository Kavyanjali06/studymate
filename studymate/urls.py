from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path

from blog.sitemaps import BlogSitemap

handler404 = "planner.views.custom_404"
handler500 = "planner.views.custom_500"

sitemaps = {
    "blog": BlogSitemap,
}

ROBOTS_TXT = """User-agent: *
Allow: /
Sitemap: https://studymate-rho-rouge.vercel.app/sitemap.xml
"""


def robots_txt(request):
    return HttpResponse(ROBOTS_TXT, content_type="text/plain")


urlpatterns = [
    path("", include("planner.urls")),
    path("blog/", include("blog.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
]
