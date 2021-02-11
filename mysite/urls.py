from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from cabinet.views import UserViewSet, postData

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('data/', postData),
    path('admin/', admin.site.urls),
]
