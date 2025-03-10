from django.contrib import admin

# Register your models here.
from .models import Restaurant
from .models import CuisineType
from .models import MenuItem


"""class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'opening_date')
    search_fields = ('name', 'location')"""

admin.site.register(Restaurant)
admin.site.register(CuisineType)
admin.site.register(MenuItem)