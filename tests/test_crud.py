import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rock_paper_scissors.api.models import Base, Game, Move
from rock_paper_scissors.api.crud import create_game, get_global_info, get_strong_hand, get_weak_hand, get_hand_info, get_ranking, get_statistics
from rock_paper_scissors.api import schemas
from collections import Counter


# Crear una base de datos en memoria para los tests
@pytest.fixture(scope='function')
def db_session():
    engine = create_engine('sqlite:///:memory:')  # Base de datos en memoria
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_create_game(db_session):
    # Datos de entrada para simular la creación de un juego
    game_data = schemas.GameCreate(
        rounds_played=[
            schemas.Move(player_1_move='rock', player_2_move='scissors', winner='Human'),
            schemas.Move(player_1_move='paper', player_2_move='rock', winner='Human')
        ],
        game_winner='Human'
    )

    # Llamada a la función que se va a probar
    response = create_game(db_session, game_data)
    
    # Asegurarse de que los datos se guardaron en la base de datos
    db_game = db_session.query(Game).first()

    # Comprobaciones de que el juego se creó correctamente
    assert db_game is not None
    assert db_game.total_rounds == 2
    assert db_game.winner == 'Human'
    assert len(db_game.moves) == 2

    # Comprobación de la respuesta
    assert response['game_winner'] == 'Human'
    assert len(response['rounds_played']) == 2
    assert response['rounds_played'][0]['player_1_move'] == 'rock'
    assert response['rounds_played'][1]['player_2_move'] == 'rock'


def test_get_global_info(db_session):
    # Insertar datos de prueba
    game1 = Game(total_rounds=3, winner='Human')
    game2 = Game(total_rounds=3, winner='Machine')
    db_session.add_all([game1, game2])
    db_session.commit()

    # Llamada a la función que se va a probar
    global_info = get_global_info(db_session)

    # Comprobaciones de la información global
    assert global_info.total_games == 2
    assert global_info.total_wins == 1
    assert global_info.total_losses == 1
    assert global_info.winrate_percentage == 50


def test_get_strong_hand(db_session):
    # Insertar datos de prueba
    game1 = Game(total_rounds=3, winner='Human')
    move1 = Move(player_1_move='rock', player_2_move='scissors', winner='Human', game=game1)
    move2 = Move(player_1_move='paper', player_2_move='rock', winner='Human', game=game1)
    move3 = Move(player_1_move='paper', player_2_move='rock', winner='Human', game=game1)
    db_session.add_all([game1, move1, move2, move3])
    db_session.commit()

    # Llamada a la función que se va a probar
    strong_hand_info = get_strong_hand(db_session)

    # Comprobaciones de la mano más fuerte
    assert strong_hand_info.strong_hand == 'paper'
    assert strong_hand_info.win_percentage == 66.66666666666666


def test_get_weak_hand(db_session):
    # Insertar datos de prueba
    game1 = Game(total_rounds=3, winner='Machine')
    move1 = Move(player_1_move='scissors', player_2_move='rock', winner='Machine', game=game1)
    move2 = Move(player_1_move='rock', player_2_move='paper', winner='Machine', game=game1)
    move3 = Move(player_1_move='rock', player_2_move='paper', winner='Machine', game=game1)
    db_session.add_all([game1, move1, move2, move3])
    db_session.commit()

    # Llamada a la función que se va a probar
    weak_hand_info = get_weak_hand(db_session)

    # Comprobaciones de la mano más fuerte
    assert weak_hand_info.weak_hand == 'rock'
    assert weak_hand_info.loss_percentage == 66.66666666666666


def test_get_hand_info():
    # Caso 1: La mano más fuerte tiene la mayor cantidad de victorias
    moves_counter = Counter({'rock': 5, 'paper': 3, 'scissors': 2})
    hand, percentage = get_hand_info(moves_counter)
    assert hand == 'rock'
    assert percentage == 50.0


def test_get_ranking(db_session):
    # Simulación de juegos
    db_session.add_all([
        Game(winner='Player_1', total_rounds=3),
        Game(winner='Player_2', total_rounds=3),
        Game(winner='Player_1', total_rounds=3),
    ])
    db_session.commit()

    ranking = get_ranking(db_session, limit=3)
    
    # Comprobamos que el ranking está bien ordenado
    assert len(ranking) == 2  # Solo hay 2 jugadores
    assert ranking[0].name == 'Player_1'
    assert ranking[0].points == 2
    assert ranking[1].name == 'Player_2'
    assert ranking[1].points == 1


def test_get_statistics(db_session):
    # Simulación de juegos
    db_session.add_all([
        Game(winner='Human', total_rounds=3),
        Game(winner='Machine', total_rounds=2),
        Game(winner='Human', total_rounds=3),
        Game(winner='Machine', total_rounds=3),
    ])
    db_session.commit()

    stats = get_statistics(db_session)
    
    # Comprobaciones
    assert stats['total_games'] == 4
    assert stats['total_wins'] == 2
    assert stats['total_abandonments'] == 1