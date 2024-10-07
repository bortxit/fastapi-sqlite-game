from .database import SessionLocal
import logging
import os
import requests

api_url = os.getenv("API_URL")

# Dependency
def get_db():
    """Dependency that provides a database session.

    This function uses `SessionLocal()` to create a new database session. 
    It ensures that the session is properly closed after use.

    Yields:
        SessionLocal: A new database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_game(rounds_information: dict, game_information:dict):
    """Sends a request to create a new game in the database.

    Args:
        rounds_information (dict): Information about the rounds played in the game.
        game_information (dict): Information about the game, including the winner.

    Raises:
        requests.exceptions.RequestException: If there's an error during the request.
    """
    API_URL = f"{api_url}/game/"
    data_to_send = {
        "rounds_played": rounds_information["rounds_played"],
        "game_winner": game_information["game_winner"]
    }

    try:
        response = requests.post(API_URL, json=data_to_send)
        response.raise_for_status()
        logging.info(f"New game created:\n{response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error saving the game: {e}")


def get_global_info():
    """Fetches and prints global game information from the API.

    Raises:
        requests.exceptions.RequestException: If there's an error during the request.
    """
    API_URL = f"{api_url}/game/get_global_info"
    try:
        response = requests.get(API_URL)
        print(response.text)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error displaying global information: {e}.")


def get_strong_hand():
    """Fetches and prints information about the strong hand from the API.

    Raises:
        requests.exceptions.RequestException: If there's an error during the request.
    """
    API_URL = f"{api_url}/game/mano_fuerte"
    try:
        response = requests.get(API_URL)
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error displaying data of strong hand: {e}")


def get_weak_hand():
    """Fetches and prints information about the weak hand from the API.

    Raises:
        requests.exceptions.RequestException: If there's an error during the request.
    """
    API_URL = f"{api_url}/game/mano_debil"
    try:
        response = requests.get(API_URL)
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error displaying data of weak hand: {e}")


def get_ranking():
    """Fetches and prints information about the ranking from the API.

    Raises:
        requests.exceptions.RequestException: If there's an error during the request.
    """
    API_URL = f"{api_url}/game/ranking"
    try:
        response = requests.get(API_URL)
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error displaying the ranking: {e}")


def get_statistics():
    """Fetches and prints information about the statistics from the API.

    Raises:
        requests.exceptions.RequestException: If there's an error during the request.
    """
    API_URL = f"{api_url}/game/estadisticas"
    try:
        response = requests.get(API_URL)
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error displaying the statistics: {e}")




