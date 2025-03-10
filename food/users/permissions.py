from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsAuthenticatedUser(permissions.BasePermission):
    """Ensures the user is authenticated before applying role-based permissions."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class IsCustomer(IsAuthenticatedUser):
    """Permission class for Customers."""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.profile.role == 'customer'

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS  # Customers can only view data

class IsRestaurantOwner(IsAuthenticatedUser):
    """Permission class for Restaurant Owners."""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.profile.role == 'restaurant_owner'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user  # Ensures owners can manage only their restaurant data

class IsDeliveryPerson(IsAuthenticatedUser):
    """Permission class for Delivery Personnel."""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.profile.role == 'delivery_person'
