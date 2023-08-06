from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# ------------------------회원가입 테스트------------------------
class SignupViewTest(APITestCase):
    def test_signup_success(self):  # 회원가입 성공 테스트
        url = reverse("users:signup")
        data = {"email": "test@test.com", "password": "12345678"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_fail(self):  # 회원가입 실패 테스트
        url = reverse("users:signup")
        data = {"email": "test", "password": "1234567"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["email"][0], "유효한 이메일 주소를 입력하십시오.")
        self.assertEqual(
            response.data["password"][0], "이 필드의 글자 수가  적어도 8 이상인지 확인하십시오."
        )
