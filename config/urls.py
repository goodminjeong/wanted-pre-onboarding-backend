from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="pre-onboarding-backend API",
        default_version="1.1.1",
        description="원티드 프리온보딩-백엔드 과정 사전 과제입니다.",
        contact=openapi.Contact(email="ehdro418@naver.com"),
        license=openapi.License(name="mit"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(
        r"swagger(?P<format>\.json|\.yaml)",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        r"swagger",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        r"redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc-v1"
    ),
    path("admin/", admin.site.urls),
    path("api/articles/", include("articles.urls")),
    path("api/users/", include("users.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
