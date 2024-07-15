from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter
from src.cloud.views import FileViewSet, ShareFiles

router = SimpleRouter()
router.register(r'files', FileViewSet, basename='file')


urlpatterns = [
    path('admin/', admin.site.urls),    
    path('api/v1/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')), 
    path('api/v1/', include(router.urls)), 
    path('share/<slug:uuid>', ShareFiles.as_view(), name='share')
]
