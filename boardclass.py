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

    def column_number(self, col):
        """
        Converts a letter from a to e to a number based on the letter's index in the first nested list inside the board list
        """
        return self.board[0].index(col.upper())

    def display_board(self):
        """
        Prints the board and the name of its player to the terminal.
        """
        print(f"\n   {self.name}'s board:\n")
        for row in self.board:
            joint_row = "   ".join(row)
            print(f"{joint_row}\n")

    def place_ships(self, col, row):
        """
        Places ships (represented by "@") at the coordinates specified by the player
        """
        if type(col) is str:
            col_num = self.column_number(col)
        else:
            col_num = col
        self.board[int(row)][col_num] = "@"

    def create_five_random_coordinates(self):
        """
        Creates 5 random coordinates without duplicates and returns them in a nested list.
        """
        col_list = ["A", "B", "C", "D", "E"]
        row_list = [1, 2, 3, 4, 5]
        coordinate_list = []
        x = 0
        while x < 5:
            rand_col = random.choice(col_list)
            rand_row = random.choice(row_list)
            col_num = self.column_number(rand_col)
            rand_coordinates = [rand_row, col_num]
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
        col_num = self.column_number(col)
        coords = [int(row), col_num]
        print(f"coords: {coords}")
        print(f"coordinate_list before: {coor_list}")
        if coords in coor_list:
            print("It's a hit!")
            self.board[int(row)][col_num] = "x"
            coor_list.remove(coords)
        else:
            print("It's a miss...")
            self.board[int(row)][col_num] = "o"
        print(f"coordinate_list after: {coor_list}")
