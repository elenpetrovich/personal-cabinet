from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from rest_framework import routers
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.shortcuts import redirect

from cabinet.views import UserViewSet, postData, StartPageView
from document.views import DocumentViewSet, FileRender, DocumentRequestViewSet
from company.views import CompanyViewSet
from synchronization.views import SyncViewSet


class TemaplteAPIView(routers.APIRootView):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        if request.query_params.get("format", "html") == "html":
            return redirect("start-list")
        else:
            return super().get(request=request, args=args, kwargs=kwargs)


class TempaleRouter(routers.DefaultRouter):
    APIRootView = TemaplteAPIView


router = TempaleRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(
    r'company/(?P<company_pk>[^/.]+)/(?P<collection_pk>[^/.]+)/requests/(?P<document_pk>[^/.]+)',
    DocumentRequestViewSet,
    basename='requests')
router.register(
    r'company/(?P<company_pk>[^/.]+)/(?P<collection_pk>[^/.]+)/docs',
    DocumentViewSet,
    basename='docs')
router.register(r'company', CompanyViewSet, basename="company")
router.register(r'sync', SyncViewSet, basename="sync")
router.register(r'start', StartPageView, basename="start")

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
] + [
    re_path(r"^media/files/(?P<document_pk>[^/.]+)/(?P<file_name>.*)",
            FileRender.serve_document_folder,
            name='files',
            kwargs={"document_root": settings.MEDIA_ROOT}),
]
# + static(settings.MEDIA_URL,
#            FileRender.serve_with_permissions,
#            document_root=settings.MEDIA_ROOT)
