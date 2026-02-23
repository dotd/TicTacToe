WIN_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


class Board:
    def __init__(self):
        self.cells = [None] * 9

    def make_move(self, position, player):
        self.cells[position] = player

    def undo_move(self, position):
        self.cells[position] = None

    def get_available_moves(self):
        return [i for i, cell in enumerate(self.cells) if cell is None]

    def check_winner(self):
        for a, b, c in WIN_COMBINATIONS:
            if self.cells[a] and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return None

    def is_full(self):
        return all(cell is not None for cell in self.cells)

    def display(self):
        print()
        for row in range(3):
            parts = []
            for col in range(3):
                idx = row * 3 + col
                cell = self.cells[idx]
                parts.append(f" {cell} " if cell else f" {idx + 1} ")
            print("|".join(parts))
            if row < 2:
                print("-----------")
        print()
