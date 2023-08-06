from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.ArticleView.as_view(), name="article"),
    path("<int:article_id>/", views.ArticleDetailView.as_view(), name="article-detail"),
]
