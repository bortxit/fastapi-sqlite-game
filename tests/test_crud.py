import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rock_paper_scissors.api.models import Base, Game, Move
from rock_paper_scissors.api.crud import create_game, get_global_info, get_strong_hand, get_weak_hand, get_hand_info, get_ranking, get_statistics
from rock_paper_scissors.api import schemas
from collections import Counter
import time


@pytest.fixture(scope='function')
def db_session():
    """Create a new SQLAlchemy database session for testing.

    This fixture sets up an in-memory SQLite database for the duration 
    of a test function. It creates the necessary tables, yields a 
    session for interacting with the database, and ensures proper 
    cleanup by closing the session and dropping the tables after the 
    test completes.

    Yields:
        Session: A SQLAlchemy session object to interact with the 
        in-memory database.
    """
    engine = create_engine('sqlite:///:memory:')
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_create_game(db_session):
    """Test the creation of a game.

    This test simulates the creation of a game by providing input data 
    that includes moves played by two players and the declared winner.

    Args:
        db_session (Session): A SQLAlchemy session object provided by 
        the db_session fixture.
    """
    game_data = schemas.GameCreate(
        rounds_played=[
            schemas.Move(player_1_move='rock', player_2_move='scissors', winner='Human'),
            schemas.Move(player_1_move='paper', player_2_move='rock', winner='Human')
        ],
        game_winner='Human'
    )

    response = create_game(db_session, game_data)
    
    db_game = db_session.query(Game).first()

    assert db_game is not None
    assert db_game.total_rounds == 2
    assert db_game.winner == 'Human'
    assert len(db_game.moves) == 2

    assert response['game_winner'] == 'Human'
    assert len(response['rounds_played']) == 2
    assert response['rounds_played'][0]['player_1_move'] == 'rock'
    assert response['rounds_played'][1]['player_2_move'] == 'rock'


def test_get_global_info(db_session):
    """Test the retrieval of global game statistics.

    This test inserts sample game data into the database to simulate 
    a scenario where both a human and a machine have played games. 
    It verifies that the global statistics, such as the total number 
    of games played, total wins, total losses, and win rate percentage, 
    are calculated and returned correctly.

    Args:
        db_session (Session): A SQLAlchemy session object provided by 
        the db_session fixture, used to interact with the in-memory 
        database during the test.
    """
    game1 = Game(total_rounds=3, winner='Human')
    game2 = Game(total_rounds=3, winner='Machine')
    db_session.add_all([game1, game2])
    db_session.commit()

    global_info = get_global_info(db_session)

    assert global_info.total_games == 2
    assert global_info.total_wins == 1
    assert global_info.total_losses == 1
    assert global_info.winrate_percentage == 50


def test_get_strong_hand(db_session):
    """Test the calculation of the strongest hand in the game.

    This test inserts sample game data into the database to simulate 
    a scenario where a player has consistently won with specific moves. 
    It verifies that the function correctly identifies the strongest 
    hand (the move that has won the most) and calculates its win 
    percentage based on the moves played.

    Args:
        db_session (Session): A SQLAlchemy session object provided by 
        the db_session fixture, used to interact with the in-memory 
        database during the test.
    """
    game1 = Game(total_rounds=3, winner='Human')
    move1 = Move(player_1_move='rock', player_2_move='scissors', winner='Human', game=game1)
    move2 = Move(player_1_move='paper', player_2_move='rock', winner='Human', game=game1)
    move3 = Move(player_1_move='paper', player_2_move='rock', winner='Human', game=game1)
    db_session.add_all([game1, move1, move2, move3])
    db_session.commit()

    strong_hand_info = get_strong_hand(db_session)

    assert strong_hand_info.strong_hand == 'paper'
    assert strong_hand_info.win_percentage == 66.66666666666666


def test_get_weak_hand(db_session):
    """Test the calculation of the weakest hand in the game.

    This test inserts sample game data into the database to simulate 
    a scenario where a player has consistently lost with specific moves. 
    It verifies that the function correctly identifies the weakest 
    hand (the move that has lost the most) and calculates its loss 
    percentage based on the moves played.

    Args:
        db_session (Session): A SQLAlchemy session object provided by 
        the db_session fixture, used to interact with the in-memory 
        database during the test.
    """
    game1 = Game(total_rounds=3, winner='Machine')
    move1 = Move(player_1_move='scissors', player_2_move='rock', winner='Machine', game=game1)
    move2 = Move(player_1_move='rock', player_2_move='paper', winner='Machine', game=game1)
    move3 = Move(player_1_move='rock', player_2_move='paper', winner='Machine', game=game1)
    db_session.add_all([game1, move1, move2, move3])
    db_session.commit()

    weak_hand_info = get_weak_hand(db_session)

    assert weak_hand_info.weak_hand == 'rock'
    assert weak_hand_info.loss_percentage == 66.66666666666666


def test_get_hand_info():
    """Test the identification of the strongest/weakest hand based on win counts.

    This test simulates a scenario with a predefined count of moves 
    to determine which hand (move) has the most victories. It verifies 
    that the function correctly identifies the strongest hand and 
    calculates the corresponding win percentage.

    Moves data is provided using a Counter, where the keys are the 
    hand types and the values are the counts of victories for each.
    """
    moves_counter = Counter({'rock': 5, 'paper': 3, 'scissors': 2})
    hand, percentage = get_hand_info(moves_counter)
    assert hand == 'rock'
    assert percentage == 50.0


def test_get_ranking(db_session):
    """Test the ranking of players based on game results.

    This test simulates a series of games between players and inserts 
    the results into the database. It verifies that the ranking 
    function correctly calculates and returns the players' rankings 
    based on their wins.

    Args:
        db_session (Session): A SQLAlchemy session object provided by 
        the db_session fixture, used to interact with the in-memory 
        database during the test.
    """
    db_session.add_all([
        Game(winner='Player_1', total_rounds=3),
        Game(winner='Player_2', total_rounds=3),
        Game(winner='Player_1', total_rounds=3),
    ])
    db_session.commit()

    ranking = get_ranking(db_session, limit=3)
    
    assert len(ranking) == 2
    assert ranking[0].name == 'Player_1'
    assert ranking[0].points == 2
    assert ranking[1].name == 'Player_2'
    assert ranking[1].points == 1


def test_get_statistics(db_session):
    """Test the calculation of game statistics.

    This test simulates multiple games between a human player and a machine, 
    recording the results in the database. It verifies that the statistics 
    function accurately calculates and returns the overall game statistics, 
    including the total number of games played, total wins, and total 
    abandonments.

    Args:
        db_session (Session): A SQLAlchemy session object provided by 
        the db_session fixture, used to interact with the in-memory 
        database during the test.
    """
    db_session.add_all([
        Game(winner='Human', total_rounds=3),
        Game(winner='Machine', total_rounds=2),
        Game(winner='Human', total_rounds=3),
        Game(winner='Machine', total_rounds=3),
    ])
    db_session.commit()

    stats = get_statistics(db_session)
    
    assert stats['total_games'] == 4
    assert stats['total_wins'] == 2
    assert stats['total_abandonments'] == 1