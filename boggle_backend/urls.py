from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This routes any url starting with /api/ to your game_engine
    path('api/', include('game_engine.urls')), 
]