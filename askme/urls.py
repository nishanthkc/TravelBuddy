from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = "askme"

urlpatterns = [
    # path('', views.ModelFormHome.as_view(), name="askme_mform"),
    # path('chat/', views.Chat.as_view(), name="askme_chat"),
    # path('recommend-food/', views.FoodRecommender.as_view(), name="askme_foodform"),
    # path('reiterate/', views.AskAgain.as_view(), name="askme_again"),
    # path('food/', views.FoodView.as_view(), name="askme_food"),
    # path('trending/', views.MostSearched.as_view(), name="most_searched"),
    # path('places/<str:place_name>/', views.PlaceView.as_view(), name="place_view"),
    # path('places/<str:place_name>/<int:d>', views.PlaceDayView.as_view(), name="place_day_view"),
    # path('my-itineraries/', views.ItinerariesView.as_view(), name="itineraries"),
    # path('my-itineraries/<int:i_id>', views.SingleItineraryView.as_view(), name="single_itinerary"),
    # path('flights/', views.flights, name="flights"),
    # path('hotel/<str:place>/', views.hotel, name="hotel"),
    
    # path('health/', views.Health.as_view(), name="health"), #for health time out
    # path('privacy/', views.Privacy.as_view(), name="privacy"), #for privacy policies

    path('testing/', views.Test.as_view(), name='testing'),
    path('test_ajax/', views.testing, name='test_ajax'),
    path('chatbot/', views.chatbot, name='chatbot'),


    path('', views.Home.as_view(), name="home"),
    path('send', views.requestItinerary, name="requestItinerary"),
    path('hotel/<str:place>/', views.hotel, name="hotel"),
    path('itinerary/<str:place_name>/<str:iti_id>', views.GetItinerary.as_view(), name="getItinerary"),
    
    path('personalised', views.PersonalHome.as_view(), name="personal_home"),
    path('personal-send', views.requestPersonalItinerary, name="requestPersonalItinerary"),
    path('pcreate/itinerary/<str:iti_id>', views.createPID, name="createPID"),
    path('personalised/<str:piti_id>', views.GetPersonalItinerary.as_view(), name="getPersonalItinerary"),
    path('goto_personal_itinerary_section/<str:piti_id>', views.goto_personal_itinerary_section, name="goto_personal_itinerary_section"),

    path('interact/<str:place>/<int:duration>/<str:iti_id>', views.interact, name="interact"),

    path('my-itineraries/', views.ItinerariesView.as_view(), name="itineraries"),

    path('foodRecommeder/', views.FoodRecommender.as_view(), name="food"),
    path('sendFood', views.requestFood, name="requestFood"),
    path('foodItinerary/<str:place>', views.GetFoodfromItinerary.as_view(), name="getFoodfromItinerary"),
    path('food/<str:place_name>/<str:food_id>', views.GetFood.as_view(), name="getFood"),

    path('personalisedFoodRecommender', views.PersonalFoodRecommender.as_view(), name="personal_food"),
    path('personal-food-send', views.requestPersonalfood, name="requestPersonalFood"),
    path('pcreate/food/<str:food_id>', views.createPFoodID, name="createPFoodID"),
    path('personalisedFood/<str:p_food_id>', views.GetPersonalFood.as_view(), name="getPersonalFood"),
    path('goto_personal_food_section/<str:p_food_id>', views.goto_personal_food_section, name="goto_personal_food_section"),

    path('food-interact/<str:place>/<str:p_food_id>', views.food_interact, name="food_interact"),

    path('my-recommendations/', views.FoodRecommendationsView.as_view(), name="foodRecommendations"),
]