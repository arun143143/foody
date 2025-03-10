from django.db import models
from django.contrib.auth.models import User

class CuisineType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurants")
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    cuisines = models.ManyToManyField(CuisineType, related_name="restaurants")
    restaurant_image = models.ImageField(upload_to="restaurant_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.cuisines} - {self.created_at}"

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cuisine = models.ForeignKey(CuisineType, on_delete=models.CASCADE, related_name="menu_items")
    item_image = models.ImageField(upload_to="menu_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} -{self.description} -{self.price} -{self.cuisine} - {self.restaurant.name}"
