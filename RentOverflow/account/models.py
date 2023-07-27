from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from store.models import Property

class UserFavorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(Property)

    class Meta:
        verbose_name_plural = 'User Favorites'
    
    def __str__(self):
        return f"{self.user.username}'s Favorites"