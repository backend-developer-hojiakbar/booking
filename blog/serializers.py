from rest_framework import serializers
from .models import Resort, Booking, Amenities, Images, Availability_dates

class ResortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resort
        fields = ('id', 'name', 'guests_number', 'bedrooms_number', 'baths_number', 'daily_price', 'location')
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'resort', 'user', 'guests_number', 'from_date', 'to_date')

class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = ('resort_id', 'name')

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('resort_id', 'img')

class Availability_datesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability_dates
        fields = ('resort_id', 'availability_dates')

class AllInfoSerializer(serializers.Serializer):
    resort_data = ResortSerializer(many=True)
    amenities_data = AmenitiesSerializer(many=True)
    images_data = ImagesSerializer(many=True)
    availability_dates_data = Availability_datesSerializer(many=True)
