from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.models import User
from apps.blog.models import Booking, Resort
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum, F, ExpressionWrapper, fields
from rest_framework import viewsets, mixins, pagination, generics


class UserSalesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user_resorts = Resort.objects.filter(user__id=user_id)
        total_resorts_sold = 0
        total_earnings = 0

        for resort in user_resorts:
            completed_bookings = Booking.objects.filter(resort=resort, pending_status=Booking.PAYMENT_STATUS_COMPLETE)
            pending_bookings = Booking.objects.filter(resort=resort, pending_status=Booking.PAYMENT_STATUS_PENDING)
            failed_bookings = Booking.objects.filter(resort=resort, pending_status=Booking.PAYMENT_STATUS_PENDING)
            pending_resorts = pending_bookings.count()
            failed_resorts = failed_bookings.count()
            total_resorts_sold += completed_bookings.count()
            for booking in completed_bookings:
                total_earnings += booking.calculate_total_sum

        data = {
            'total_resorts_sold': total_resorts_sold,
            'total_earnings': total_earnings,
            'pending_resorts': pending_resorts,
            'failed_resorts': failed_resorts
        }
        return Response(data)