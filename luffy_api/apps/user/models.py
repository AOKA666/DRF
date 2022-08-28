from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telephone = models.CharField(verbose_name="手机号", max_length=11)
    icon = models.ImageField(verbose_name="头像", upload_to='icon', default='icon/default.png')

