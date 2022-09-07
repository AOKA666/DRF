from cProfile import label
from re import I
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import ValidationError
from django_redis import get_redis_connection

from .models import User
from .utils import get_user, get_tokens_for_user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user.id
        token['username'] = user.username

        return token


class RegisterSerializer(serializers.ModelSerializer):
    sms = serializers.CharField(label="验证码")
    token_str = serializers.CharField(max_length=1024, read_only=True, help_text="token认证字符串")
    class Meta:
        model = User
        fields = ['id','username','telephone', 'sms', 'token_str']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'username': {
                'read_only': True
            },
            'telephone': {
                'write_only': True
            },

        }
    
    def validate(self, attrs):
        input_telephone = attrs.get('telephone')
        exist = get_user(input_telephone)
        if exist:
            raise ValidationError("用户名已存在！")
        input_code = attrs.get("sms")
        conn = get_redis_connection("sms_code")
        real_code = conn.get(input_telephone)
        if not real_code:
            raise ValidationError("验证码已过期，请重新获取")
        if input_code != real_code.decode('utf-8'):
            conn.delete(input_telephone)
            raise ValidationError("验证码错误，请重新获取")
        return attrs

    def create(self, validated_data):
        validated_data.pop("sms")
        password = validated_data.get("telephone")[-6:]
        username = validated_data.get("telephone")
        user = User.objects.create(
            username=username,
            password=password,
            telephone=username
        )
        user.token_str = get_tokens_for_user(user)
        return user