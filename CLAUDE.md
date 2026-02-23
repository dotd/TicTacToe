# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Game

```
python main.py
```

No dependencies beyond Python 3 standard library.

## Architecture

Text-based tic-tac-toe with an unbeatable AI opponent using the Minimax algorithm.

- **`board.py`** — `Board` class: 9-cell list representation, move/undo, win detection via `WIN_COMBINATIONS`, display as numbered grid (1-9)
- **`engine.py`** — Minimax AI: `get_best_move(board, ai_player)` returns optimal position. Scores: +10 win, -10 loss, 0 draw. Exhaustive search (no pruning needed for 3x3)
- **`game.py`** — `Game` class: player side selection, turn loop, input validation, delegates AI moves to engine
- **`main.py`** — Entry point

## Key Design Decisions

- Board positions are 0-indexed internally, displayed as 1-9 to the player
- Minimax has no depth limit or alpha-beta pruning — the game tree is small enough (~9! nodes) that full search is instant
- The AI is guaranteed to never lose: it wins or draws every game
