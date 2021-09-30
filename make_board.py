from typing import List, Dict
from copy import deepcopy

def board_to_string(vision: List[str]) -> str:
  return ''.join(vision)


def add_board(boards: List[str], board: str) -> List[dict]:
  boards = boards
  #print("  Checking if {} is in {}".format(board, boards))
  if in_boards(boards, board):
    print("  Duplicate board")
  else:
    boards.append(board)
  return(boards)


def in_boards(boards: List[str], board: str) -> bool:
  if board in boards:
    print("Found {} in {}".format(board, boards))
    return True
  else:
    print("Did NOT find {} in {}".format(board, boards))
    return False

def create_apple_board(apples: List[dict]) -> str:
    """

    return: A matrix representing the 8 blocks directly surrounding the snake's head.
    """
    
    board = []
    preferred = {
      "left": 0,
      "right": 0,
      "up": 0,
      "down": 0,
    }
    for x in range(0, 3):
      for y in range(0, 3):
        space = "."
        if x == 1 and y == 1:
          space = "H"
        else:
          for apple in apples:
            if x == apple["x"] and y == apple["y"]:
              if x < 1:
                preferred["left"] += 1
              elif x > 1:
                preferred["right"] += 1
              if y < 1:
                preferred["down"] += 1
              elif y > 1:
                preferred["up"] += 1
              space = "O"
        board.append(space)
    #print(board_to_string(board))
    #print(dict(sorted(preferred.items(), key=lambda item: item[1], reverse=True)))
    return board_to_string(board)


def add_apple(apples: List[dict], x: int, y: int) -> List[dict]:
  print("Adding apple at {} x {}".format(x, y))
  #print(apples)
  if x == 1 and y == 1:
    print("Apple already eaten")
    return apples
  for apple in apples:
    if x == apple["x"] and y == apple["y"]:
      print("Duplicate apple")
      return apples
  apples.append({ "x": x, "y": y})
  print("Apple added: {}".format(apples))
  return apples


def in_apples(apples: List[dict], x: int, y:int) -> bool:
  match = False
  for apple in apples:
    if x == apple["x"] and y == apple["y"]:
      match = True
  return match


def recursive_apples(max_depth: int, depth: int, apples: List[dict]):
  print("  At depth {} with {}".format(depth, apples))
  local_boards = []
  if depth != max_depth:
    for x in range(0,3):
      for y in range(0,3):
        local_apples = deepcopy(apples)
        if in_apples(local_apples, x, y):
          print("Skipping duplicate apple")
        else:
          local_apples = add_apple(local_apples, x, y)
          if in_boards(local_boards, create_apple_board(local_apples)):
            print("  Skipping duplicate board tree")
          else:
            print("Entering depth {} with {}".format(depth+1, local_apples))
            local_boards += recursive_apples(max_depth, depth+1, local_apples)
            print("Returned to depth {}: {}".format(depth, local_boards))
  else:
    local_boards = add_board(local_boards, create_apple_board(apples))
    print("  Added leaf: {}".format(local_boards))
  #local_boards.append(create_apple_board(apples))
  #print("Local boards: {}".format(local_boards))
  return(local_boards)

if __name__ == "__main__":
  apples = []
  all_boards = recursive_apples(2,0, apples)
  print('--------------------------------')
  print("Generated {} boards:".format(len(all_boards)))
  print(all_boards)
