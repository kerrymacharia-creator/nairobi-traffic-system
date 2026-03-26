"""
URL configuration for nairobi_traffic project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # The Django Admin interface
    path('admin/', admin.site.urls),
    
    # Includes all URLs from your 'traffic' app
    path('', include('traffic.urls')),
]

# Serving static and media files during development (DEBUG = True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)