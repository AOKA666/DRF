from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import MyTokenObtainPairView, GeetestAPIView, SendSMSAPIView, RegisterAPIView


urlpatterns = [
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 自定义token路由
    path('api/token/', MyTokenObtainPairView.as_view(), name='customer_token_obtain_pair'),
    # 行为验证
    path('geetest/', GeetestAPIView.as_view()),
    # 发送短信验证码
    path('send/sms/', SendSMSAPIView.as_view()),
    # 注册
    path('register/', RegisterAPIView.as_view())
]