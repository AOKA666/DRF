from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import MyTokenObtainPairView, GeetestAPIView, SendSMSAPIView


urlpatterns = [
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 自定义token路由
    path('api/token/', MyTokenObtainPairView.as_view(), name='customer_token_obtain_pair'),
    # 行为验证
    path('geetest/', GeetestAPIView.as_view()),
    # 发送短信验证码
    re_path(r'^send/sms/$', SendSMSAPIView.as_view()),
]