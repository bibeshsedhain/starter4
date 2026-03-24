from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Game, LeaderBoard, LeaderBoardEntry
from .serializers import GameSerializer, LeaderBoardSerializer, LeaderBoardEntrySerializer
from .boggle_solver import Boggle, generate_random_grid

# Dummy dictionary
DEFAULT_DICTIONARY = ["API", "APP", "BAT", "BOGGLE", "CAT", "DJANGO", "DOG", "EGG", "PYTHON", "REACT", "WEB"]

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get('name', 'New Boggle Game')
        grid_size = int(request.data.get('grid_size', 4))

        grid = generate_random_grid(grid_size)

        boggle = Boggle(grid, DEFAULT_DICTIONARY)
        solution_set = boggle.getSolution()

        game = Game.objects.create(
            name=name,
            grid_size=grid_size,
            grid=grid,
            solution_set=solution_set
        )

        LeaderBoard.objects.create(game=game)

        serializer = self.get_serializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LeaderBoardViewSet(viewsets.ModelViewSet):
    queryset = LeaderBoard.objects.all()
    serializer_class = LeaderBoardSerializer

class LeaderBoardEntryViewSet(viewsets.ModelViewSet):
    queryset = LeaderBoardEntry.objects.all()
    serializer_class = LeaderBoardEntrySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()