import random

INF = 1000
DEPTH = 3


def findBestMove(gs, validMoves):
    random.shuffle(validMoves)
    score, bestMove = findMoveAlphaBeta(gs, validMoves, DEPTH, -INF, INF, 1 if not gs.is_hider_move else -1)
    return bestMove


# Định nghĩa hàm alpha-beta search chính
def findMoveAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    if depth == 0:
        return gs.evaluate(), None

    bestMove = None

    if turnMultiplier == 1:  # Seeker's turn, maximizing score
        bestScore = -INF
        for move in validMoves:
            gs.move_support(move)
            next_moves = gs.getAllPossibleMoves()
            score, _ = findMoveAlphaBeta(gs, next_moves, depth - 1, alpha, beta, -turnMultiplier)
            gs.undo_move()

            if score > bestScore:
                bestScore = score
                if depth == DEPTH:
                    bestMove = move
                alpha = max(alpha, score)

            if alpha >= beta:
                break
        return bestScore, bestMove

    else:  # Hider's turn, minimizing score
        bestScore = INF
        for move in validMoves:
            gs.move_support(move)
            next_moves = gs.getAllPossibleMoves()
            score, _ = findMoveAlphaBeta(gs, next_moves, depth - 1, alpha, beta, -turnMultiplier)
            gs.undo_move()

            if score < bestScore:
                bestScore = score
                if depth == DEPTH:
                    bestMove = move
                beta = min(beta, score)
            if beta <= alpha:
                break
        return bestScore, bestMove



