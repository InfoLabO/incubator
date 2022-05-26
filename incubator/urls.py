from django.urls import include, path
from django.contrib import admin

import incubator.views
from incubator import settings
from django.conf.urls.static import static

import redir.views
import incubator.views
import space.views

urlpatterns = [
    path('', incubator.views.home, name='home'),
    path('spaceapi.json', space.views.spaceapi, name="spaceapi"),
    path('projects/', include('projects.urls')),
    path('accounts/', include('users.urls')),
    path('space/', include('space.urls')),
    path('wiki/', include('wiki.urls')),
    path('streams/', include('streams.urls')),
    path('materials/', include('materials.urls')),
    path('storage/', include('storage.urls')),
    path('admin/', admin.site.urls),
    path('auth/reset/done/', incubator.views.password_reset_done),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('incubator.apiurls')),
    path('notifications/', include('django_nyt.urls')),
    path('r/<slug:short_name>', redir.views.short_url, name='redirection'),
    path('ckeditor', include('ckeditor_uploader.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = incubator.views.error_view(400, "Impossible de traiter cette requête")
handler403 = incubator.views.error_view(403, "Tu n'as pas la permission de faire ça")
handler404 = incubator.views.error_view(404, "Impossible de trouver ça")
handler500 = incubator.views.error_view(500, "Une erreur serveur s'est produite")
