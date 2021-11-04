from typing import List
import json
import os

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
                preferred["left"] += 1 + x_weight + y_weight
            # right
            if x_diff > head:
                preferred["right"] += 1 + x_weight + y_weight
            # down
            if y_diff < head:
                preferred["down"] += 1 + x_weight + y_weight
            # up
            if y_diff > head:
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
    if best_moves:
        description = "food found {}".format(' '.join(best_moves)),
    else:
        description = "no food found"
    play = {
        "objectID": board,
        "board": board,
        "best_move": best_moves,
        "description": description,
        "remove_moves": []
    }
    return play


def save_plays(plays: List[dict], filename: str):
    # MAke sure outputs directory exists
    os.makedirs('outputs', exist_ok=True)
    # Write the records to a file
    with open(filename, 'w') as outfile:
        json.dump(plays, outfile, indent=2)
