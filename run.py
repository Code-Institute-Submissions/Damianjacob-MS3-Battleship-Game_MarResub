class Board:
    board = [
        [" ", "A", "B", "C", "D", "E"],
        ["1", "~", "~", "~", "~", "~"],
        ["2", "~", "~", "~", "~", "~"],
        ["3", "~", "~", "~", "~", "~"],
        ["4", "~", "~", "~", "~", "~"],
        ["5", "~", "~", "~", "~", "~"],
    ]

    def __init__(self, name):
        self.name = name

    def display_board(self):
        print(f"{self.name}'s board")
        for row in self.board:
            joint_row = " ".join(row)
            print(f"{joint_row}\n")

    def place_ships(self, row, col):
        self.board[row][col] = "@"


player_board = Board("Damian")

player_board.place_ships(2, 3)

player_board.display_board()
