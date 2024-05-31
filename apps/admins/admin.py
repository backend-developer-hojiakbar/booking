from django.contrib import admin
from .models import *


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_filter = ['name']


@admin.register(NewsImages)
class NewsImagesAdmin(admin.ModelAdmin):
    list_filter = ['news_id']