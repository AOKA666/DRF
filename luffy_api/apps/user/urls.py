from django.urls import path, re_path
from .views import MyAPIView


urlpatterns = [
    path('test/', MyAPIView.as_view())
]