from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Queries(models.Model):
    place = models.CharField(max_length=30)
    duration  = models.IntegerField(validators=[MinValueValidator(1, "Duration must be greater than 1 day"), MaxValueValidator(10, "Duration must be less than 10 days")])
    # personalize = models.CharField(max_length=100)

class Data(models.Model):
    itinerary_id = models.CharField(max_length=30, editable=False, unique=True)
    gpt_place = models.CharField(max_length=30)
    gpt_duration  = models.IntegerField(validators=[MinValueValidator(1, "Duration must be greater than 1 day")])
    gpt_result = models.TextField(max_length=100000)

    def __str__(self):
        return self.gpt_place+"( "+str(self.gpt_duration)+" )"+" ( "+str(self.itinerary_id)+" )"

class PersonalisedData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    p_itinerary_id = models.CharField(max_length=30, editable=False, unique=True)
    p_gpt_place = models.CharField(max_length=30)
    p_gpt_duration  = models.IntegerField(validators=[MinValueValidator(1, "Duration must be greater than 1 day")])
    p_gpt_result = models.TextField(max_length=100000)

    def __str__(self):
        return "Pesonalised "+self.p_gpt_place+"( "+str(self.p_gpt_duration)+" )"+" ( "+str(self.p_itinerary_id)+" )"

class Food(models.Model):
    food_id = models.CharField(max_length=30, editable=False, unique=True)
    food_place = models.CharField(max_length=30)
    food_result = models.TextField(max_length=10000)

    def __str__(self):
        return self.food_place+"( "+str(self.food_id)+" )"
class PersonalisedFoodData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    p_food_id = models.CharField(max_length=30, editable=False, unique=True)
    p_food_place = models.CharField(max_length=30)
    p_food_result = models.TextField(max_length=100000)

    def __str__(self):
        return self.p_food_place+"( "+str(self.p_food_id)+" )"
# class Statistics(models.Model):
#     stat_place = models.CharField(max_length=30)
#     stat_duration  = models.IntegerField(validators=[MinValueValidator(1, "Duration must be greater than 1 character")])
#     stat_count = models.IntegerField(validators=[MinValueValidator(1, "Duration must be greater than 1 character")])

#     def __str__(self):
#         return self.stat_place+"( "+str(self.stat_duration)+"-"+str(self.stat_count)+" )"

# class Search_history(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     search_place =models.CharField(max_length=30)
#     search_duration  = models.IntegerField()
#     search_query = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.email} searched for '{self.search_duration}-days'"