from django.db import models
from users.models import User


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    title = models.CharField("제목", max_length=100)
    content = models.TextField("내용")
    image = models.ImageField("이미지", blank=True, null=True, upload_to="articles/%Y/%m/")
    created_at = models.DateTimeField("작성시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정시간", auto_now=True)

    def __str__(self):
        return self.title
