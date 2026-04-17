from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    photo = models.URLField()
    birth_date = models.DateField()
    is_married = models.BooleanField()