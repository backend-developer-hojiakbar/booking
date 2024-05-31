from django.urls import path, include
from rest_framework import routers
from apps.admins.views import CountView, NewsViewSet, NewsImagesViewSet

router = routers.DefaultRouter()
router.register('news', NewsViewSet, basename='news')
router.register('newsImages', NewsImagesViewSet, basename='newsImages')

urlpatterns = [
    path('', include(router.urls)),
    path('totalsCount/', CountView.as_view(), name='totalsCount'),
]