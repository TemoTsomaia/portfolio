from django.db import models

# Create your models here.
class Toy(models.Model):
    name = models.CharField(max_length=50)
    time_to_create = models.IntegerField()
    is_assigned = models.BooleanField(default=False)

class Coal(models.Model):
    name = models.CharField(default="Coal", editable=False, max_length=50)