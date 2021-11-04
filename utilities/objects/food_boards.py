from typing import List, Set
from copy import deepcopy


def add_board(boards: Set[str], board: str) -> List[str]:
    boards.add(board)
    return boards


def print_board(size: int, board: str):
    print(board)
    print(len(board))
    for i in range(len(board), 0, -size):
        row = ''
        for j in range(i - size, i):
            row += board[j]
    print(row)


def inverse_board(board: str) -> str:
    board = board.replace('S', 'X')
    board = board.replace('O', 'S')
    board = board.replace('X', 'O')
    return board


def in_boards(boards: List[dict], board: dict) -> bool:
    return board in boards


def create_board(board_size: int, apples: List[dict]) -> str:
    """

    return: A string representing food directly surrounding the snake's head.
    """
    board = ''
    head = board_size//2
    for y in range(0, board_size):
        for x in range(0, board_size):
            space = 'S'
            if x == head and y == head:
                space = "H"
            else:
                for apple in apples:
                    if x == apple["x"] and y == apple["y"]:
                        space = "O"
            board += space
    return board


def add_apple(apples: List[dict], x: int, y: int) -> List[dict]:
    apples.append({"x": x, "y": y})
    return apples


def in_apples(apples: List[dict], x: int, y: int) -> bool:
    match = False
    for apple in apples:
        if x == apple["x"] and y == apple["y"]:
            match = True
    return match


def recursive_boards(board_size: int = 3, depth: int = 0, apples: List[dict] = [], boards: Set[str] = set()):
    head = board_size//2
    max_depth = (board_size**2-1)
    # print("  At depth {} with {}".format(depth, apples))
    board = create_board(board_size, apples)
    boards = add_board(boards, board)
    # We can halve the the recursion depth by also adding the inverse of the
    # generated board
    boards = add_board(boards, inverse_board(board))
    if depth != max_depth:
        for y in range(0, board_size):
            for x in range(0, board_size):
                local_apples = deepcopy(apples)
                if not (x == head and y == head) and not (in_apples(local_apples, x, y)):
                    local_apples = add_apple(local_apples, x, y)
                    local_board = create_board(board_size, local_apples)
                    if not in_boards(boards, local_board):
                        boards = recursive_boards(board_size, depth+1, local_apples, boards)
    print("{} boards({}  {})".format(len(boards), board, inverse_board(board)))
    return boards


def generate_boards(board_size: int = 3) -> Set[str]:
    return recursive_boards(board_size)
