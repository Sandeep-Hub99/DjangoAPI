from django.db import models

# Create your models here.
class Article(models.Model):
    title       = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Passenger(models.Model):
    """
    Stores passenger info
    """
    name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    mobile = models.IntegerField(unique=True)