from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from .models import Banner, Nav
from .serializers import BannerModelSerializer, NavModelSerializer
from luffy_api.settings import constants


class BannerListAPIView(ListAPIView): # 自动导包
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by("-orders", "-id")[:constants.BANNER_LENGTH]
    serializer_class = BannerModelSerializer


class NavListAPIView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True, is_deleted=False, position=1).order_by("id")[
               :constants.NAV_LENGTH]
    serializer_class = NavModelSerializer


class FootListAPIView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True, is_deleted=False, position=2).order_by("id")[
               :constants.FOOT_LENGTH]
    serializer_class = NavModelSerializer
