from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


def get_user(username):
    user = User.objects.filter(Q(username=username) | Q(telephone=username)).first()
    return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user(username)
        if user is not None and user.check_password(password):
            return user


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['id'] = user.id
    refresh['username'] = user.username

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
