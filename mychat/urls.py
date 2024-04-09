from django.contrib import admin
from django.urls import path, include
from mychatapp.urls import urlapp
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urlapp))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)