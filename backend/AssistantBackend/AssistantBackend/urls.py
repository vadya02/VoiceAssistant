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
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    # path('upload_audio_file_mp3/', AudioUploadViewMp3.as_view(), name='upload_audio'),
    path('upload_audio_file_mp3/', AudioUploadViewMp3V2.as_view(), name='upload_audio'),
    path('get_history_of_requests/', RequestHistoryList.as_view(), name='history_of_requests'),
    path('upload_audio_text/', AudioUploadViewText.as_view(), name='history_of_requests'),
    path('get_user_data/', CurrentUserView.as_view(), name='get_user_data'),
]
