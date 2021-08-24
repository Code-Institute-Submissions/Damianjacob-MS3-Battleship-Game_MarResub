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
        self.ship_count = 5
        self.turn_count = 0
        self.win = 0
        self.num_of_getting_hit = 0
        self.coordinates_list = [
            (col, row) for col in range(1, 6) for row in range(1, 6)
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
        col_num = self.column_number(col)
        coords = [int(row), col_num]
        if coords in coor_list:
            self.board[int(row)][col_num] = "X"
            coor_list.remove(coords)
            self.ship_count -= 1
            self.num_of_getting_hit += 1
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
            self.board[int(row)][col_num] = "O"

    def guess_player_ships(self, player_name):
        """
        Pulls a random coordinate from the coordinate_list instance variable, then removes that coordinate
        from the coordinate_list and changes the corresponding character on the board based on
        whether that character is an @ or not.
        """
        i = len(self.coordinates_list)
        rand_index = random.randrange(i)
        rand_coordinate = self.coordinates_list[rand_index]

        col, row = rand_coordinate
        coordinate = self.board[row][col]
        self.coordinates_list.remove(rand_coordinate)
        if coordinate == "@":
            self.board[row][col] = "X"
            self.ship_count -= 1
            self.num_of_getting_hit += 1
            if self.ship_count > 1:
                print(
                    f"\n---{player_name}! The enemy has sunken our ship at {self.board[0][col].upper()} {row}! We still have {self.ship_count} ships in our fleet.---"
                )
            elif self.ship_count == 1:
                print(
                    f"\n---{player_name}! The enemy has sunken our ship at {self.board[0][col].upper()} {row}! We only have {self.ship_count} ship left...---"
                )
            else:
                print(
                    f"\n---{player_name}! The enemy has sunken our last ship at {self.board[0][col].upper()} {row}! We are defeated!---"
                )
        else:
            print(
                f"\n---The enemy shot {self.board[0][col].upper()} {row}. It's a miss!---"
            )
            self.board[row][col] = "O"
