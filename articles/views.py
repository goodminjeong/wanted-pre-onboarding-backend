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
                "message": "게시글 등록 성공!",
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
            articles = Article.objects.all().order_by("-id")
            pagination = PageNumberPagination()
            paginated_articles = pagination.paginate_queryset(articles, request)
            serializer = ArticleSerializer(paginated_articles, many=True)
            return pagination.get_paginated_response(serializer.data)

    def put(self, request, article_id):  # 게시글 수정
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            serializer = ArticleSerializer(article, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "data": serializer.data,
                    "status": status.HTTP_200_OK,
                    "message": "게시글 수정 성공!",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": status.HTTP_403_FORBIDDEN,
                    "message": "권한이 없습니다.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def delete(self, request, article_id):  # 게시글 삭제
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response(
                {
                    "status": status.HTTP_204_NO_CONTENT,
                    "message": "게시글 삭제 성공!",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {
                    "status": status.HTTP_403_FORBIDDEN,
                    "message": "권한이 없습니다.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
