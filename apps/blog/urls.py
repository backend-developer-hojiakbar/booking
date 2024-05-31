from django.urls import path, include
from apps.blog import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('resort', views.ResortViewSet, 'resort')
router.register('search-resort', views.ResortSearchViewSet, 'search-resort')
router.register('police-search', views.TouristPoliceSearch, 'police-search')
router.register('amenties', views.AmenitiesViewSet, 'amenities')
router.register('dates', views.Availability_datesViewSet, 'dates')
router.register('images', views.ImagesViewSet, 'images')
router.register('location', views.LocationViewSet, 'location')
router.register('booking', views.BookingCreateAPIView, 'booking')
router.register('feedback', views.FeedbackViewSet, 'feedback')

urlpatterns = [
    path('', include(router.urls)),
    path('security/', views.ForSecurity.as_view(),),
    path('filter/', views.ResortFilterListView.as_view(),)
]