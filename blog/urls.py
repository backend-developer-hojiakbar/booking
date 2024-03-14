from django.urls import path
from .views import BookingCreateAPIView, AllInfoDataView, \
    ResortViewSet


urlpatterns = [
    path('', ResortViewSet.as_view(),),
    path('book/create/', BookingCreateAPIView.as_view(),),
    path('all/info/', AllInfoDataView.as_view(),),
]