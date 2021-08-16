import random


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

    def display_board(self):
        """
        Prints the board and the name of its player to the terminal.
        """
        print(f"{self.name}'s board")
        for row in self.board:
            joint_row = "  ".join(row)
            print(f"{joint_row}\n")

    def place_ships(self, col, row):
        """
        Converts the column letter to a number based on the letter's index in the first list of the board list
        """
        col_num = self.board[0].index(col.upper())
        self.board[int(row)][col_num] = "@"

    def place_ships_randomly(self):
        """
        Creates 5 random coordinates without duplicates and returns them in a list of lists.
        """
        col_list = ["A", "B", "C", "D", "E"]
        row_list = [1, 2, 3, 4, 5]
        coordinate_list = []
        x = 0
        while x < 5:
            rand_col = random.choice(col_list)
            rand_row = random.choice(row_list)
            col_num = self.board[0].index(rand_col.upper())
            rand_coordinates = [rand_row, col_num]
            if rand_coordinates in coordinate_list:
                pass
            else:
                coordinate_list.append(rand_coordinates)
                x += 1
        return coordinate_list


# player_name = input(
#     "Hello and welcome to this game of battleship! Please enter your name: "
# )
player_board = Board("player")
computer_board = Board("Computer")

player_board.display_board()

i = 0
while i < 5:
    player_coordinates = input(
        f"Please insert the coordinates where you want to place ship number {i + 1}. You have 5 ships in total. \nThe coordinates should be the column letter and the row number, separated by a space (like this: A 1): "
    )
    try:
        a, b = player_coordinates.split()
        player_board.place_ships(a, b)
    except ValueError:
        print(
            "Your coordinates have to be exactly two characters, should be separated by a space and the letter should come before the number. Please insert them again!"
        )
    else:
        a, b = player_coordinates.split()
        player_board.place_ships(a, b)
        i += 1
        player_board.display_board()

computer_board.place_ships_randomly()
computer_board.display_board()
