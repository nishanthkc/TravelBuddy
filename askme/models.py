from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Queries(models.Model):
    place = models.CharField(max_length=30)
    duration  = models.IntegerField(validators=[MinValueValidator(1, "Duration must be greater than 1 character")])

class Data(models.Model):
    gpt_place = models.CharField(max_length=30)
    gpt_duration  = models.IntegerField(validators=[MinValueValidator(1, "Duration must be greater than 1 character")])
    gpt_result = models.TextField(max_length=10000)

    def __str__(self):
        return self.gpt_place+"( "+str(self.gpt_duration)+" )"

class Food(models.Model):
    gpt_place = models.CharField(max_length=30)
    gpt_result = models.TextField(max_length=10000)

    def __str__(self):
        return self.gpt_place