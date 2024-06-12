from rest_framework import serializers
from .models import *
from rest_framework.fields import SerializerMethodField


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    resort_name = serializers.SerializerMethodField()
    total_sum = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ('id', 'resort', 'resort_name', 'user', 'pending_status', 'guests_number', 'from_date', 'to_date', 'total_sum', 'created_at', 'updated_at')

    def get_resort_name(self, obj):
        return obj.resort.name

    def get_total_sum(self, obj):
        total_sum = 0
        duration = (self.obj.to_date - self.obj.from_date).days
        total_sum = duration * self.obj.resort.daily_price
        print(total_sum)
        return obj.total_sum


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = ('resort_id', 'name', 'count')


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('resort_id', 'img')


class BedroomImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BedroomImages
        fields = ('resort_id', 'img')


class Availability_datesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability_dates
        fields = ('resort_id', 'date')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class ResortFeedbackSerializer(serializers.ModelSerializer):
    user = SerializerMethodField()

    class Meta:
        model = ResortFeedback
        fields = ["id", "user", "resort", "text", "rating", "is_identified", "created_at"]

        read_only_fields = ["created_at", "resort", "is_identified"]

    def get_user(self, obj):
        data = {}
        if obj.user:
            data["id"] = obj.user.id
            data["full_name"] = (
                    obj.user.first_name + " " + obj.user.last_name
            )
        return data


class ResortSerializer(serializers.ModelSerializer):
    user = SerializerMethodField()
    resort_feedbacks = ResortFeedbackSerializer(many=True, read_only=True)
    images = ImagesSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True
    )
    bedroomImages = BedroomImagesSerializer(many=True, read_only=True)
    bedroomUploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True
    )
    amenities = AmenitiesSerializer(many=True, read_only=True)
    amenities_list = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True
    )
    availability_dates = Availability_datesSerializer(many=True, read_only=True)
    availability_dates_list = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True
    )
    location_name = serializers.CharField(source='location.district', read_only=True)

    class Meta:
        model = Resort
        fields = ('id', "user", 'name', 'guests_number', 'bedrooms_number', 'baths_number', 'daily_price','location', 'location_name', 'mainImage', 'url', 'longtitude', 'latitude','images', 'uploaded_images', 'amenities', 'amenities_list', 'availability_dates', 'availability_dates_list', 'category', 'bedroomImages', 'bedroomUploaded_images', 'resort_feedbacks')

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        bedroomUploaded_images = validated_data.pop("bedroomUploaded_images")
        resort_id = Resort.objects.create(**validated_data)
        amenities_list = validated_data.pop("amenities_list")
        availability_dates_list = validated_data.pop("availability_dates_list")
        for availability_dates in availability_dates_list:
            newresort_date = Availability_dates.objects.create(resort_id=resort_id, availability_dates=availability_dates)
        for name in amenities_list:
            newresort_amenities = Amenities.objects.create(resort_id=resort_id, name=name)
        for img in uploaded_images:
            newresort_image = Images.objects.create(resort_id=resort_id, img=img)
        for bedroomImg in bedroomUploaded_images:
            newresort_image = BedroomImages.objects.create(resort_id=resort_id, img=bedroomImg)
        return resort_id

    def get_user(self, obj):
        data = {}
        if obj.user:
            data["id"] = obj.user.id
            data["full_name"] = (
                    obj.user.first_name + " " + obj.user.last_name
            )
        return data
