from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from cabinet.views import UserViewSet, postData
from document.views import DocumentViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'docs', DocumentViewSet, basename='docs')

urlpatterns = [
    path('', include(router.urls)),
    path('data/', postData),
    path('admin/', admin.site.urls),
]
