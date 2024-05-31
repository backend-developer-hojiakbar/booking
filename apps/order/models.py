from django.db import models
from django.conf import settings
from core.models import BaseModel
from apps.blog.models import Booking
from datetime import datetime, timedelta


class CustomOrderModel(models.Model):
    order = models.ForeignKey(Booking, models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return str(self.amount)

    @property
    def calculate_total_sum(self):
        total_sum = 0
        duration = (self.order.to_date - self.order.from_date).days
        total_sum = duration * self.order.resort.daily_price
        print(total_sum)
        return total_sum
        # orders = CustomOrderModel.objects.all()
        #
        # for order in orders:
        #     booking = order.self.order
        #     duration = (booking.end_date - booking.start_date).days
        #     total_amount = duration * booking.price
        #     total_sum += total_amount
        #
        # return total_sum
