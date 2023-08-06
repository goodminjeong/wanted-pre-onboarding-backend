from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignupSerializer, SigninSerializer


class SignupView(APIView):
    @swagger_auto_schema(
        tags=["회원가입"],
        request_body=SignupSerializer,
        responses={201: "회원가입 성공", 400: "유효하지 않은 email 또는 password 입력"},
    )
    def post(self, request):  # 회원가입
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "message": "회원가입 완료!",
            },
            status=status.HTTP_201_CREATED,
        )


class SigninView(APIView):  # 로그인
    @swagger_auto_schema(
        tags=["로그인"],
        request_body=SigninSerializer,
        responses={200: "로그인 성공", 400: "유효하지 않은 email 또는 password 입력"},
    )
    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "data": serializer.validated_data,
                "status": status.HTTP_200_OK,
                "message": "로그인 성공!",
            },
            status=status.HTTP_200_OK,
        )
