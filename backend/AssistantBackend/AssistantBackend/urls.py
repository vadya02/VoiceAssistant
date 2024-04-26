"""
URL configuration for AssistantBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from AssistantBackendApp.views import (
    AudioUploadViewMp3,
    AudioUploadViewMp3V2,
    AudioUploadViewText,
    CurrentUserView,
    RequestHistoryList,
)
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from drf_yasg import openapi  # new
from drf_yasg.views import get_schema_view  # new
from rest_framework import permissions

schema_view = get_schema_view(  # new
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    # url=f'{settings.APP_URL}/api/v3/',
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('auth/', include('djoser.urls.jwt')),
    # path('upload_audio_file_mp3/', AudioUploadViewMp3.as_view(), name='upload_audio'),
    path('upload_audio_file_mp3/', AudioUploadViewMp3V2.as_view(), name='upload_audio'),
    path('get_history_of_requests/', RequestHistoryList.as_view(), name='history_of_requests'),
    path('upload_text/', AudioUploadViewText.as_view(), name='text_request'),
    path('get_user_data/', CurrentUserView.as_view(), name='get_user_data'),
]
