import random
import gspread
import sys
from tabulate import tabulate
from boardclass import Board
from google.oauth2.service_account import Credentials

sys.path.append("boardclass.py")

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("Battleship-stats")
stats = SHEET.worksheet("stats")


def player_turn():
    """
    Prompts the player to insert the coordinates they want to attack.
    Checks for the coordinates correct length and returns an error message
    if the lenght is shorter or longer than intended. Checks if a value error
    is raised and returns a message if so.
    In both cases the user will be asked to insert the coordinates again.
    If the coordinates are correct, this function checks if
    those coordinates are in the computer_coordinates list, which contains
    five randomly generated coordinates. If yes, it puts an x on the computer
    board and removes the coordinates from computer_coordinates.
    Otherwise, it puts an o on the computer board.
    """
    flag = True
    while flag:
        coordinates = input(
            "Which coordinates do you want to shoot? The coordinates should\n"
            "be the column letter and the row number, separated by a space "
            "(like this: A 1):\n"
        )
        if len(coordinates) > 3:
            print(
                "\n***Attention! Your input is too long. It should only "
                "contain a letter, a space and a number.***\n"
            )
            continue
        elif len(coordinates) < 3:
            print(
                "\n***Attention! Your input is too short. It should only "
                "contain a letter, a space and a number.***\n"
            )
            continue
        else:
            try:
                a, b = coordinates.split()
                a_num = computer_board.column_number(a)
                if (
                    computer_board.board[int(b)][a_num] == "X" or
                    computer_board.board[int(b)][a_num] == "O"
                ):
                    print(
                        f"\n***You already shot {a.upper()} {b}! "
                        "Please choose another coordinate***\n"
                    )
                else:
                    computer_board.guess_computer_ships(a, b, computer_coords)
                    player_board.turn_count += 1
                    flag = False
            except ValueError:
                print(
                    "\n***Attention! Your coordinates should be a letter "
                    "from A to E and a number from 1 to 5, separated by a "
                    "space.\nThe letter should come before the number.***\n"
                )


def computer_turn():
    """
    Guesses a random coordinate to shoot at by executing the
    guess_player_ships() method of the Board class. Then adds 1 to the
    turn_count instance variable of the computer_board instance.
    """
    player_board.guess_player_ships(player_name)
    computer_board.turn_count += 1


title = [
    [" *", "-", "-", "-", "-", "-", "*", "-", "-", "-", "-", "*"],
    [" ", " B", "A", "T", "T", "L", "E", "S", "H", "I", "P", " "],
    [" *", "-", "-", "-", "-", "-", "*", "-", "-", "-", "-", "*"],
]

instructions = """Hello and welcome to this game of battleship! Let me
explain how it works: You will have to face the computer in this strategic
naval game, and each of you will try to sink each other's fleet.
You each have 5 ships, placed strategically on your board.
Only you can see your ships, and you cannot see the computer's ships.
The same is true the other way around: The computer can only see their
own ships, but not yours.

First, you will have to enter your name, then you have to place your own ships
by entering coordinates. Place your ships wisely!Once your ships are placed,
you and the computer will take turns to shoot at coordinates of each other's
boards. Whoever manages to sink the enemy fleet first, wins! If you miss,
a "O" will appear on your enemies board, and when you hit an enemy ship an "X"
will appear. You can't shoot the same coordinates twice! Good luck!"""


def show_title_and_instructions():
    """
    Displays the title and instructions variables.
    """
    for row in title:
        print(" ".join(row) + "\n")
    print(instructions)


def place_ships():
    """
    Prompts the player to select whether they want to place their ships
    themselves or if they want to have them placed randomly. Changes the
    user input to lowercase. If the user input is neither one of the two
    options, prints "input not valid" and the loop runs again.
    If the user input is "n": uses the create_five_random_coordinates method
    and places a ship at each of the five coordinates. If the user input
    is "y": runs a loop that lets the user insert a coordinate for 5 times and
    places a ship at that coordinate. If the player mistakenly chose the
    same coordinate twice, an message will be printed to the terminal and
    the user will be asked to insert a new coordinate. Checks that the user's
    input has the correct lenght and contains usable data for the function
    with a try statement.
    """
    ships_placed = False
    while ships_placed is False:
        ship_placement = input(
            "You can either choose the coordinates of your ships yourself "
            "or you can have your ships placed randomly on the board.\n"
            "Do you want to choose the coordinates yourself? "
            "Type 'y' for yes or 'n' for no:\n"
        )
        if ship_placement.lower() == "n":
            coordinates = player_board.create_five_random_coordinates()
            for coor in coordinates:
                a, b = coor
                player_board.place_ships(a, b)
            player_board.display_board()
            ships_placed = True
        elif ship_placement.lower() == "y":
            i = 0
            while i < 5:
                player_coordinates = input(
                    "\nPlease insert the coordinates where you want to place "
                    f"ship number {i + 1}.\nThe coordinates should be the "
                    " column letter and the row number, separated by a space "
                    "(like this: A 1):\n"
                )
                try:
                    a, b = player_coordinates.split()
                    a_num = player_board.column_number(a)
                    if player_board.board[int(b)][a_num] == "@":
                        print(
                            "\n***You already have placed a ship at this "
                            "coordinate! Please choose another "
                            "coordinate.***\n"
                        )
                    else:
                        player_board.place_ships(a, b)
                        i += 1
                        player_board.display_board()
                except ValueError:
                    print(
                        "\n***Your coordinates have to be exactly two "
                        "characters, should be separated by a space and the "
                        "letter should come before the number.\nPlease insert "
                        "them again!***"
                    )
            ships_placed = True
        else:
            print(
                "\n***Input not valid, please insert either y or n without "
                "any space and then press enter***"
            )
    computer_board.display_board()


def start_game():
    """
    Determines who starts the game randomly. If the player wins, runs a loop
    with the player_turn and compuyter_turn functions while both players still
    have all of their ships. If at any point the ship_count of one of the
    players drops to zero, the loop stops.
    """
    coin_flip = random.randrange(1, 3)
    if coin_flip == 1:
        print("---You start first. Good luck!---")
        while computer_board.ship_count > 0 and player_board.ship_count > 0:
            player_turn()
            if computer_board.ship_count == 0 or player_board.ship_count == 0:
                player_board.display_board()
                computer_board.display_board()
                break
            computer_turn()
            player_board.display_board()
            computer_board.display_board()
    else:
        print("---Your enemy starts first! You start second. Good luck!---")
        while computer_board.ship_count > 0 and player_board.ship_count > 0:
            computer_turn()
            player_board.display_board()
            computer_board.display_board()
            if computer_board.ship_count == 0 or player_board.ship_count == 0:
                break
            player_turn()


def game_over():
    """
    Displays a message announcing the winner and updates the win instance
    variable of the player who won.
    """
    if computer_board.ship_count == 0:
        print("\n---Congratulations, you won!---\n")
        player_board.win += 1
    elif player_board.ship_count == 0:
        print("\n---GAME OVER! The enemy has sunken our entire fleet...---\n")
        computer_board.win += 1


def get_game_stats(n_turns, p_hitrate, c_hitrate):
    """
    Takes stats from the "stats" google sheet, calculates averages and displays
    them to the player comparing them to the player's stats from the current
    game.
    @n_turns: number of total turns from the current game
    @p_hitrate: player hit rate of the current game
    @c_hitrate: computer hit rate of the current game
    """
    turns_column = stats.col_values(1)
    n_of_turns_list = [int(x) for x in turns_column[1:]]
    avg_n_of_turns = sum(n_of_turns_list) / len(n_of_turns_list)

    player_hit_rate_column = stats.col_values(4)
    player_hit_rate_list = [float(x) for x in player_hit_rate_column[1:]]
    avg_player_hit_rate = sum(player_hit_rate_list) / len(player_hit_rate_list)

    computer_hit_rate_column = stats.col_values(5)
    computer_hr_list = [float(x) for x in computer_hit_rate_column[1:]]
    avg_computer_hit_rate = sum(computer_hr_list) / len(computer_hr_list)

    print(
        "\nBelow you can see your stats compared to the average stats of "
        "people who played this game previously\n"
    )
    print(
        tabulate(
            [
                [
                    "This game",
                    n_turns,
                    f"{round(p_hitrate, 1)}%",
                    f"{round(c_hitrate, 1)}%",
                ],
                [
                    "Average",
                    round(avg_n_of_turns, 1),
                    f"{round(avg_player_hit_rate, 1)}%",
                    f"{round(avg_computer_hit_rate, 1)}%",
                ],
            ],
            headers=[
                "",
                "Number of turns",
                "Player hit rate",
                "Computer hit rate"
            ],
        )
    )


def update_stats_spreadsheet():
    """
    Updates a google sheet with game stats from the current game. Calls the
    get_game_stats() function.
    """
    print("Updating stats...")
    num_of_turns = player_board.turn_count + computer_board.turn_count
    computer_hit_rate = (
        player_board.num_of_getting_hit / computer_board.turn_count * 100
    )
    c_num_ghit = computer_board.num_of_getting_hit
    player_hit_rate = c_num_ghit / player_board.turn_count * 100

    current_game_stats = [
        num_of_turns,
        player_board.win,
        computer_board.win,
        player_hit_rate,
        computer_hit_rate,
    ]

    stats.append_row(current_game_stats)
    get_game_stats(num_of_turns, player_hit_rate, computer_hit_rate)


play_game = True
while play_game:
    show_title_and_instructions()

    computer_board = Board("Computer")
    computer_coords = computer_board.create_five_random_coordinates()

    player_name = input("Please enter your name:\n")
    player_board = Board(player_name)
    player_board.display_board()

    place_ships()
    start_game()
    game_over()
    update_stats_spreadsheet()

    question_answered = False
    while question_answered is False:
        user_answer = input(
            "\nWould you like to play another game? "
            "Insert 'y' for yes and 'n' for no:\n"
        )
        if user_answer.lower().strip() == "y":
            question_answered = True
        elif user_answer.lower().strip() == "n":
            play_game = False
            question_answered = True
        else:
            print("***Invalid input, please type either y or n***")
