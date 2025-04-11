from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Journals.views import AboutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-app/', include('Admin.urls')),
    
    # About debe estar ANTES del patrón de slug
    path('about/', AboutView.as_view(), name='about'),
    
    # Journals URLs
    path('', include('Journals.urls')),  # Esto debe ir después de about/
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)