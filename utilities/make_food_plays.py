from objects.food_boards import generate_boards
from objects.food_plays import create_play, save_plays
from objects.algolia_index import update_index
from time import perf_counter

BOARD_SIZE = 5


def get_plays(board_size: int = 3):
    plays = []
    boards = generate_boards(board_size)
    for board in boards:
        plays.append(create_play(board_size, board))
    return plays


if __name__ == "__main__":
    index = f"boards-apples-{BOARD_SIZE}x{BOARD_SIZE}"
    tic = perf_counter()
    all_plays = get_plays(BOARD_SIZE)
    toc = perf_counter()
    print('--------------------------------')
    # print(json.dumps(all_plays))
    print(f"Generated {len(all_plays)} moves in {toc - tic:0.4f} seconds")
    save_plays(all_plays, f"outputs/{BOARD_SIZE}x{BOARD_SIZE}-food-plays.json")
    update_index(all_plays, index)
