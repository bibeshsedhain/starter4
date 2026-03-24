from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=100)
    grid_size = models.IntegerField(default=4)
    grid = models.JSONField(blank=True, null=True)
    dictionary_ref = models.CharField(max_length=50, default="English")
    solution_set = models.JSONField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.grid_size}x{self.grid_size})"

class LeaderBoard(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='leaderboard')

    def __str__(self):
        return f"Leaderboard for {self.game.name}"

class LeaderBoardEntry(models.Model):
    leaderboard = models.ForeignKey(LeaderBoard, on_delete=models.CASCADE, related_name='entries')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    player_name = models.CharField(max_length=50, blank=True, help_text="Used if user is anonymous")
    words_found = models.JSONField(default=list)
    words_not_found = models.JSONField(default=list)
    time_elapsed = models.IntegerField(help_text="Time in seconds")
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name = self.user.username if self.user else self.player_name
        return f"{name} - {self.score} pts"