import random

from rock_paper_scissors.api.api_client import create_game

MOVES = ["rock", "paper", "scissors"]


def determine_round_winner(player_1_move: str, player_2_move: str, player_1: str, player_2: str) -> str:
    """Determine the winner of a game.
    
    Args
        player_1_move (str): Player 1 movement (rock, paper o scissors).
        player_2_move (str): Player 2 movement (rock, paper o scissors).
        player_1 (str): Player 1 name.
        player_2 (str): Player 2 name.
    
    Returns:
        str: Name of the player winner of the round.

    Examples:
    >>> determine_round_winner("rock", "scissors", "Player1", "Player2")
    'Player1'
    >>> determine_round_winner("rock", "paper", "Player1", "Player2")
    'Player2'
    """
    if player_1_move == player_2_move:
        return player_2
    elif (player_1_move == "rock" and player_2_move == "scissors") or \
         (player_1_move == "paper" and player_2_move == "rock") or \
         (player_1_move == "scissors" and player_2_move == "paper"):
        return player_1
    else:
        return player_2
    

def get_round_result(round_number: str, player_1_move: str, player_2_move: str, player_1: str, player_2: str) -> dict:
    """Simulates the result of a round

    Args:
        round_number (str): Number of round (1-3)
        player_1_move (str): Move of player 1 (rock, paper, scissors)
        player_2_move (str): Move of player 2 (rock, paper, scissors)
        player_1 (str): Name of player 1
        player_2 (str): Name of player 2

    Returns:
        dict: Dictionary with moves and winner of the round

    Examples:
        >>> get_round_result('1', 'rock', 'scissors', 'Alice', 'Bob')
        Round 1. Alice has selected rock and Bob has selected scissors. Alice wins
        {'player_1_move': 'rock', 'player_2_move': 'scissors', 'winner': 'Alice'}

        >>> get_round_result('2', 'scissors', 'scissors', 'Alice', 'Bob')
        Round 2. Alice has selected scissors and Bob has selected scissors. Bob wins
        {'player_1_move': 'scissors', 'player_2_move': 'scissors', 'winner': 'Bob'}
    """
    winner = determine_round_winner(player_1_move, player_2_move, player_1, player_2)
    
    print(f"Round {round_number}. {player_1} has selected {player_1_move} and {player_2} has selected {player_2_move}. {winner} wins")

    return {
        "player_1_move": player_1_move,
        "player_2_move": player_2_move,
        "winner": winner
    }


def play_rounds(player_1: str, player_2: str, special_game: bool = False) -> dict:
    """Simulates a game of three rounds. It is allowed to give up the game before finish when it is a basic game mode (special_game = False).

    Args:
        player_1 (str): Name of player 1.
        player_2 (str): Name of player 2.
        special_game (bool): If True, both players are under control of the machine. By default, False.

    Returns:
        dict: Dictionary that contains information about rounds played. It prepares information to be inserted into database .
    """
    rounds_played = []
    total_rounds = 3

    for round_number in range(1, total_rounds + 1):
        if not special_game:
            player_1_move = get_player_1_move(round_number)
        else:
            player_1_move = get_machine_move()
        player_2_move = get_machine_move()

        round_result = get_round_result(round_number, player_1_move, player_2_move, player_1, player_2)
        rounds_played.append(round_result)

        if not special_game and round_number < 3 and is_round_abandoned():
            break

    game_result = {
        "rounds_played": rounds_played
    }

    return game_result


def get_game_information(rounds_results: dict, player_1: str, player_2: str) -> dict:
    """
    Processes the information of the played rounds and determines the winner of the game, 
    as well as the total number of rounds.

    Args:
        rounds_information (dict): Result of the rounds
        player_1 (str): Name of player 1.
        player_2 (str): Name of player 2.

    Returns:
        dict: Prepare the information to be inserted into database for the game result: total rounds and game_winner.

    Examples:
    >>> rounds_results = {'rounds_played': [{'winner': 'Alice'}, {'winner': 'Bob'}, {'winner': 'Alice'}]}
    >>> get_game_information(rounds_results, 'Alice', 'Bob')
    Game finished. Alice wins.
    {'total_rounds': 3, 'game_winner': 'Alice'}
    """
    player_1_wins, player_2_wins = calculate_round_wins(rounds_results, player_1, player_2)
    total_rounds = len(rounds_results["rounds_played"])

    if player_1_wins > player_2_wins and total_rounds == 3:
        game_winner = player_1
    else:
        game_winner = player_2

    print(f"Game finished. {game_winner} wins.")

    return {
        "total_rounds": total_rounds,
        "game_winner": game_winner
    }


def calculate_round_wins(rounds_information: dict, player_1: str, player_2: str) -> tuple:
    """Calculates the number of rounds won by each player in the game.

    Args:
        rounds_information (dict): Dictionary containing information about rounds played.
        player_1 (str): Name of player 1.
        player_2 (str): Name of player 2.

    Returns:
        tuple: A tuple containing the number of wins for player 1 and player 2 respectively.
    
    Examples:
    >>> rounds_info = {"rounds_played": [{"winner": "Alice"}, {"winner": "Bob"}, {"winner": "Alice"}]}
    >>> calculate_round_wins(rounds_info, "Alice", "Bob")
    (2, 1)
    """
    player_1_wins = 0
    player_2_wins = 0

    for round_info in rounds_information["rounds_played"]:
        if round_info["winner"] == player_1:
            player_1_wins += 1
        elif round_info["winner"] == player_2:
            player_2_wins += 1

    return player_1_wins, player_2_wins


def get_player_1_move(round_number: int) -> str:
    """Prompts player 1 to choose a move and validates that the move is valid.

    Args:
        round_number (int): The current round number.

    Returns:
        str: The validated move chosen by player 1.
    """
    while True:
        player_1_move = input(f"Round {round_number}. Choose your move (rock, paper, scissors): ").lower().strip()
        if player_1_move in MOVES:
            return player_1_move
        print(f"Incorrect move: {player_1_move}. Try again.")


def get_machine_move() -> str:
    """Randomly selects and returns a move for machine from the available options.

    Returns:
        str: The move chosen by machine.
    """
    return random.choice(MOVES)


def is_round_abandoned() -> bool:
    """Prompt the player to decide if wants to abandon the round.

    Returns:
        bool: True if the player chooses to abandon the round, False otherwise.
    """
    while True:
        abandon = input("Do you want to give up the round? (yes/no): ").lower().strip()
        if abandon == "yes":
            return True
        elif abandon == "no":
            return False
        
        print(f"Move invalid: {abandon}. Try again.")


def play_game(special_game: bool = False):
    """This is the entry point to the logic of the game.

    Args:
        special_game (bool, optional): Indicates if the game is machine vs machine or a simple game between human and machine. Defaults to False.
    """
    if not special_game:
        player_1 = "Human"
        player_2 = "Machine"
    else:
        player_1 = "Machine_1"
        player_2 = "Machine_2"
    rounds_information = play_rounds(player_1, player_2, special_game)
    game_information = get_game_information(rounds_information, player_1, player_2)
    create_game(rounds_information, game_information)