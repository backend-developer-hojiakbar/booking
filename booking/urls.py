from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers, urlpatterns
from blog import views

router = routers.DefaultRouter()
router.register('search',
                views.ResortSearchViewSet,
                basename='search-resort')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('blog.urls')),
    path('', include(router.urls)),
    path('accounts/', include('accounts.urls')),
]
app_name = 'blog'
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
