from typing import List, Dict
from copy import deepcopy
import json

def board_to_string(vision: List[str]) -> str:
  return ''.join(vision)


def add_board(boards: List[dict], board: dict) -> List[dict]:
  global dup_count
  boards = deepcopy(boards)
  #print("  Checking if {} is in {}".format(board, boards))
  if in_boards(boards, board["board"]):
    print("  Duplicate board: {}".format(board["board"]))
    dup_count += 1
  else:
    boards.append(board)
  return(boards)


def get_boards(boards: List[dict]):
  return([ sub['board'] for sub in boards ])


def in_boards(boards: List[dict], board: dict) -> bool:
  board_values = get_boards(boards)
  return(board in board_values)


def create_board(board_size: int, apples: List[dict]) -> dict:
    """

    return: A matrix representing the 8 blocks directly surrounding the snake's head.
    """
    temp_board = {}
    board = []
    head = board_size//2
    preferred = {
      "left": 0,
      "right": 0,
      "up": 0,
      "down": 0,
    }
    for y in range(0, board_size):
      for x in range(0, board_size):
        space = "."
        if x == head and y == head:
          space = "H"
        else:
          for apple in apples:
            if x == apple["x"] and y == apple["y"]:
              if x < head:
                preferred["left"] += 1
              if x > head:
                preferred["right"] += 1
              if y < head:
                preferred["down"] += 1
              if y > head:
                preferred["up"] += 1
              space = "O"
        board.append(space)
    #print(board_to_string(board))
    best_move_score = max(preferred, key=preferred.get)
    #print("Best move is {}: {}".format(best_move_score, preferred))
    best_moves = []
    if preferred[best_move_score] != 0:
      for move in preferred.keys():
        if preferred[move] == preferred[best_move_score]:
          best_moves.append(move)
    temp_board= {
      "board": board_to_string(board),
      "best_move": best_moves,
      "description": "apple {}".format(' '.join(best_moves)),
      "remove_moves": []
    }
    return temp_board


def save_boards(boards: List[dict], filename: str):
  # Write the records to a file
  with open(filename, 'w') as outfile:
    json.dump(boards, outfile, indent=2)


def add_apple(apples: List[dict], x: int, y: int) -> List[dict]:
  #print("Adding apple at {} x {}".format(x, y))
  for apple in apples:
    if x == apple["x"] and y == apple["y"]:
      print("Duplicate apple")
      return apples
  apples.append({ "x": x, "y": y})
  #print("Apple added: {}".format(apples))
  return apples


def in_apples(apples: List[dict], x: int, y:int) -> bool:
  match = False
  for apple in apples:
    if x == apple["x"] and y == apple["y"]:
      match = True
  return match


def recursive_apples(board_size: int = 3, depth: int = 0, boards: List[dict] = [], apples: List[dict] = []):
  head = board_size//2
  max_depth = board_size**2-1
  #print("  At depth {} with {}".format(depth, apples))
  boards = add_board(boards, create_board(board_size, apples))
  if depth != max_depth:
    for y in range(0,board_size):
      for x in range(0,board_size):
        local_apples = deepcopy(apples)
        if not (x == head and y == head) and not (in_apples(local_apples, x, y)):
          local_apples = add_apple(local_apples, x, y)
          #print("Entering depth {} with {}".format(depth+1, local_apples))
          local_board = create_board(board_size, local_apples)
          if in_boards(boards, local_board):
            print("  Pruning duplicate board: {}".format(local_board["board"]))
#            global dup_count
#            dup_count += 1
          else:
            boards = recursive_apples(board_size, depth+1, boards, local_apples)
          #print("Returned to depth {}: {}".format(depth, get_boards(boards)))
  #print("  Adding leaf: {}".format(get_boards(boards)))
  #print("  Added leaf: {}".format(get_boards(boards)))
  print("{} boards ({} dups)".format(len(boards),dup_count))
  return(boards)

if __name__ == "__main__":
  global dup_count
  dup_count = 0
  all_boards = recursive_apples(3, 0, [], [])
  print('--------------------------------')
  print("Generated {} boards:".format(len(all_boards)))
  print(json.dumps(all_boards))
  save_boards(all_boards, 'all-apple-boards.json')