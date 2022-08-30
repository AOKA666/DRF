from django.contrib import admin
from .models import Banner
from user.models import User

admin.site.register(Banner)
admin.site.register(User)
