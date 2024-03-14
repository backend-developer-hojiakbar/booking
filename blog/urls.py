from django.urls import path
from .views import BookingCreateAPIView, AllInfoDataView


urlpatterns = [
    path('book/create/', BookingCreateAPIView.as_view(),),
    path('all/info/', AllInfoDataView.as_view(),),
]