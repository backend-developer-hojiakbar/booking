from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.models import User
from apps.blog.models import Booking
from .models import *
from .serializers import NewsSerializers, NewsImagesSerializers
from rest_framework import status
from django.db.models import Sum, F, ExpressionWrapper, fields
from rest_framework import viewsets, mixins, pagination, generics


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializers


class NewsImagesViewSet(viewsets.ModelViewSet):
    queryset = NewsImages.objects.all()
    serializer_class = NewsImagesSerializers


class CountView(APIView):
    def get(self, request):
        total_user = User.objects.count()
        total_orders = Booking.objects.count()
        complete_bookings_count = Booking.objects.filter(pending_status=Booking.PAYMENT_STATUS_COMPLETE).count()
        bookings = Booking.objects.all()
        total_sum = bookings.aggregate(
            total_order=Sum(
                ExpressionWrapper(
                    (F('to_date') - F('from_date')) * F('resort__daily_price'),
                    output_field=fields.FloatField()
                )
            )
        )['total_order'] or 0
        return Response({'total_user': total_user,
                         'total_orders': total_orders,
                         'total_pending': complete_bookings_count,
                         'total_sum': total_sum}, status=status.HTTP_200_OK)