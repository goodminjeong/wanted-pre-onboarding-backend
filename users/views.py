from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import SignupSerializer


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
