from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsRestaurantOwner
from .models import CuisineType, Restaurant, MenuItem
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CuisineTypeSerializer, RestaurantSerializer, MenuItemSerializer

class CuisineTypeListCreateAPIView(APIView):
    """
    API View to list and create Cuisine Types.
    - Any authenticated user can view cuisines.
    - Restaurant owners can add new cuisine types.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cuisines = CuisineType.objects.all()
        serializer = CuisineTypeSerializer(cuisines, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CuisineTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantListCreateAPIView(APIView):
    """
    API View for listing and creating restaurants.
    - Customers can only view restaurants.
    - Only restaurant owners can create restaurants.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Enable file upload


    def get(self, request):
        restaurants = Restaurant.objects.all().prefetch_related('cuisines')
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        if request.user.profile.role != "restaurant_owner":
            return Response({"error": "Only restaurant owners can create a restaurant."}, status=403)

        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantDetailAPIView(APIView):
    """
    API View for retrieving, updating, and deleting a restaurant.
    - Customers can only view restaurant details.
    - Only restaurant owners can update or delete their own restaurants.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Enable file upload


    def get(self, request, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            serializer = RestaurantSerializer(restaurant)
            return Response(serializer.data)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            if restaurant.owner != request.user:
                return Response({"error": "You can only update your own restaurant."}, status=status.HTTP_403_FORBIDDEN)
            serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            if restaurant.owner != request.user:
                return Response({"error": "You can only delete your own restaurant."}, status=status.HTTP_403_FORBIDDEN)
            restaurant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)


class MenuItemListCreateAPIView(APIView):
    """
    API View for listing and creating menu items.
    - Customers can only view menu items.
    - Only restaurant owners can add new menu items.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Enable file upload


    def get(self, request):
        cuisine_id = request.query_params.get("cuisine_id")
        menu_items = MenuItem.objects.all()
        if cuisine_id:
            menu_items = menu_items.filter(cuisine_id=cuisine_id)
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != "owner":
            return Response({"error": "Only restaurant owners can add menu items."}, 
                            status=status.HTTP_403_FORBIDDEN)
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuItemDetailAPIView(APIView):
    """
    API View for retrieving, updating, and deleting a menu item.
    - Customers can only view menu items.
    - Only restaurant owners can update or delete their own menu items.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Enable file upload


    def get(self, request, pk):
        try:
            menu_item = MenuItem.objects.get(pk=pk)
            serializer = MenuItemSerializer(menu_item)
            return Response(serializer.data)
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            menu_item = MenuItem.objects.get(pk=pk)
            if menu_item.restaurant.owner != request.user:
                return Response({"error": "You can only update your own menu items."}, status=status.HTTP_403_FORBIDDEN)
            serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            menu_item = MenuItem.objects.get(pk=pk)
            if menu_item.restaurant.owner != request.user:
                return Response({"error": "You can only delete your own menu items."}, status=status.HTTP_403_FORBIDDEN)
            menu_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item not found."}, status=status.HTTP_404_NOT_FOUND)
