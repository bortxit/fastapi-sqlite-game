from fastapi import  APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List

from rock_paper_scissors.api import crud, schemas
from rock_paper_scissors.api.api_client import get_db


router = APIRouter(prefix="/game",
                   tags=["game"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

"""
API Router for managing game-related operations.

This router provides endpoints for creating a game, retrieving game information,
and accessing various statistics related to the Rock Paper Scissors game.

Endpoints:
    POST /game/               - Create a new game
    GET /game/get_global_info - Get global game information
    GET /game/mano_fuerte     - Get strong hand information
    GET /game/mano_debil      - Get weak hand information
    GET /game/ranking         - Get ranking of players
    GET /game/estadisticas    - Get game statistics
"""

@router.post("/", response_model=schemas.Game)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    """Create a new game.

    Args:
        game (schemas.GameCreate): The game creation request data.
        db (Session): The database session dependency.

    Returns:
        schemas.Game: The created game object.
    """
    return crud.create_game(db=db, game=game)


@router.get("/get_global_info", response_model=schemas.GlobalInfo)
def get_global_info(db: Session = Depends(get_db)):
    """ Retrieve global game information.

    Args:
        db (Session): The database session dependency.

    Returns:
        schemas.GlobalInfo: An object containing global game information.
    """
    return crud.get_global_info(db=db)


@router.get("/mano_fuerte", response_model=schemas.StrongHandInfo)
def get_strong_hand(db: Session = Depends(get_db)):
    """Get information about the strong hand in the game.

    Args:
        db (Session): The database session dependency.

    Returns:
        schemas.StrongHandInfo: Information about the strong hand.
    """
    return crud.get_strong_hand(db=db)


@router.get("/mano_debil", response_model=schemas.WeakHandInfo)
def get_weak_hand_info(db: Session = Depends(get_db)):
    """Get information about the weak hand in the game.

    Args:
        db (Session): The database session dependency.

    Returns:
        schemas.WeakHandInfo: Information about the weak hand.
    """
    return crud.get_weak_hand(db)


@router.get("/ranking", response_model= List[schemas.PlayerInfo])
def get_ranking(db: Session = Depends(get_db)):
    """Retrieve the ranking of players.

    Args:
        db (Session): The database session dependency.

    Returns:
        List[schemas.PlayerInfo]: A list of players and their ranking information.
    """
    return crud.get_ranking(db=db)


@router.get("/estadisticas", response_model=schemas.Statistics)
def get_statistics(db: Session = Depends(get_db)):
    """Retrieve game statistics.

    Args:
        db (Session): The database session dependency.

    Returns:
        schemas.Statistics: An object containing game statistics.
    """
    return crud.get_statistics(db=db)