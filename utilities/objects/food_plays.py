from typing import List


def find_best_moves(board_size: int, board: str) -> List[str]:
    head = board_size//2
    preferred = {
        "left": 0,
        "right": 0,
        "up": 0,
        "down": 0,
    }

    for loc, value in enumerate(board):
        if value == 'O':
            x_diff = loc % board_size
            y_diff = loc // board_size
            x_weight = head - abs(x_diff - head)
            y_weight = head - abs(y_diff - head)

            # left
            if x_diff < head:
                print("{} left weight is 1 + {} + {}".format(loc, x_weight, y_weight))
                preferred["left"] += 1 + x_weight + y_weight
            # right
            if x_diff > head:
                print("{} right weight is 1 + {} + {}".format(loc, x_weight, y_weight))
                preferred["right"] += 1 + x_weight + y_weight
            # down
            if y_diff < head:
                print("{} down weight is 1 + {} + {}".format(loc, x_weight, y_weight))
                preferred["down"] += 1 + x_weight + y_weight
            # up
            if y_diff > head:
                print("{} up weight is 1 + {} + {}".format(loc, x_weight, y_weight))
                preferred["up"] += 1 + x_weight + y_weight

    best_move_score = max(preferred, key=preferred.get)
    best_moves = []
    if preferred[best_move_score] != 0:
        for move in preferred.keys():
            if preferred[move] == preferred[best_move_score]:
                best_moves.append(move)
    print("Best moves for {} are {}: {}".format(board, best_moves, preferred))
    return best_moves


def create_play(board_size: int, board: str) -> dict:
    best_moves = find_best_moves(board_size, board)
    play = {
        "objectID": board,
        "board": board,
        "best_move": best_moves,
        "description": "apple {}".format(' '.join(best_moves)),
        "remove_moves": []
    }
    return play
