from django.contrib import admin
from django.urls import path, re_path
from musics.views import home, add_new, detail_view
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
urlpatterns = [
    path('QdkosjdWE434Fdfkpfee/', admin.site.urls),
    path('', home),
    path('Share/', add_new, name="add_new"),
    path('<pk>/', detail_view, name="detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
        re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    ]
