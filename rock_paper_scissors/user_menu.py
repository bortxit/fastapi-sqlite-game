import logging

from rock_paper_scissors.api.api_client import get_global_info, get_strong_hand, get_weak_hand, get_ranking, get_statistics
from rock_paper_scissors.game_logic import play_game


def print_menu():
    """Print the interactive menu to the user"""
    print("\n--- Main Menu ---")
    print("1. Play against machine")
    print("2. General information about the game history")
    print("3. Strong Hand")
    print("4. Weak Hand")
    print("5. Ranking")
    print("6. Statistics")
    print("7. Exit")
        

def handle_choice(choice: str) -> bool:
    """Handles the choice selected by the user in the interactive menu

    Args:
        choice (str): option selected by user from menu

    Returns:
        bool: False if the user exit from game. True, the user continues playing.

    Example:
    >>> handle_choice("7")
    Thank you for playing! See you next time.
    False
    >>> handle_choice(7)
    Invalid option, please try again.
    True
    """
    if choice == "1":
        play_game(special_game=False)
    elif choice == "2":
        get_global_info()
    elif choice == "3":
        get_strong_hand()
    elif choice == "4":
        get_weak_hand()
    elif choice == "5":
        get_ranking()
    elif choice == "6":
        get_statistics()
    elif choice == "7":
        print("Thank you for playing! See you next time.")
        return False
    else:
        logging.warning(f"Invalid option selected by the user: {choice}")
        print("Invalid option, please try again.")
    return True