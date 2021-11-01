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
      if x_diff < head:
        preferred["left"] += 1 + x_diff
      if x_diff > head:
        preferred["right"] += board_size - x_diff
      if y_diff < head:
        preferred["down"] += 1 + y_diff
      if y_diff > head:
        preferred["up"] += board_size - y_diff
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