from pydantic import BaseModel
from typing import List, Optional


# Schema definition for a movement
class Move(BaseModel):
    player_1_move: str
    player_2_move: str
    winner: str

    class Config:
        from_attributes = True


# Schema definition to create a game
class GameCreate(BaseModel):
    rounds_played: List[Move]
    game_winner: str


# Schema definition to get information of a game
class Game(GameCreate):
    id: int

    class Config:
        from_attributes = True


# Schema definition for global information
class GlobalInfo(BaseModel):
    total_games: int
    total_wins: int
    total_losses: int
    winrate_percentage: float

    class Config:
        from_attributes = True

# Schema definition for strong hand
class StrongHandInfo(BaseModel):
    strong_hand: str
    win_percentage: float

    class Config:
        from_attributes = True


# Schema definition to get the weakest hand and the percentage
class WeakHandInfo(BaseModel):
    weak_hand: str
    loss_percentage: float

    class Config:
        from_attributes = True


# Schema definition to get player information for the ranking
class PlayerInfo(BaseModel):
    name: str
    points: int

    class Config:
        from_attributes = True


# Schema definition to get the statistics
class Statistics(BaseModel):
    total_games: int
    total_wins: int
    total_abandonments: int

    class Config:
        from_attributes = True