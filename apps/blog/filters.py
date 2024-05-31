import django_filters
from .models import Resort


class ResortFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Resort
        fields = ['min_price', 'max_price', 'rating', 'guests_number', 'bedrooms_number', 'baths_number', 'amenities__name']