from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = "askme"

urlpatterns = [
    # path('', views.Home.as_view(), name="askme_home"),
    # path('forms/', views.FormHome.as_view(), name="askme_form"),
    path('mforms/', views.ModelFormHome.as_view(), name="askme_mform"),
    path('lol/', views.AskAgain.as_view(), name="askme_again"),
    path('food/', views.FoodView.as_view(), name="askme_food"),
]
