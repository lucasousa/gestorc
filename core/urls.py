from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import permission_required
from django.urls import path

from .views import IndexView

app_name = "core"


urlpatterns = [
    # path('', permission_required('core:index', raise_exception=True)(IndexView.as_view()), name="index"),
    path("", IndexView.as_view(), name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/core/login"), name="logout"),
]
