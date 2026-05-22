from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .health import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("rest_framework.urls")),
    path("api/", include("apps.courses.urls")),
    path("api/", include("apps.news.urls")),
    path("api/", include("apps.applications.urls")),
    path("api/", include("apps.faq.urls")),
    path("api/", include("apps.about.urls")),
    path("api/health/", health_check, name="health-check"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
