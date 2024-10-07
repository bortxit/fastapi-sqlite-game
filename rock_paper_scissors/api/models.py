from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from rock_paper_scissors.api.database import Base


class Game(Base):
    """Represents a game in the Rock Paper Scissors application.

    Attributes:
        id (int): Unique identifier for the game.
        total_rounds (int): Total number of rounds in the game. Defaults to 3.
        winner (str): The name of the player who won the game.

    Relationships:
        moves (list[Move]): A list of moves associated with this game.
    """
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    total_rounds = Column(Integer, default=3)
    winner = Column(String)

    moves = relationship("Move", back_populates="game")


class Move(Base):
    """Represents a move made during a game.

    Attributes:
        id (int): Unique identifier for the move.
        game_id (int): Foreign key linking to the associated game.
        player_1_move (str): The move selected by player 1.
        player_2_move (str): The move selected by player 2.
        winner (str): The name of the player who won the round.

    Relationships:
        game (Game): The game associated with this move.
    """
    __tablename__ = 'moves'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    player_1_move = Column(String, nullable=False)
    player_2_move = Column(String, nullable=False)
    winner = Column(String)

    game = relationship("Game", back_populates="moves")