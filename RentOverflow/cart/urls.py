from django.urls import path 
from . import views 
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('favorites', views.cart_summary, name='favorites'),
]