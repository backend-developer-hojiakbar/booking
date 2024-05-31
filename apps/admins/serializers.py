from rest_framework import serializers
from .models import *
from rest_framework.fields import SerializerMethodField


class NewsImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsImages
        fields = ('news_id', 'images')


class NewsSerializers(serializers.ModelSerializer):
    news_images = NewsImagesSerializers(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'name', 'description', 'news_images')






