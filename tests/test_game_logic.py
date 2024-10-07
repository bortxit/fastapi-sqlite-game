from unittest.mock import patch
from rock_paper_scissors.game_logic import determine_round_winner, get_round_result, play_rounds, get_game_information, calculate_round_wins, get_machine_move, is_round_abandoned


def test_determine_round_winner():
    """Test the determine_round_winner function.

    This function tests the winner determination logic based on the moves 
    of two players. It verifies that the correct winner is returned for 
    various scenarios of rock-paper-scissors.
    """
    assert determine_round_winner("rock", "scissors", "Player 1", "Player 2") == "Player 1"
    assert determine_round_winner("paper", "rock", "Player 1", "Player 2") == "Player 1"
    assert determine_round_winner("scissors", "paper", "Player 1", "Player 2") == "Player 1"
    assert determine_round_winner("rock", "rock", "Player 1", "Player 2") == "Player 2"
    assert determine_round_winner("rock", "paper", "Player 1", "Player 2") == "Player 2"


def test_get_round_result():
    """Test the get_round_result function.

    This function tests the result of a single round in the game, verifying 
    that the moves and winner are correctly recorded. It checks both 
    scenarios where Player 1 wins and where there is a tie.
    """
    result = get_round_result(1, "rock", "scissors", "Player_1", "Player_2")
    assert result == {
        "player_1_move": "rock",
        "player_2_move": "scissors",
        "winner": "Player_1"
    }

    result = get_round_result(2, "scissors", "scissors", "Player_1", "Player_2")
    assert result["winner"] == "Player_2"
    assert result["player_1_move"] == "scissors"
    assert result["player_2_move"] == "scissors"


@patch('rock_paper_scissors.game_logic.get_player_1_move', return_value='rock')
@patch('rock_paper_scissors.game_logic.get_machine_move', return_value='scissors')
@patch('rock_paper_scissors.game_logic.is_round_abandoned', return_value=False)
def test_play_rounds(mock_p1_move, mock_machine_move, mock_abandon):
    """Test the play_rounds function.

    This function simulates a complete game of three rounds between two players,
    mocking the input moves for both players. It verifies that the expected 
    number of rounds are played and checks if the winner of the first round 
    is correctly identified.
    """
    result = play_rounds("Player_1", "Player_2")
    assert len(result["rounds_played"]) == 3
    assert result["rounds_played"][0]["winner"] == "Player_1"


def test_get_game_information():
    """Test the get_game_information function.

    This function tests the processing of round results to determine the 
    overall game winner and the total number of rounds played. It verifies 
    that the correct winner is returned based on the provided round results.
    """
    rounds_results = {'rounds_played': [{'winner': 'Player_1'}, {'winner': 'Player_2'}, {'winner': 'Player_1'}]}
    game_info = get_game_information(rounds_results, 'Player_1', 'Player_2')
    assert game_info["total_rounds"] == 3
    assert game_info["game_winner"] == 'Player_1'


def test_calculate_round_wins():
    """Test the calculate_round_wins function.

    This function tests the calculation of the total rounds won by each player 
    throughout the game. It verifies that the function correctly counts wins 
    based on the provided round results.
    """
    rounds_info = {"rounds_played": [{"winner": "Player_1"}, {"winner": "Player_2"}, {"winner": "Player_1"}]}
    player_1_wins, player_2_wins = calculate_round_wins(rounds_info, "Player_1", "Player_2")
    assert player_1_wins == 2
    assert player_2_wins == 1


def test_get_machine_move():
    """Test the get_machine_move function.

    This function tests the machine's ability to randomly select a move. 
    It ensures that the chosen move is one of the valid options.
    """
    move = get_machine_move()
    assert move in ["rock", "paper", "scissors"]


@patch('builtins.input', return_value='yes')
def test_is_round_abandoned_yes(mock_input):
    """Test the is_round_abandoned function when user chooses to abandon.

    This function tests the scenario where the player indicates they want to 
    abandon the round. It verifies that the function returns True in this case.
    """
    assert is_round_abandoned() == True

@patch('builtins.input', return_value='no')
def test_is_round_abandoned_no(mock_input):
    """Test the is_round_abandoned function when user chooses not to abandon.

    This function tests the scenario where the player indicates they do not 
    want to abandon the round. It verifies that the function returns False in this case.
    """
    assert is_round_abandoned() == False