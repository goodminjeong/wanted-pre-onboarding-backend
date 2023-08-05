from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article
from .serializers import ArticleSerializer


class ArticleView(APIView):
    def get_permissions(self):  # 권한 설정
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def post(self, request):  # 게시글 작성
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            {
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "message": "게시글 등록 완료!",
            },
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, article_id=None):
        if article_id:  # 특정 게시글 조회
            article = get_object_or_404(Article, id=article_id)
            serializer = ArticleSerializer(article)
            return Response(
                {
                    "data": serializer.data,
                    "status": status.HTTP_200_OK,
                    "message": "게시글 조회 성공!",
                },
                status=status.HTTP_200_OK,
            )
        else:  # 게시글 목록 조회
            articles = Article.objects.all()
            pagination = PageNumberPagination()
            paginated_articles = pagination.paginate_queryset(articles, request)
            serializer = ArticleSerializer(paginated_articles, many=True)
            return pagination.get_paginated_response(serializer.data)
