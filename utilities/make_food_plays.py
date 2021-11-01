from objects.food_boards import generate_boards, save_boards
from objects.food_plays import create_play
from objects.algolia_index import update_index

BOARD_SIZE = 3

def get_plays(board_size: int = 3):
  plays = []
  boards = generate_boards(board_size)
  for board in boards:
    plays.append(create_play(board_size, board))
  return plays


if __name__ == "__main__":
  index = "boards-apples-{}x{}".format(BOARD_SIZE, BOARD_SIZE)
  all_plays = get_plays(BOARD_SIZE)
  print('--------------------------------')
  #print(json.dumps(all_plays))
  print("Generated {} moves".format(len(all_plays)))
  save_boards(all_plays, "outputs/{}x{}-food-plays.json".format(BOARD_SIZE, BOARD_SIZE))
  update_index(all_plays, index)