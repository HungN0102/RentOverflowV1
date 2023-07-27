from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('property/property-list/', views.property_list, name='property_list'),
    path('property/<int:pk>/', views.property_info, name='property_info'),

    path('property/favorite-listing/', views.favorite_listing, name='favorite_listing'),
    
    #path('property/property-list/<str:search>', views.property_list, name='property_list_search')
]