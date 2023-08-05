from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
