from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),  

    # Include app URLs
    path("api/users/", include("users.urls")),
    path("api/restaurents/",include("restaurants.urls")), 
    path('silk/', include('silk.urls', namespace='silk')),


    # JWT Token Refresh (to get a new access token)
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
