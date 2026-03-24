from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, LeaderBoardViewSet, LeaderBoardEntryViewSet

# A router automatically creates all the standard RESTful routes (GET, POST, PUT, DELETE)
router = DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'leaderboards', LeaderBoardViewSet)
router.register(r'entries', LeaderBoardEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]