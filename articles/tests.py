import tempfile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from PIL import Image
from .models import Article


# ---------------------------이미지 생성 함수---------------------------
def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, "png")
    return temp_file


# ---------------------------게시글 CRUD 테스트---------------------------
class AccompanyViewTest(APITestCase):
    # ----------------유저 데이터 생성----------------
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "password": "12345678"}
        cls.user = User.objects.create_user(**cls.user_data)
        cls.article_data = {"title": "test title", "content": "test content"}

    def setUp(self):
        super().setUp()
        self.access_token = self.client.post(
            reverse("users:signin"), self.user_data
        ).data["data"]["access"]
        self.article = Article.objects.create(**self.article_data, user=self.user)

    # ------------------------게시글 작성 테스트------------------------
    def test_create_article_success(self):  # 게시글 작성 성공 테스트
        response = self.client.post(
            path=reverse("articles:article"),
            data=self.article_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)
        self.assertEqual(
            Article.objects.get(id=self.article.id).content,
            self.article_data["content"],
        )

    def test_create_article_success_with_image(self):  # 이미지 있는 게시글 작성 성공 테스트
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)
        self.article_data["image"] = image_file
        response = self.client.post(
            path=reverse("articles:article"),
            data=self.article_data,
            format="multipart",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)
        self.assertEqual(bool(response.data["data"]["image"]), True)

    def test_create_article_failed_not_user(self):  # 게시글 작성 실패 테스트 - 비로그인
        response = self.client.post(
            path=reverse("articles:article"), data=self.article_data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Article.objects.count(), 1)

    def test_create_article_failed_empty_title(self):  # 게시글 작성 실패 테스트 - 빈 제목
        article_data = {"content": "test content"}
        response = self.client.post(
            path=reverse("articles:article"),
            data=article_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(response.data["title"][0], "이 필드는 필수 항목입니다.")

    def test_create_article_failed_empty_content(self):  # 게시글 작성 실패 테스트 - 빈 내용
        article_data = {"title": "test title"}
        response = self.client.post(
            path=reverse("articles:article"),
            data=article_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(response.data["content"][0], "이 필드는 필수 항목입니다.")
