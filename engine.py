def _opponent(player):
    return "O" if player == "X" else "X"


def minimax(board, is_maximizing, ai_player):
    winner = board.check_winner()
    if winner == ai_player:
        return 10
    if winner == _opponent(ai_player):
        return -10
    if board.is_full():
        return 0

    if is_maximizing:
        best = -100
        for move in board.get_available_moves():
            board.make_move(move, ai_player)
            best = max(best, minimax(board, False, ai_player))
            board.undo_move(move)
        return best
    else:
        best = 100
        for move in board.get_available_moves():
            board.make_move(move, _opponent(ai_player))
            best = min(best, minimax(board, True, ai_player))
            board.undo_move(move)
        return best


def get_best_move(board, ai_player):
    best_score = -100
    best_move = None
    for move in board.get_available_moves():
        board.make_move(move, ai_player)
        score = minimax(board, False, ai_player)
        board.undo_move(move)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move
