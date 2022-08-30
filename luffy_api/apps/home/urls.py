from django.urls import path, re_path, include
from .views import BannerListAPIView


urlpatterns = [
    path('banners/', BannerListAPIView.as_view())
]
