import operator
from django.db.models import Q
from .models import *
from .serializers import ResortSerializer, BookingSerializer, \
    AmenitiesSerializer, ImagesSerializer, \
    Availability_datesSerializer, LocationSerializer, ResortFeedbackSerializer
from rest_framework import viewsets, mixins, pagination, generics
from functools import reduce
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geopy.distance import geodesic
from rest_framework.decorators import action
from rest_framework import pagination
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ResortFilter


class ResortViewSet(viewsets.ModelViewSet):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    pagination_class = pagination.PageNumberPagination


class AmenitiesViewSet(viewsets.ModelViewSet):
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer


class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class Availability_datesViewSet(viewsets.ModelViewSet):
    queryset = Availability_dates.objects.all()
    serializer_class = Availability_datesSerializer


class BookingCreateAPIView(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.filter(user=user)


class ResortSearchViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer

    def get_queryset(self):
        text = self.request.query_params.get('q', None)
        if not text:
            return self.queryset
        text_seq = text.split(' ')
        text_qs = reduce(operator.and_,
                         (Q(name__icontains=x) for x in text_seq))
        return self.queryset.filter(text_qs)


class TouristPoliceSearch(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        text = self.request.query_params.get('q', None)
        if not text:
            return self.queryset
        text_seq = text.split(' ')
        text_qs = reduce(operator.and_,
                         (Q(user__first_name__icontains=x) |
                          Q(user__last_name__icontains=x) |
                          Q(resort__name__icontains=x) for x in text_seq))
        return self.queryset.filter(text_qs)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    @action(detail=True, methods=['get'])
    def get_resorts(self, request, pk=None, *args, **kwargs):
        location = self.get_object()
        resorts = Resort.objects.filter(location=location)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(resorts, request)
        serializer = ResortSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ForSecurity(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    @action(detail=False, methods=['get'])
    def get(self, request):
        data = Booking.objects.filter(pending_status='Complete')
        return Response(data)


class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = ResortFeedbackSerializer
    queryset = ResortFeedback.objects.all().order_by("-created_at")
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if self.request.user.is_active == True:
                return self.queryset
            else:
                return self.queryset.filter(is_identified=True)
        else:
            return self.queryset.filter(is_identified=True)


class ResortFilterListView(generics.ListAPIView):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ResortFilter






