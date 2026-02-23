from board import Board
from engine import get_best_move


class Game:
    def __init__(self):
        self.board = Board()
        self.human = None
        self.ai = None

    def choose_side(self):
        while True:
            choice = input("Play as X or O? (X goes first): ").strip().upper()
            if choice in ("X", "O"):
                self.human = choice
                self.ai = "O" if choice == "X" else "X"
                return
            print("Please enter X or O.")

    def human_turn(self):
        while True:
            raw = input(f"Your move ({self.human}) [1-9]: ").strip()
            if not raw.isdigit():
                print("Enter a number 1-9.")
                continue
            pos = int(raw) - 1
            if pos < 0 or pos > 8:
                print("Enter a number 1-9.")
                continue
            if pos not in self.board.get_available_moves():
                print("That cell is taken.")
                continue
            self.board.make_move(pos, self.human)
            return

    def ai_turn(self):
        move = get_best_move(self.board, self.ai)
        self.board.make_move(move, self.ai)
        print(f"AI plays position {move + 1}")

    def play_round(self):
        self.board = Board()
        self.choose_side()
        current = "X"

        self.board.display()
        while True:
            if current == self.human:
                self.human_turn()
            else:
                self.ai_turn()

            self.board.display()

            winner = self.board.check_winner()
            if winner:
                if winner == self.human:
                    print("You win!")
                else:
                    print("AI wins!")
                return

            if self.board.is_full():
                print("It's a draw!")
                return

            current = "O" if current == "X" else "X"

    def play(self):
        print("=== Tic-Tac-Toe ===")
        while True:
            self.play_round()
            again = input("Play again? (y/n): ").strip().lower()
            if again != "y":
                print("Thanks for playing!")
                break
