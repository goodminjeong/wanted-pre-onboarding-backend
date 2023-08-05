from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import SignupSerializer, SigninSerializer


class SignupView(APIView):
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
