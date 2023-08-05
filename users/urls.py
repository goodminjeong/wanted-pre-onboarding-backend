from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("signin/", views.SigninView.as_view(), name="signin"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
