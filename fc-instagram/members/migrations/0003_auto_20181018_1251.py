# Generated by Django 2.1.2 on 2018-10-18 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20181018_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='img_profile',
            field=models.ImageField(blank=True, upload_to='media', verbose_name='프로필 이미지'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=32, verbose_name='아이디'),
        ),
    ]
