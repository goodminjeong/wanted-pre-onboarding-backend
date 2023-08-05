from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source="user.email")

    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("id", "user", "created_at", "updated_at")
