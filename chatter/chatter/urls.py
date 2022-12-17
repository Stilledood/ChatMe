"""chatter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include,re_path
from chat import urls  as chat_urls
from user import urls as user_urls
from django.conf.urls.static import static
from django.conf import settings
from videochat import urls as videochat_urls

admin.site.site_header = 'Chatter'
admin.site.site_title = 'Chatter Site'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(chat_urls)),
    path('user/',include(user_urls, namespace='dj-auth')),
    path('',include(videochat_urls)),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
