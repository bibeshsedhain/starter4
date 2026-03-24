from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Game, LeaderBoard, LeaderBoardEntry
from .boggle_solver import Boggle

class BoggleSolverTests(APITestCase):
    def test_boggle_solver_finds_words(self):
        """Test that the core Boggle algorithm correctly finds words in a grid."""
        grid = [
            ["C", "A"],
            ["T", "S"]
        ]
        dictionary = ["CAT", "CATS", "BAT", "SAT"]
        
        boggle = Boggle(grid, dictionary)
        solutions = boggle.getSolution()
        
        # It should find CAT, CATS, and SAT, but not BAT.
        self.assertIn("CAT", solutions)
        self.assertIn("CATS", solutions)
        self.assertIn("SAT", solutions)
        self.assertNotIn("BAT", solutions)
        self.assertEqual(len(solutions), 3)

class GameAPITests(APITestCase):
    def setUp(self):
        self.games_url = '/api/games/'

    def test_create_game_generates_board_and_leaderboard(self):
        """Test that a POST to /api/games/ creates a game, a random grid, and a leaderboard."""
        payload = {
            "name": "My API Test Game",
            "grid_size": 4
        }
        
        response = self.client.post(self.games_url, payload, format='json')
        
        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that the game was actually saved to the database
        self.assertEqual(Game.objects.count(), 1)
        game = Game.objects.first()
        self.assertEqual(game.name, "My API Test Game")
        self.assertEqual(game.grid_size, 4)
        
        # Check that the grid was randomly generated (should be a list of lists)
        self.assertIsNotNone(game.grid)
        self.assertEqual(len(game.grid), 4)
        
        # Check that the LeaderBoard was automatically created and attached to this game
        self.assertEqual(LeaderBoard.objects.count(), 1)
        self.assertEqual(LeaderBoard.objects.first().game, game)

    def test_retrieve_games_list(self):
        """Test that a GET request fetches the list of games."""
        # Create a dummy game first
        Game.objects.create(name="Dummy Game", grid_size=3)
        
        response = self.client.get(self.games_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Dummy Game")


class UserAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testplayer', password='password123')
        
        self.game = Game.objects.create(
            name="Test Game", 
            grid_size=4, 
            grid=[["A","B","C","D"],["E","F","G","H"],["I","J","K","L"],["M","N","O","P"]],
            solution_set=["ABC", "DEF"]
        )
        self.leaderboard = LeaderBoard.objects.create(game=self.game)
        self.url = '/api/entries/'
        
        self.valid_payload = {
            "leaderboard": self.leaderboard.id,
            "player_name": "Anonymous Player",
            "words_found": ["ABC"],
            "words_not_found": ["DEF"],
            "time_elapsed": 45,
            "score": 100
        }

    def test_authenticated_user_can_post_score(self):
        """Test that a logged-in user can post a score and it links to their account."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        entry = LeaderBoardEntry.objects.first()
        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.user.username, 'testplayer')

    def test_unauthenticated_user_cannot_post_score(self):
        """Test that an anonymous user gets blocked from posting a score."""
        response = self.client.post(self.url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(LeaderBoardEntry.objects.count(), 0)