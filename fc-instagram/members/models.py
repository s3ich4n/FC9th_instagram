from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='user',
        blank=True,
    )
    website = models.CharField(
        '웹사이트',
        max_length=128,
        blank=True,
    )
    bio_info = models.TextField(
        '소개',
        blank=True,
        max_length=64,
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'
