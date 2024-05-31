from django.db import models
from core.models import BaseModel
from apps.users.models import User


# Create your models here.
class News(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class NewsImages(BaseModel):
    news_id = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news_images')
    images = models.ImageField(upload_to='news/images/')

    def __str__(self):
        return str(self.news_id)

