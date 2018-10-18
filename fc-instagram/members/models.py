from django.db import models


class User(models.Model):
    # profile_image = models
    username = models.CharField(max_length=32)
    img_profile = models.ImageField(
        upload_to='user',
        blank=True,
    )
    name = models.CharField(max_length=32, blank=True)
    website = models.CharField(max_length=64, blank=True)
    bio_info = models.TextField(max_length=64)
    # User = models.ManyToManyField(
    #     'self',
    #
    # )

    def __str__(self):
        return self.name
