from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para la administración
    path('journals/', include('Journals.urls')),  # Ruta para la app Journals
    path('admin-app/', include('Admin.urls')),  # Ruta para la app Admin
    path('', include('Journals.urls')),  # Redirige la raíz a Journals
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)