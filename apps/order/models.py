from django.db import models
from django.conf import settings
from core.models import BaseModel


class CustomOrderModel(models.Model):
    amount = models.PositiveIntegerField()