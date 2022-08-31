from django.urls import path, re_path, include
from .views import BannerListAPIView, NavListAPIView, FootListAPIView


urlpatterns = [
    path('banners/', BannerListAPIView.as_view()),
    path('nav/header/', NavListAPIView.as_view()),
    path('nav/footer/', FootListAPIView.as_view()),
]
