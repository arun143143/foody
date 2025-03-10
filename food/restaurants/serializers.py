from rest_framework import serializers
from .models import CuisineType, Restaurant, MenuItem

class CuisineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuisineType
        fields = "__all__"

class RestaurantSerializer(serializers.ModelSerializer):
    cuisines = CuisineTypeSerializer(many=True, read_only=True)
    cuisine_ids = serializers.ListField(write_only=True, child=serializers.IntegerField(), required=False)


    class Meta:
        model = Restaurant
        fields = ["id", "name", "address", "phone_number", "restaurant_image", "cuisines", "cuisine_ids"]

        
    def create(self, validated_data):
        cuisine_ids = validated_data.pop("cuisine_ids", [])
        restaurant = Restaurant.objects.create(**validated_data)
        restaurant.cuisines.set(cuisine_ids)  #  Assign cuisines
        return restaurant

    def update(self, instance, validated_data):
        cuisine_ids = validated_data.pop('cuisine_ids', None)
        if cuisine_ids is not None:
            instance.cuisines.set(cuisine_ids)  # Update cuisines
        return super().update(instance, validated_data)

class MenuItemSerializer(serializers.ModelSerializer):
    cuisine = CuisineTypeSerializer(read_only=True)
    cuisine_id = serializers.PrimaryKeyRelatedField(
        queryset=CuisineType.objects.all(), write_only=True, source="cuisine"
    )

    class Meta:
        model = MenuItem
        fields = ["id", "name", "description", "price", "cuisine", "cuisine_id", "item_image", "restaurant"]
