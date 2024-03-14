from django.db import models
import accounts
# Create your models here.
class Resort(models.Model):
    name = models.CharField(max_length=200)
    guests_number = models.IntegerField()
    bedrooms_number = models.IntegerField()
    baths_number = models.IntegerField()
    daily_price = models.IntegerField()
    location = models.CharField(max_length=500)

    def __str__(self):
        return self.name
class Booking(models.Model):
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE)
    user = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE)
    guests_number = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return str(self.guests_number)
class Images(models.Model):
    img = models.ImageField(upload_to='img/')
    resort_id = models.ForeignKey(Resort, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.resort_id)

class Availability_dates(models.Model):
    resort_id = models.ForeignKey(Resort, on_delete=models.CASCADE)
    availability_dates = models.DateField()

    def __str__(self):
        return str(self.resort_id)

class Amenities(models.Model):
    resort_id = models.ForeignKey(Resort, on_delete=models.CASCADE)
    name = models.TextField()

    def __str__(self):
        return self.name