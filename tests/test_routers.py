from fastapi.testclient import TestClient
from unittest.mock import patch

from rock_paper_scissors.api.init_app import app

client = TestClient(app)


@patch('rock_paper_scissors.api.crud.create_game')
@patch('rock_paper_scissors.api.api_client.get_db')
def test_create_game(mock_get_db, mock_create_game):
    """Test for verifying the creation of a game through the API.

    This test simulates a POST request to the `/game` endpoint to create a new game,
    mocking the `get_db` and `create_game` functions to avoid real interactions
    with the database. The test checks that the data sent to the API is correct 
    and that the response is as expected.

    Parameters:
    - mock_get_db: Mock object simulating the database connection.
    - mock_create_game: Mock object simulating the function that creates a game in the database.
    """
    data = {
        "rounds_played": [
            {"player_1_move": "Rock", "player_2_move": "Scissors", "winner": "Human"},
            {"player_1_move": "Paper", "player_2_move": "Rock", "winner": "Human"}
        ],
        "game_winner": "Human"
    }
    
    mock_create_game.return_value = {
        "id": 1,
        "rounds_played": data["rounds_played"],
        "game_winner": "Human"
    }

    response = client.post("/game", json=data)

    assert response.status_code == 200

    json_response = response.json()
    assert json_response["game_winner"] == "Human"
    assert len(json_response["rounds_played"]) == 2

    mock_create_game.assert_called_once()


def test_get_global_info():
    """Test for retrieving global game information.

    This test sends a GET request to the `/game/get_global_info` endpoint and 
    verifies that the returned data includes key statistics like the total number 
    of games, wins, losses, and the win rate percentage.
    """
    response = client.get("/game/get_global_info")
    assert response.status_code == 200

    data = response.json()

    assert "total_games" in data
    assert "total_wins" in data
    assert "total_losses" in data
    assert "winrate_percentage" in data

    assert isinstance(data["total_games"], int)
    assert isinstance(data["total_wins"], int)
    assert isinstance(data["total_losses"], int)
    assert isinstance(data["winrate_percentage"], float)


def test_get_strong_hand():
    """Test for retrieving the player's strongest hand.

    This test sends a GET request to the `/game/mano_fuerte` endpoint and verifies
    that the returned data includes the strongest hand and the win percentage 
    associated with that hand.
    """
    response = client.get("/game/mano_fuerte")
    assert response.status_code == 200

    data = response.json()

    assert "strong_hand" in data
    assert "win_percentage" in data

    assert isinstance(data["strong_hand"], str)
    assert isinstance(data["win_percentage"], float)
    
    assert 0 <= data["win_percentage"] <= 100


def test_get_weak_hand_info():
    """Test for retrieving the player's weakest hand.

    This test sends a GET request to the `/game/mano_debil` endpoint and verifies
    that the returned data includes the weakest hand and the loss percentage 
    associated with that hand.
    """
    response = client.get("/game/mano_debil")
    assert response.status_code == 200

    data = response.json()

    assert "weak_hand" in data
    assert "loss_percentage" in data

    assert isinstance(data["weak_hand"], str)
    assert isinstance(data["loss_percentage"], float)

    assert 0 <= data["loss_percentage"] <= 100


def test_get_ranking():
    """Test for retrieving the player ranking.

    This test sends a GET request to the `/game/ranking` endpoint and verifies that 
    the response is a list of players, with a maximum of 3 entries. It also checks 
    that each entry includes the player's name and points.
    """
    response = client.get("/game/ranking")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) <= 3

    for entry in data:
        assert "name" in entry
        assert "points" in entry
        assert isinstance(entry["name"], str)
        assert isinstance(entry["points"], int)


def test_get_statistics():
    """Test for retrieving game statistics.

    This test sends a GET request to the `/game/estadisticas` endpoint and verifies
    that the response includes key statistics such as the total number of games,
    wins, and abandonments. It also ensures that the number of abandonments 
    does not exceed the total number of games.
    """
    response = client.get("/game/estadisticas")
    assert response.status_code == 200

    data = response.json()

    assert "total_games" in data
    assert "total_wins" in data
    assert "total_abandonments" in data

    assert isinstance(data["total_games"], int)
    assert isinstance(data["total_wins"], int)
    assert isinstance(data["total_abandonments"], int)
    
    assert data["total_abandonments"] <= data["total_games"]





