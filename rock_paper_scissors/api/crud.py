from collections import Counter
from sqlalchemy.orm import Session

from rock_paper_scissors.api import models, schemas


PLAYER_1 = ['Human', 'Machine_1']
PLAYER_2 = ['Machine', 'Machine_2']


def create_game(db: Session, game: schemas.GameCreate) -> dict:
    """Creates a new game in the database.

    Args:
        db (Session): Database session to interact with the database.
        game (schemas.GameCreate): Schema object containing information about the game being created.

    Returns:
        dict: Formatted response with game details.
    """
    db_game = models.Game(
        total_rounds=len(game.rounds_played),
        winner=game.game_winner
    )
    
    for round_info in game.rounds_played:
        db_move = models.Move(
            player_1_move=round_info.player_1_move,
            player_2_move=round_info.player_2_move,
            winner=round_info.winner,
            game=db_game
        )
        db_game.moves.append(db_move)

    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return format_game_response(db_game)


def format_game_response(db_game: models.Game) -> dict:
    """Formats the game data to match the expected schema for the response.

    Args:
        db_game (models.Game): The game instance retrieved from the database.

    Returns:
        dict: Formatted game response containing game id, rounds played, and game winner.
    """
    rounds_played = [
        {
            "player_1_move": move.player_1_move,
            "player_2_move": move.player_2_move,
            "winner": move.winner
        } for move in db_game.moves
    ]

    return {
        "id": db_game.id,
        "rounds_played": rounds_played,
        "game_winner": db_game.winner
    }


def get_global_info(db: Session) -> schemas.GlobalInfo:
    """Retrieves global information about the games played.

    Args:
        db (Session): Database session to interact with the database.

    Returns:
        schemas.GlobalInfo: An object containing total games, wins, losses, and win rate percentage.
    """
    total_games = db.query(models.Game).count()
    total_wins = db.query(models.Game).filter(models.Game.winner == 'Human').count()
    total_losses = db.query(models.Game).filter(models.Game.winner == 'Machine').count()

    winrate_percentage = (total_wins / total_games * 100) if total_games > 0 else 0

    return schemas.GlobalInfo(
        total_games=total_games,
        total_wins=total_wins,
        total_losses=total_losses,
        winrate_percentage=winrate_percentage
    )


def get_strong_hand(db: Session) -> schemas.StrongHandInfo:
    """Retrieves information about the hand that has resulted in the most victories for Human player.

    Args:
        db (Session): Database session to interact with the database.

    Returns:
        schemas.StrongHandInfo: An object containing the strongest hand and its win percentage.
    """
    player_wins = db.query(models.Game).filter(models.Game.winner == 'Human').all()

    moves_counter = get_moves_by_winner(player_wins, 'Human')

    strong_hand, win_percentage = get_hand_info(moves_counter)

    return schemas.StrongHandInfo(
        strong_hand=strong_hand,
        win_percentage=win_percentage
    )


def get_weak_hand(db: Session) -> schemas.WeakHandInfo:
    """Retrieves information about the hand that has resulted in the most losses for the human player.

    Args:
        db (Session): Database session to interact with the database.

    Returns:
        schemas.WeakHandInfo: An object containing the weakest hand and its loss percentage.
    """
    human_losses = db.query(models.Game).filter(models.Game.winner == 'Machine').all()

    moves_counter = get_moves_by_winner(human_losses, 'Machine')

    weak_hand, loss_percentage = get_hand_info(moves_counter)

    return schemas.WeakHandInfo(
        weak_hand=weak_hand,
        loss_percentage=loss_percentage
    )


def get_moves_by_winner(player_wins, player: str) -> Counter:
    """Counts the moves made by the player in the won games.

    Args:
        player_wins (list): List of game instances that the player has won.
        player (str): The player's name.

    Returns:
        Counter: A counter object with the count of moves made by the player in the won games.

    Examples:
        >>> from collections import namedtuple
        >>> Game = namedtuple('Game', ['moves'])
        >>> Move = namedtuple('Move', ['winner', 'player_1_move', 'player_2_move'])
        
        >>> game1 = Game(moves=[Move('Human', 'rock', 'scissors'), Move('Human', 'paper', 'rock')])
        >>> game2 = Game(moves=[Move('Machine', 'rock', 'scissors'), Move('Human', 'scissors', 'paper')])
        >>> player_wins = [game1, game2]
        
        >>> get_moves_by_winner(player_wins, 'Human')
        Counter({'rock': 1, 'paper': 1, 'scissors': 1})
    """
    moves_counter = Counter()

    for game in player_wins:
        for move in game.moves:
            if move.winner == player:
                if player in PLAYER_1:
                    moves_counter[move.player_1_move] += 1
                elif player in PLAYER_2:
                    moves_counter[move.player_1_move] += 1

    return moves_counter


def get_hand_info(moves_counter: Counter) -> tuple:
    """Retrieves information about the strongest or weakest hand for a player.

    Args:
        moves_counter (Counter): A counter object with the count of moves.

    Returns:
        tuple: The hand that has the most wins and its win percentage.

    Examples:
        >>> from collections import Counter
        >>> moves_counter = Counter({'rock': 5, 'paper': 3, 'scissors': 2})
        >>> get_hand_info(moves_counter)
        ('rock', 50.0)
    """
    if moves_counter:
        hand = moves_counter.most_common(1)[0][0]
        total_moves = sum(moves_counter.values())
        percentage = (moves_counter[hand] / total_moves * 100) if total_moves > 0 else 0
    else:
        hand = "No hand"
        percentage = 0

    return hand, percentage


def get_ranking(db: Session, limit: int = 3) -> list[schemas.PlayerInfo]:
    """Retrieves the ranking of the 3 best players based on the number of victories.

    Args:
        db (Session): Database session to interact with the database.
        limit (int): Maximum number of players to retrieve from the ranking.

    Returns:
        list: A list of PlayerInfo schemas containing player names and their victory counts.
    """
    victories = Counter()
    
    games = db.query(models.Game).all()
    
    for game in games:
        winner = game.winner
        victories[winner] += 1

    ranking = sorted(victories.items(), key=lambda item: item[1], reverse=True)[:limit]

    players = []
    for player, wins in ranking:
        players.append(schemas.PlayerInfo(name=player, points=wins))
    
    return players


def get_statistics(db: Session) -> dict:
    """Retrieves statistics about the games played, won, and those abandoned.

    Args:
        db (Session): Database session to interact with the database.

    Returns:
        dict: A dictionary containing total games, total wins, and total abandonments.
    """
    total_games = db.query(models.Game).count()
    total_wins = db.query(models.Game).filter(models.Game.winner == 'Human').count()
    total_abandonments = db.query(models.Game).filter(models.Game.winner == 'Machine', models.Game.total_rounds < 3).count()

    return {
        "total_games": total_games,
        "total_wins": total_wins,
        "total_abandonments": total_abandonments
    }
