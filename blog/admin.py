from django.contrib import admin
from .models import Resort, Images, Amenities, Availability_dates
# Register your models here.

@admin.register(Resort)
class ResortAdmin(admin.ModelAdmin):
    list_filter = ['name']
@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_filter = ['resort_id']
@admin.register(Amenities)
class AmenitiesAdmin(admin.ModelAdmin):
    list_filter = ['resort_id']
@admin.register(Availability_dates)
class Availability_dates(admin.ModelAdmin):
    list_filter = ['resort_id']