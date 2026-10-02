from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

handler404 = "planner.views.custom_404"
handler500 = "planner.views.custom_500"

urlpatterns = [
    path("", include("planner.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("admin/", admin.site.urls),
]
