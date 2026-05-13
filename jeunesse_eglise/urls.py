from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('teachings/', include('teachings.urls')),
    path('blog/', include('blog.urls')),
    path('donations/', include('donations.urls')),
    path('gallery/', include('gallery.urls')),
    path('chat/', include('chat.urls')),
]

# ✅ Gestion des fichiers médias (images, vidéos, PDF)
if settings.DEBUG:
    # En développement
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # ✅ En production (Render) - Sert les fichiers médias
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
