from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


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


# ------------------------로그인 테스트------------------------
class SigninViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="12345678")
        self.user.save()

    def test_signin_success(self):  # 로그인 성공 테스트
        url = reverse("users:signin")
        signin_data = {"email": "test@test.com", "password": "12345678"}
        response = self.client.post(url, signin_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signin_failed_email(self):  # 로그인 실패 테스트 - 이메일
        url = reverse("users:signin")
        signin_data = {"email": "test1@test.com", "password": "12345678"}
        response = self.client.post(url, signin_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"][0], "존재하지 않는 이메일입니다.")

    def test_signin_failed_password(self):  # 로그인 실패 테스트 - 비밀번호
        url = reverse("users:signin")
        signin_data = {"email": "test@test.com", "password": "1234567"}
        response = self.client.post(url, signin_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"][0], "비밀번호를 다시 확인해 주십시오.")
