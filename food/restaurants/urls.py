from django.urls import path
from .views import (
    CuisineTypeListCreateAPIView, 
    RestaurantListCreateAPIView, 
    RestaurantDetailAPIView, 
    MenuItemListCreateAPIView, 
    MenuItemDetailAPIView
)

urlpatterns = [
    # Cuisine Type 
    path("cuisines/", CuisineTypeListCreateAPIView.as_view(), name="cuisine-list-create"),

    # Restaurant 
    path("restaurants/", RestaurantListCreateAPIView.as_view(), name="restaurant-list-create"),
    path("restaurants/<int:pk>/", RestaurantDetailAPIView.as_view(), name="restaurant-detail"),

    # Menu Item 
    path("menu-items/", MenuItemListCreateAPIView.as_view(), name="menuitem-list-create"),
    path("menu-items/<int:pk>/", MenuItemDetailAPIView.as_view(), name="menuitem-detail"),
]

