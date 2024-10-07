import logging
import sys

from rock_paper_scissors.game_logic import play_game
from rock_paper_scissors.user_menu import print_menu, handle_choice
from rock_paper_scissors.utils import setup_logging


def main():
    """
    Starter point of the programme. If commands line's arguments contain 'mvm' followed by number,
    there is a special game between machine and machine. After that, there is a interactive menu
    for the user to continue playing.
    """
    if len(sys.argv) == 3:
        try:
            if sys.argv[1] == "mvm":
                for game_number in range(1, int(sys.argv[2]) + 1):
                    print(f"----------- Game {game_number} -----------")
                    play_game(special_game=True)
            else:
                print(f"You have to introduce 'mvm' as first parameter of the script to play machine vs machine.")
        except ValueError:
            print("Second argument must be a number for the number of games to play.")
            logging.error(f"The second argument is not a int: {sys.argv[2]}. There is no posible to play machine against machine.")

    while True:
        print_menu()
        choice = input("Select an option: ")
        if not handle_choice(choice):
            break


if __name__ == "__main__":
    setup_logging()
    main()