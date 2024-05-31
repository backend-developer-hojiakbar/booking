from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.users.managers import UserTypeManager
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import BaseModel
RATINGS = (
    (0, 0),
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
    (0, 0),
    (25, 25),
    (50, 50),
    (75, 75),
    (100, 100)
)
ROLE_CHOICES = (
        ('placer', 'Placer'),
        ('booker', 'Booker'),
)


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    rating = models.PositiveIntegerField(choices=RATINGS, default=5, blank=True, null=True)
    rapidlyReply = models.PositiveIntegerField(choices=PERCENTAGE, default=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='users/', blank=True, null=True, default="/media/default_img/user.jpg/")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='booker')
    username = None

    objects = UserTypeManager()
    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if not self.password:
            self.set_unusable_password()
        super().save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }


class Languages(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return str(self.name)


class PhoneToken(models.Model):
    phone_number = models.CharField(max_length=20)
    token = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Sms token"
        verbose_name_plural = "Sms Tokens"

    def __str__(self):
        return "{} - {}".format(self.phone_number, self.token)

    @property
    def is_expired(self):
        return self.expires_at < timezone.now()
