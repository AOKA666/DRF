from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from .models import User


def get_user(username):
    user = User.objects.filter(Q(username=username) | Q(telephone=username)).first()
    return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user(username)
        if user is not None and user.check_password(password):
            return user

