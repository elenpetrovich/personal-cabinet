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
from synchronization.views import SyncCompanyViewSet, SyncCollectionViewSet, SyncUserViewSet, SyncRoleViewSet, SyncDocsViewSet, SyncDocsFileViewSet, SyncDocsRequestsViewSet


class TemaplteAPIView(routers.APIRootView):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        if request.query_params.get("format", "html") == "html":
            return redirect("start-list")
        else:
            return super().get(request=request, args=args, kwargs=kwargs)


class TempaleRouter(routers.DefaultRouter):
    APIRootView = TemaplteAPIView

    routes = [
        routers.Route(url=r'^{prefix}{trailing_slash}$',
                      mapping={
                          'get': 'list',
                          'post': 'create'
                      },
                      name='{basename}-list',
                      detail=False,
                      initkwargs={'suffix': 'List'}),
        routers.DynamicRoute(url=r'^{prefix}/{url_path}{trailing_slash}$',
                             name='{basename}-{url_name}',
                             detail=False,
                             initkwargs={}),
        routers.Route(url=r'^{prefix}/{lookup}{trailing_slash}$',
                      mapping={
                          'get': 'retrieve',
                      },
                      name='{basename}-detail',
                      detail=True,
                      initkwargs={'suffix': 'Instance'}),
        routers.Route(url=r'^{prefix}/{lookup}/update{trailing_slash}$',
                      mapping={
                          'get': 'page_update',
                          'post': 'partial_update',
                      },
                      name='{basename}-update',
                      detail=True,
                      initkwargs={'suffix': 'Instance'}),
        routers.Route(url=r'^{prefix}/{lookup}/delete{trailing_slash}$',
                      mapping={
                          'get': 'page_delete',
                          'post': 'destroy',
                      },
                      name='{basename}-delete',
                      detail=True,
                      initkwargs={'suffix': 'Instance'}),
        routers.DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}),
    ]


router = TempaleRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(
    r'company/(?P<company_pk>[^/.]+)/(?P<collection_pk>[^/.]+)/requests/(?P<document_pk>[^/.]+)',
    DocumentRequestViewSet,
    basename='requests',
)
router.register(
    r'company/(?P<company_pk>[^/.]+)/(?P<collection_pk>[^/.]+)/docs',
    DocumentViewSet,
    basename='docs',
)
router.register(r'company', CompanyViewSet, basename="company")
router.register(r'start', StartPageView, basename="start")
router.register(r'sync/company', SyncCompanyViewSet, basename="sync-company")
router.register(
    r'sync/collection',
    SyncCollectionViewSet,
    basename="sync-collection",
)
router.register(r'sync/user', SyncUserViewSet, basename="sync-user")
router.register(r'sync/role', SyncRoleViewSet, basename="sync-role")
router.register(r'sync/docs', SyncDocsViewSet, basename="sync-docs")
router.register(
    r'sync/docs/file',
    SyncDocsFileViewSet,
    basename="sync-docs-file",
)
router.register(
    r'sync/docs/requests',
    SyncDocsRequestsViewSet,
    basename="sync-docs-requests",
)

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
