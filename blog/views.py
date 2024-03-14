import operator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Resort, Booking, Amenities, Images, Availability_dates
from .serializers import ResortSerializer, BookingSerializer, AllInfoSerializer, \
    AmenitiesSerializer, ImagesSerializer, Availability_datesSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins, generics
from functools import reduce
from rest_framework.views import APIView

class ResortViewSet(viewsets.ModelViewSet):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer

class AllInfoDataView(APIView):
    def get(self, request, *args, **kwargs):
        resort_data = Resort.objects.all()
        amenity_data = Amenities.objects.all()
        images_data = Images.objects.all()
        availability_dates_data = Availability_dates.objects.all()
        serialized_resort_data = ResortSerializer(resort_data, many=True).data
        serialized_amenity_data = AmenitiesSerializer(amenity_data, many=True).data
        serialized_images_data = ImagesSerializer(images_data, many=True).data
        serialized_availability_dates_data = Availability_datesSerializer(availability_dates_data, many=True).data

        all_info = {
            'resort': serialized_resort_data,
            'amenity': serialized_amenity_data,
            'images': serialized_images_data,
            'availability_dates': serialized_availability_dates_data,
        }
        all_info_serializer = AllInfoSerializer(all_info)
        # return Response(all_info_serializer.data)
        return Response(all_info)


class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ResortSearchViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    def get_queryset(self):
        text = self.request.query_params.get('query', None)
        if not text:
            return self.queryset
        text_seq = text.split(' ')
        text_qs = reduce(operator.and_,
                         (Q(name__icontains=x) for x in text_seq))
        return self.queryset.filter(text_qs)