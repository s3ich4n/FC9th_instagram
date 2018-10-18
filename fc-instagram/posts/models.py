# from django.contrib.auth.models import AbstractUser
from django.db import models

# https://github.com/matthewwithanm/django-imagekit


class Post(models.Model):
    author = models.ForeignKey(
        'members.User',
        on_delete=models.CASCADE,
    )

    photo = models.ImageField(upload_to='post')


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        'members.User',
        on_delete=models.CASCADE,
    )
    contents = models.TextField()
    # 해시태그: 여러개
    hashtags = models.ManyToManyField(
        'Hashtags',
    )
    # 멘션을 달면 나와 남이 바로연계됨.
    # mentions = models.ManyToManyField(
    #     'User',
    # )


class Hashtags(models.Model):
    tag_name = models.CharField(max_length=64)

    def __str__(self):
        return self.tag_name

