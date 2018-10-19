# from django.contrib.auth.models import AbstractUser
import datetime

from django.db import models

# https://github.com/matthewwithanm/django-imagekit


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        'members.User',
        on_delete=models.CASCADE,
    )

    photo = models.ImageField(
        '사진',
        upload_to='post',
    )

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('-pk',)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='포스트',
    )
    author = models.ForeignKey(
        'members.User',
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )
    contents = models.TextField()
    # 해시태그: 여러개
    hashtags = models.ManyToManyField(
        'Hashtags',
        blank=True,
        verbose_name='해시태그 목록',
    )

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = f'{verbose_name} 목록'
    # 멘션을 달면 나와 남이 바로연계됨.
    # mentions = models.ManyToManyField(
    #     'User',
    # )


class Hashtags(models.Model):
    tag_name = models.CharField(max_length=64)

    def __str__(self):
        return self.tag_name

