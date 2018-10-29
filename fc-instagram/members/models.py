from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models

from posts.models import PostLike


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

    @property
    def img_profile_url(self):
        if self.img_profile:
            return self.img_profile.url
        return static('img/blank_user.png')

    def like_post_toggle(self, post):
        # 자신에게 연결된 PostLike 중,
        # post값이 매개변수의 post인 PostLike가
        # 있다면 가져오고 없다면 생성
        postlike, postlike_created = self.postlike_set.get_or_create(post=post)

        if not postlike_created:
            postlike.delete()
