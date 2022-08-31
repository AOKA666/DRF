from django.urls import path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
from .views import MyTokenObtainPairView

urlpatterns = [
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 自定义token路由
    path('api/token/', MyTokenObtainPairView.as_view(), name='customer_token_obtain_pair'),
]