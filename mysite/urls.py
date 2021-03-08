from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from rest_framework import routers
from cabinet.views import UserViewSet, postData, CompanyViewSet
from document.views import DocumentViewSet, SyncViewSet
from django.contrib.auth.views import LoginView, LogoutView


class TemaplteAPIView(routers.APIRootView):
    template_name = 'base.html'


class TempaleRouter(routers.DefaultRouter):
    APIRootView = TemaplteAPIView


router = TempaleRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'docs', DocumentViewSet, basename='docs')
router.register(r'company', CompanyViewSet, basename="company")
router.register(r'sync', SyncViewSet, basename="sync")

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('data/', postData),
    path('login/', LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    re_path(r'^favicon\.ico$',
            RedirectView.as_view(url='static/favicon.ico', permanent=True)),
]
