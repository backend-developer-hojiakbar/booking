from django.db import models
from core.models import BaseModel
from apps.users.models import User
from datetime import datetime, timedelta


class Location(BaseModel):
    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    def __str__(self):
        return self.district


RATINGS = (
    (0.5, 0.5),
    (1, 1),
    (1.5, 1.5),
    (2, 2),
    (2.5, 2.5),
    (3, 3),
    (3.5, 3.5),
    (4, 4),
    (4.5, 4.5),
    (5, 5)
)

PERCENTAGE = (
    (25, 25),
    (50, 50),
    (75, 75),
    (100, 100)
)
RESORT_STATUS = (
    (0,"New"),
    (1,"Active"),
    (2,"Canceled")
)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Resort(BaseModel):
    user = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=200)
    guests_number = models.PositiveIntegerField(default=0)
    bedrooms_number = models.PositiveIntegerField(default=0)
    baths_number = models.PositiveIntegerField(default=0)
    daily_price = models.IntegerField(default=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    mainImage = models.ImageField(upload_to='mainImage/')
    url = models.URLField(null=True, blank=True)
    longtitude = models.FloatField(max_length=255)
    latitude = models.FloatField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATINGS, default=5)
    kadastr = models.ImageField(upload_to='kadastr/', blank=True, null=True)
    passport = models.ImageField(upload_to='passport/', blank=True, null=True)
    resortDocument = models.ImageField(upload_to='document/', blank=True, null=True)
    resortStatus = models.IntegerField(choices=RESORT_STATUS, default=0)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Booking(BaseModel):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    pending_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guests_number = models.PositiveIntegerField()
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return str(self.guests_number)

    @property
    def calculate_total_sum(self):
        total_sum = 0
        duration = (self.to_date - self.from_date).days
        total_sum = duration * self.resort.daily_price
        print(total_sum)
        return total_sum


class ResortFeedback(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_feedbacks')
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name='resort_feedbacks')
    text = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField(choices=RATINGS, default=5)
    is_identified = models.BooleanField(default=False)

    def __str__(self):
        return f'{str(self.user.first_name)} {self.resort.name}'


class Images(BaseModel):
    img = models.ImageField(upload_to='img/', default='', null=True, blank=True)
    resort_id = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return str(self.resort_id)


class Availability_dates(BaseModel):
    resort_id = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name='availability_dates')
    date = models.DateField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.resort_id)


class Amenity(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Amenities(BaseModel):
    resort_id = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name='amenities')
    name = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return self.name


class BedroomImages(BaseModel):
    resort_id = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name='bedroomImages')
    img = models.ImageField(upload_to='bedroom/')

    def __str__(self):
        return str(self.resort_id)


class Information(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.TextField()
    ip = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.ip

    class Meta:
        ordering = ['-created']