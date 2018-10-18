from django.db import models


class User(models.Model):
    # profile_image = models
    username = models.CharField(
        max_length=32,
    )
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='user',
        blank=True,
    )
    name = models.CharField(
        '이름',
        max_length=32,
        blank=True,
    )
    website = models.CharField(
        '웹사이트',
        max_length=64,
        blank=True,
    )
    bio_info = models.TextField(
        '소개',
        blank=True,
        max_length=64,
    )
    # User = models.ManyToManyField(
    #     'self',
    #
    # )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'
