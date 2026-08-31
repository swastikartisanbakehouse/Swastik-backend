from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        "status": "online",
        "message": "Swastik Backend API is running successfully."
    })

urlpatterns = [
    # Health check & Root endpoint
    path('', health_check, name='root_health_check'),
    path('health/', health_check, name='health_check'),

    # Django Admin Panel
    path('admin-panel/', admin.site.urls),

    # API endpoints
    path('api/auth/', include('apps.accounts.urls')),
    path('api/', include('apps.categories.urls')),
    path('api/', include('apps.products.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

