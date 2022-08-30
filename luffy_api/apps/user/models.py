from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telephone = models.CharField(verbose_name="手机号", max_length=11, unique=True)
    avatar = models.ImageField(verbose_name="头像", upload_to='avatar', default='avatar/default.png')

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"
        db_table = 'ly_users'