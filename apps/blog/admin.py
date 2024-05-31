from django.contrib import admin
from .models import *


@admin.register(Resort)
class ResortAdmin(admin.ModelAdmin):
    list_filter = ['name']


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_filter = ['resort_id']


@admin.register(BedroomImages)
class BedroomImagesAdmin(admin.ModelAdmin):
    list_filter = ['resort_id']


@admin.register(Amenities)
class AmenitiesAdmin(admin.ModelAdmin):
    list_filter = ['resort_id']


@admin.register(Availability_dates)
class Availability_dates(admin.ModelAdmin):
    list_filter = ['resort_id']


@admin.register(Booking)
class Booking(admin.ModelAdmin):
    list_filter = ['pending_status']
    list_display = ['id']


@admin.register(Location)
class Location(admin.ModelAdmin):
    list_display = ['region', 'district']


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ResortFeedback)
class ResortFeedback(admin.ModelAdmin):
    list_display = ['rating', 'user']