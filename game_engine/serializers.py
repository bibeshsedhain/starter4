from rest_framework import serializers
from .models import Game, LeaderBoard, LeaderBoardEntry

class LeaderBoardEntrySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = LeaderBoardEntry
        fields = '__all__'
        read_only_fields = ['user']

class LeaderBoardSerializer(serializers.ModelSerializer):
    entries = LeaderBoardEntrySerializer(many=True, read_only=True)

    class Meta:
        model = LeaderBoard
        fields = ['id', 'game', 'entries']

class GameSerializer(serializers.ModelSerializer):
    leaderboard = LeaderBoardSerializer(read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'name', 'grid_size', 'grid', 'dictionary_ref', 'solution_set', 'date_created', 'leaderboard']
        read_only_fields = ['grid', 'solution_set', 'date_created']