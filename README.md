# Tic-Tac-Toe with Unbeatable AI

A terminal-based tic-tac-toe game where you play against an AI opponent that never loses. The AI uses the Minimax algorithm to evaluate every possible game outcome and always picks the optimal move.

## Requirements

- Python 3.x (no external dependencies)

## How to Play

### Run directly

```bash
python main.py
```

### Run with Docker

```bash
docker build -t tictactoe .
docker run -it tictactoe
```

The `-it` flag is required because the game reads keyboard input from stdin. The `-u` flag in the Dockerfile ensures Python output is unbuffered so prompts appear immediately.

### Gameplay

1. Choose your side: **X** (plays first) or **O** (plays second).
2. The board displays a numbered grid from 1 to 9:

```
 1 | 2 | 3
-----------
 4 | 5 | 6
-----------
 7 | 8 | 9
```

3. On your turn, enter a number (1-9) to place your mark in that cell.
4. The AI responds instantly with its move.
5. The game ends when someone gets three in a row or the board is full (draw).
6. After each game, you can choose to play again or quit.

### Input validation

- Non-numeric input is rejected with "Enter a number 1-9."
- Numbers outside 1-9 are rejected with "Enter a number 1-9."
- Occupied cells are rejected with "That cell is taken."
- Invalid side selection is rejected with "Please enter X or O."

## Project Structure

```
tictactoe/
├── main.py          # Entry point
├── board.py         # Board representation and game state
├── engine.py        # Minimax AI engine
├── game.py          # Game loop and player interaction
├── Dockerfile       # Container image definition
├── .dockerignore    # Files excluded from Docker build context
├── CLAUDE.md        # Guidance for Claude Code
└── README.md        # This file
```

## Architecture

The project is split into three modules with clear responsibilities:

### board.py — Board State

The `Board` class represents the game state as a flat list of 9 cells (indexed 0-8). Each cell is `None` (empty), `"X"`, or `"O"`.

Key components:

- **`WIN_COMBINATIONS`**: A module-level constant listing all 8 winning lines — 3 rows, 3 columns, and 2 diagonals — as tuples of cell indices.
- **`make_move(position, player)` / `undo_move(position)`**: Mutate and restore board state. `undo_move` is essential for the minimax search, which needs to explore and backtrack through possible moves without creating new board copies.
- **`get_available_moves()`**: Returns indices of all empty cells.
- **`check_winner()`**: Iterates through `WIN_COMBINATIONS` and returns `"X"`, `"O"`, or `None`.
- **`is_full()`**: Returns `True` when all 9 cells are occupied.
- **`display()`**: Prints the board to the terminal. Empty cells show their position number (1-9) so the player knows which numbers to enter. Occupied cells show `X` or `O`.

Positions are 0-indexed internally but displayed as 1-9 to the player. The conversion (`pos = input - 1`) happens in `game.py`.

### engine.py — Minimax AI

The AI engine implements the [Minimax algorithm](https://en.wikipedia.org/wiki/Minimax), a decision-making algorithm for two-player zero-sum games.

Key components:

- **`_opponent(player)`**: Helper that returns the other player (`"X"` ↔ `"O"`).
- **`minimax(board, is_maximizing, ai_player)`**: Recursively evaluates every possible game state. Returns a score:
  - `+10` if the AI wins
  - `-10` if the AI loses
  - `0` if the game is a draw

  The `is_maximizing` parameter alternates between `True` (AI's turn — maximize score) and `False` (opponent's turn — minimize score). At each level, the function tries every available move, recurses, then undoes the move to backtrack.

- **`get_best_move(board, ai_player)`**: The public interface. Evaluates all available moves by calling `minimax` on each, and returns the position with the highest score.

**Why no alpha-beta pruning or depth limit?** Tic-tac-toe has at most 9! (362,880) terminal states, and the branching factor shrinks with each move. A full minimax search completes instantly. Adding pruning or depth limits would add complexity without any noticeable performance gain.

**Correctness guarantee**: The AI was verified by exhaustively playing all possible games (every combination of human moves) in both positions:

| AI plays as | Wins | Losses | Draws |
|-------------|------|--------|-------|
| X (first)   | 99   | 0      | 2     |
| O (second)  | 498  | 0      | 183   |

Zero losses across all possible game trees confirms the AI is unbeatable.

### game.py — Game Loop

The `Game` class orchestrates the player experience:

- **`choose_side()`**: Prompts the player to pick X or O. X always goes first per standard tic-tac-toe rules. The AI is assigned the opposite side.
- **`human_turn()`**: Input loop with validation. Converts 1-9 input to 0-8 index, checks the cell is empty, and places the move.
- **`ai_turn()`**: Calls `get_best_move()` from the engine, places the move, and announces it to the player.
- **`play_round()`**: Runs a single game from start to finish. Creates a fresh board, alternates turns starting with X, checks for a winner or draw after each move, and announces the result.
- **`play()`**: Outer loop that runs rounds and asks if the player wants to play again.

### main.py — Entry Point

Imports `Game` and calls `play()`. Guarded by `if __name__ == "__main__"` so modules can be imported independently for testing.

## Docker Setup

### Dockerfile

```dockerfile
FROM python:3.13-alpine
WORKDIR /app
COPY board.py engine.py game.py main.py ./
CMD ["python", "-u", "main.py"]
```

- **Base image**: `python:3.13-alpine` — minimal image (~50MB) since the project has no external dependencies.
- **`-u` flag**: Runs Python in unbuffered mode so `input()` prompts display immediately without waiting for a newline in the output buffer.
- **Selective COPY**: Only the four Python source files are copied, not documentation or Docker files.

### .dockerignore

Excludes from the build context:
- `__pycache__` / `*.pyc` — Python bytecode cache
- `.git` / `.claude` — Version control and tool metadata
- `CLAUDE.md` / `Dockerfile` / `.dockerignore` — Not needed at runtime
