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
        Creates 5 random coordinates without duplicates and returns them in a list of lists.
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

    def guess_computer_ships(self, col, row):
        """
        Let's the player guess the computer's ship coordinates
        """
        coordinate_list = self.create_five_random_coordinates()
        col_num = self.column_number(col)
        coords = [row, col_num]
        print(f"coords: {coords}")
        print(f"coordinate_list before: {coordinate_list}")
        if coords in coordinate_list:
            print("It's a hit!")
            self.board[int(row)][col_num] = "x"
            coordinate_list.remove(coords)
        else:
            print("It's a miss...")
            self.board[int(row)][col_num] = "o"
        print(f"coordinate_list after: {coordinate_list}")


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

for row in title:
    print(" ".join(row) + "\n")

print(instructions)

player_name = input("Please enter your name: ")
player_board = Board(player_name)
computer_board = Board("Computer")

player_board.display_board()

ships_placed = False
while ships_placed == False:
    ship_placement = input(
        "You can either choose the coordinates of your ships yourself or you can let the computer choose random coordinates for you.\nDo you want to choose the coordinates yourself? Type 'y' for yes or 'n' for no: "
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
        ships_placed = True
    else:
        print("Input not valid")


computer_board.create_five_random_coordinates()
computer_board.display_board()

flag = True
while flag == True:
    coordinates = input(
        "Which coordinates do you want to shoot?\nThe coordinates should be the column letter and the row number, separated by a space (like this: A 1): "
    )
    if coordinates == "none":
        flag = False
    else:
        try:
            a, b = coordinates.split()
            computer_board.guess_computer_ships(a, b)
        except ValueError:
            print(
                "Your coordinates have to be exactly two characters, should be separated by a space and the letter should come before the number. Please insert them again!"
            )
        else:
            a, b = coordinates.split()
            computer_board.guess_computer_ships(a, b)
            player_board.display_board()
            computer_board.display_board()
