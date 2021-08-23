import random
from tabulate import tabulate
import gspread
from google.oauth2.service_account import Credentials

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


# import sys

# sys.path.append("board-class.py")

# from boardclass.py import Board

existing_rows = len(stats.row_values(1))

existing_columns = len(stats.col_values(1))

print(existing_columns)
print(existing_rows)


def get_game_stats(n_turns, p_hitrate, c_hitrate):
    """
    @n_turns

    """

    turns_column = stats.col_values(1)
    n_of_turns_list = [int(x) for x in turns_column[1:]]
    avg_n_of_turns = sum(n_of_turns_list) / len(n_of_turns_list)

    player_wins_column = stats.col_values(2)
    player_wins_list = [int(x) for x in player_wins_column[1:]]
    tot_player_wins = sum(player_wins_list)

    computer_wins_column = stats.col_values(3)
    computer_wins_list = [int(x) for x in computer_wins_column[1:]]
    tot_computer_wins = sum(computer_wins_list)

    player_hit_rate_column = stats.col_values(4)
    player_hit_rate_list = [int(x) for x in player_hit_rate_column[1:]]
    avg_player_hit_rate = sum(player_hit_rate_list) / len(player_hit_rate_list)

    computer_hit_rate_column = stats.col_values(5)
    computer_hit_rate_list = [int(x) for x in computer_hit_rate_column[1:]]
    avg_computer_hit_rate = sum(computer_hit_rate_list) / len(computer_hit_rate_list)

    print(
        "\nBelow you can see your stats compared to the average stats of people who played this game previously\n"
    )
    print(
        tabulate(
            [
                ["This game", n_turns, p_hitrate, c_hitrate, "-", "-"],
                [
                    "Average",
                    avg_n_of_turns,
                    avg_player_hit_rate,
                    avg_computer_hit_rate,
                    tot_player_wins,
                    tot_computer_wins,
                ],
            ],
            headers=[
                "",
                "Number of turns",
                "Player hit rate",
                "Computer hit rate",
                "Total player wins",
                "Total computer wins",
            ],
        )
    )


# get_game_stats(43, 23, 20)


class Board:
    """
    Creates a board instance for playing the battleship game. Contains methods for displaying the board and placing ships.
    """

    def __init__(self, name):
        self.name = name
        self.board = [
            [" ", "A", "B", "C", "D", "E"],
            ["1", "~", "~", "~", "~", "~"],
            ["2", "~", "~", "~", "~", "~"],
            ["3", "~", "~", "~", "~", "~"],
            ["4", "~", "~", "~", "~", "~"],
            ["5", "~", "~", "~", "~", "~"],
        ]
        self.ship_count = 5
        self.turn_count = 0
        self.win = 0
        self.num_of_getting_hit = 5 - self.ship_count
        self.coordinates_list = [
            (col, row) for col in range(1, 6) for row in range(1, 6)
        ]

    def column_number(self, col):
        """
        Converts a letter from a to e to a number based on the letter's index in the first nested list inside the board list
        """
        print("$$$ executing column_number() $$$")
        return self.board[0].index(col.upper())

    def display_board(self):
        """
        Prints the board and the name of its player to the terminal.
        """
        print("$$$ executing display_board() $$$")
        print(f"\n   {self.name}'s board:\n")
        for row in self.board:
            joint_row = "   ".join(row)
            print(f"{joint_row}\n")

    def place_ships(self, col, row):
        """
        Places ships (represented by "@") at the coordinates specified by the player
        """
        print("$$$ executing place_ships() $$$")
        if type(col) is str:
            col_num = self.column_number(col)
        else:
            col_num = col
        self.board[int(row)][col_num] = "@"

    def create_five_random_coordinates(self):
        """
        Creates 5 random coordinates without duplicates and returns them in a nested list.
        """
        print("$$$ executing create_five_random_coordinates $$$")
        col_list = ["A", "B", "C", "D", "E"]
        row_list = [1, 2, 3, 4, 5]
        coordinate_list = []
        x = 0
        while x < 5:
            col = random.choice(col_list)
            row = random.choice(row_list)
            col_num = self.column_number(col)
            rand_coordinates = [row, col_num]
            if rand_coordinates in coordinate_list:
                pass
            else:
                coordinate_list.append(rand_coordinates)
                x += 1
        return coordinate_list

    def guess_computer_ships(self, col, row, coor_list):
        """
        Lets the player guess the computer's ship coordinates.
        """
        print("$$$ executing guess_computer_ships $$$")
        col_num = self.column_number(col)
        coords = [int(row), col_num]
        # print(f"coords: {coords}")
        # print(f"coordinate_list before: {coor_list}")
        if coords in coor_list:
            self.board[int(row)][col_num] = "x"
            coor_list.remove(coords)
            self.ship_count -= 1
            if self.ship_count > 1:
                print(
                    f"\n---You shot {col.upper()} {row}, it's a hit! We need to sink {self.ship_count} more ships to destroy the enemy's fleet---"
                )
            elif self.ship_count == 1:
                print(
                    f"\n---You shot {col.upper()} {row}, it's a hit! We only need to sink one more ship to destroy the enemy's fleet!---"
                )
        else:
            print(f"\n---You shot {col.upper()} {row}, it's a miss...---")
            self.board[int(row)][col_num] = "o"
        # print(f"coordinate_list after: {coor_list}")

    def guess_player_ships(self):
        """
        The loop generates a random coordinate and checks which character is at that coordinate.
        if the character is x or o, it does nothing but the loop will start
        over again. If there is an @ it transforms it into an x and detracts one point
        from the ship count.
        """
        print("$$$ executing guess_player_ships $$$")

        print(self.coordinates_list)
        i = len(self.coordinates_list)
        print(f"i (length of coordinates list): {i}")
        rand_index = random.randrange(i)
        print(f"rand_index: {rand_index}")
        rand_coordinate = self.coordinates_list[rand_index]
        print(f"rand_coordinate: {rand_coordinate}")

        col, row = rand_coordinate
        coordinate = self.board[row][col]
        self.coordinates_list.remove(rand_coordinate)
        if coordinate == "@":
            print("$$$ executing code for when there is an undamaged ship (@) $$$")
            self.board[row][col] = "x"
            self.ship_count -= 1
            if self.ship_count > 1:
                print(
                    f"\n---{player_name}! The enemy has sunken our ship at {self.board[0][col].upper()} {row}! We still have {self.ship_count} ships in our fleet.---"
                )
            else:
                print(
                    f"\n---{player_name}! The enemy has sunken our ship at {self.board[0][col].upper()} {row}! We only have {self.ship_count} ship left...---"
                )
        else:
            print(
                "$$$ executing code for when at the coordinates there is not an @ $$$"
            )
            print(
                f"\n---The enemy shot {self.board[0][col].upper()} {row}. It's a miss!---"
            )
            self.board[row][col] = "o"
        print(f"coordinates after while loop inside guess_player_ships: {coordinate}")
        print(f"ship_count after loop: {self.ship_count}")


def player_turn():
    """
    Prompts the player to insert the coordinates they want to attack. Checks for the coordinates correct length and returns an
    error message if the lenght is shorter or longer than intended. Checks if a value error is raised and returns a message if so.
    In both cases the user will be asked to insert the coordinates again. If the coordinates are correct, this function checks if
    those coordinates are in the computer_coordinates list, which contains five randomly generated coordinates. If yes, it
    puts an x on the computer board and removes the coordinates from computer_coordinates. Otherwise, it puts an o on the computer board.
    """
    print("$$$ executing player_turn $$$")
    flag = True
    while flag == True:
        coordinates = input(
            "Which coordinates do you want to shoot?\nThe coordinates should be the column letter and the row number, separated by a space (like this: A 1): "
        )
        if len(coordinates) > 3:
            print(
                "\n***Attention! Your input is too long. Tt should only contain a letter, a space and a number.***\n"
            )
            continue
        elif len(coordinates) < 3:
            print(
                "\n***Attention! Your input is too short. It should only contain a letter, a space and a number.***\n"
            )
            continue
        else:
            try:
                a, b = coordinates.split()
                if (
                    computer_board.board[int(b)][computer_board.column_number(a)] == "x"
                    or computer_board.board[int(b)][computer_board.column_number(a)]
                    == "o"
                ):
                    print(
                        f"\n***You already shot {a.upper()} {b}! Please choose another coordinate***"
                    )
                else:
                    computer_board.guess_computer_ships(a, b, computer_coordinates)
                    player_board.turn_count += 1
                    flag = False
            except ValueError:
                print(
                    "\n***Attention! Your coordinates should be a letter from A to E and a number from 1 to 5, separated by a space. The letter should come before the number.***\n"
                )


def computer_turn():
    print("$$$ executing computer_turn $$$")
    player_board.guess_player_ships()
    computer_board.turn_count += 1


title = [
    [" *", "-", "-", "-", "-", "-", "*", "-", "-", "-", "-", "*"],
    [" ", " B", "A", "T", "T", "L", "E", "S", "H", "I", "P", " "],
    [" *", "-", "-", "-", "-", "-", "*", "-", "-", "-", "-", "*"],
]

instructions = """Hello and welcome to this game of battleship! \nLet me explain how it works: You will have to face the computer in this strategic naval game, and each of you will try to sink each other's fleet.
You each have 5 ships, placed strategically on your board. Only you can see your ships, and you cannot see the computer's ships. 
The same is true the other way around: The computer can only see their own ships, 
but not yours. 

First, you will have to enter your name, then you have to place your own ships by entering coordinates. Place your ships wisely!
Once your ships are placed, you and the computer will take turns to shoot at coordinates of each other's boards. Whoever manages to sink the enemy fleet first, wins!
If you miss, a "o" will appear on your enemies board, and when you hit an enemy ship an "x" will appear. You can't shoot the same coordinates twice! Good luck!
"""


def show_title_and_instructions():
    for row in title:
        print(" ".join(row) + "\n")
    print(instructions)


def place_ships():
    """
    Prompts the player to select whether they want to place their ships themselves or if they want to
    have them placed randomly. Changes the user input to lowercase. If the user input is neither one of the two options,
    prints "input not valid" and the loop runs again.
    If the user input is "n": uses the create_five_random_coordinates method and places a ship at each of the five coordinates.
    If the user input is "y": runs a loop that lets the user insert a coordinate for 5 times and places a ship at that coordinate. If the
    player mistakenly chose the same coordinate twice, an message will be printed to the terminal and the user will be asked to insert
    a new coordinate.
    Checks that the user's input has the correct lenght and contains usable data for the function with a try statement.
    """
    print("$$$ executing place_ships $$$")
    ships_placed = False
    while ships_placed == False:
        ship_placement = input(
            "You can either choose the coordinates of your ships yourself or you can have your ships placed randomly on the board.\nDo you want to choose the coordinates yourself? Type 'y' for yes or 'n' for no: "
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
                    f"Please insert the coordinates where you want to place ship number {i + 1}.\nThe coordinates should be the column letter and the row number, separated by a space (like this: A 1): "
                )
                try:
                    a, b = player_coordinates.split()
                    if player_board.board[int(b)][player_board.column_number(a)] == "@":
                        print(
                            "\n***You already have placed a ship at this coordinate! Please choose another coordinate.***\n"
                        )
                    else:
                        player_board.place_ships(a, b)
                        i += 1
                        player_board.display_board()
                except ValueError:
                    print(
                        "***Your coordinates have to be exactly two characters, should be separated by a space and the letter should come before the number. Please insert them again!***"
                    )
            ships_placed = True
        else:
            print(
                "***Input not valid, please insert either y or n without any space and then press enter***"
            )
    computer_board.display_board()


def start_game():
    """
    Determines who starts the game by flipping a coin. If the player wins, runs a loop with the player_turn and compuyter_turn functions
    while both players still have all of their ships. If at any point the ship_count of one of the players drops to zero, the loop
    stops.
    """
    print("$$$ executing start_game $$$")
    coin_flip = random.randrange(1, 3)
    if coin_flip == 1:
        print("---You start first. Good luck!---")
        while computer_board.ship_count > 0 and player_board.ship_count > 0:
            print(
                "$$$ executing while loop for alternating turns inside start_game $$$"
            )
            player_turn()
            if computer_board.ship_count == 0 or player_board.ship_count == 0:
                print(
                    "$$$ breaking out of loop because either player has a ship count of 0 $$$"
                )
                print(
                    f"comp ship count:{computer_board.ship_count} player ship count: {player_board.ship_count}"
                )
                player_board.display_board()
                computer_board.display_board()
                break
            computer_turn()
            player_board.display_board()
            computer_board.display_board()
    else:
        print("---Your enemy starts first! You start second. Good luck!---")
        while computer_board.ship_count > 0 and player_board.ship_count > 0:
            print(
                "$$$ executing while loop for alternating turns inside start_game $$$"
            )
            computer_turn()
            player_board.display_board()
            computer_board.display_board()
            if computer_board.ship_count == 0 or player_board.ship_count == 0:
                print(
                    "$$$ breaking out of loop because either player has a ship count of 0 $$$"
                )
                print(
                    f"comp ship count:{computer_board.ship_count} player ship count: {player_board.ship_count}"
                )
                break
            player_turn()


def game_over():
    print("$$$ executing game_over $$$")
    if computer_board.ship_count == 0:
        print("\n---Congratulations, you won!---\n")
        player_board.win += 1
    elif player_board.ship_count == 0:
        print("\n---GAME OVER! The enemy has sunken our entire fleet...---\n")
        computer_board.win += 1


def update_stats_spreadsheet(game_stats):
    """
    Updates a google sheet with game stats from the current game
    """
    print("$$$ executing update_stats_spreadsheet $$$")
    stats.append_row(game_stats)


play_game = True
while play_game == True:
    show_title_and_instructions()

    computer_board = Board("Computer")
    computer_coordinates = computer_board.create_five_random_coordinates()

    player_name = input("Please enter your name: ")
    player_board = Board(player_name)
    player_board.display_board()

    place_ships()
    start_game()
    game_over()

    # The following piece of code calculates game stats and updates the google sheet where they are stored
    num_of_turns = player_board.turn_count + computer_board.turn_count
    computer_hit_rate = (
        player_board.num_of_getting_hit / computer_board.turn_count * 100
    )
    player_hit_rate = computer_board.num_of_getting_hit / player_board.turn_count * 100

    current_game_stats = [
        num_of_turns,
        player_board.win,
        computer_board.win,
        player_hit_rate,
        computer_hit_rate,
    ]

    update_stats_spreadsheet(current_game_stats)

    question_answered = False
    while question_answered == False:
        user_answer = input(
            "Would you like to play another game? insert 'y' for yes and 'n' for no, insert 's' to see your game stats: "
        )
        if user_answer.lower().strip() == "y":
            question_answered = True
        elif user_answer.lower().strip() == "n":
            play_game = False
            question_answered = True
        elif user_answer.lower().strip() == "s":
            pass
        else:
            print("***Invalid input, please type either y or n***")
