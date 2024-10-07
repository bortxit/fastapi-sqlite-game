import pytest
from unittest.mock import patch
from rock_paper_scissors.api.api_client import create_game, get_global_info, get_strong_hand, get_weak_hand, get_ranking, get_statistics

@pytest.fixture(scope='function')
def mock_requests_post():
    """
    Fixture to mock the 'requests.post' function for use in tests that involve POST requests.
    """
    with patch('requests.post') as mock_post:
        yield mock_post

@pytest.fixture(scope='function')
def mock_requests_get():
    """
    Fixture to mock the 'requests.get' function for use in tests that involve GET requests.
    """
    with patch('requests.get') as mock_get:
        yield mock_get

def test_create_game(mock_requests_post):
    """Test the 'create_game' function.

    This test mocks the API call to create a game and verifies that the function
    correctly sends the data and makes a single POST request to the API. The 
    response should contain the rounds played and the game winner.
    """
    # Mock data to create the game
    rounds_info = {
        "rounds_played": [
            {"player_1_move": "Rock", "player_2_move": "Scissors", "winner": "Human"},
            {"player_1_move": "Paper", "player_2_move": "Rock", "winner": "Human"}
        ]
    }
    game_info = {
        "game_winner": "Human"
    }
    
    # Simulates the response of the API
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {
        "id": 1,
        "rounds_played": rounds_info["rounds_played"],
        "game_winner": "Human"
    }
    
    # Execution of the function
    create_game(rounds_info, game_info)

    # Make sure that the API call was made.
    mock_requests_post.assert_called_once()


def test_get_global_info(mock_requests_get):
    """Test the 'get_global_info' function.

    This test verifies that the function correctly makes a GET request to 
    fetch the global game statistics (total games, wins, and losses). 
    The API call should be made exactly once with the correct endpoint.
    """
    # Simulates the response of the API
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.text = '{"total_games": 10, "total_wins": 5, "total_losses": 5}'
    
    # Execution of the function
    get_global_info()

    # Make sure that the API call was made.
    mock_requests_get.assert_called_once_with("http://localhost:8000/game/get_global_info")


def test_get_strong_hand(mock_requests_get):
    """Test the 'get_strong_hand' function.

    This test checks that the function sends a GET request to retrieve 
    information about the player's strongest hand (the hand that has the highest win percentage).
    The API call should return the hand and the win percentage.
    """
    # Simulates the response of the API
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.text = '{"strong_hand": "Rock", "win_percentage": 75}'
    
    # Execution of the function
    get_strong_hand()

    # Make sure that the API call was made.
    mock_requests_get.assert_called_once_with("http://localhost:8000/game/mano_fuerte")


def test_get_weak_hand(mock_requests_get):
    """Test the 'get_weak_hand' function.

    This test verifies that the function makes a GET request to the API to fetch 
    information about the player's weakest hand (the hand with the highest loss percentage).
    The API call should be made exactly once, and the response should contain
    the weak hand and the loss percentage.
    """
    # Simulates the response of the API
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.text = '{"weak_hand": "Scissors", "loss_percentage": 60}'
    
    # Execution of the function
    get_weak_hand()

    # Make sure that the API call was made.
    mock_requests_get.assert_called_once_with("http://localhost:8000/game/mano_debil")


def test_get_ranking(mock_requests_get):
    """Test the 'get_ranking' function.

    This test verifies that the function makes a GET request to fetch the player 
    rankings from the API. It checks that the response is in JSON format, 
    contains a list of players, and each player has a name and points.
    """
    # Simulates the response of the API
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.text = '[{"player": "Alice", "points": 10}, {"player": "Bob", "points": 8}]'
    
    # Execution of the function
    get_ranking()

    # Make sure that the API call was made.
    mock_requests_get.assert_called_once_with("http://localhost:8000/game/ranking")


def test_get_statistics(mock_requests_get):
    """Test the 'get_statistics' function.

    This test ensures that the function makes a GET request to retrieve overall 
    game statistics (total games, wins, losses, abandonments). It checks that 
    the API call is made to the correct endpoint and that the response contains 
    the correct data.
    """
    # Simulates the response of the API
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.text = '{"total_games": 10, "total_wins": 5, "total_losses": 5, "total_abandonments": 2}'
    
    # Execution of the function
    get_statistics()

    # Make sure that the API call was made.
    mock_requests_get.assert_called_once_with("http://localhost:8000/game/estadisticas")
