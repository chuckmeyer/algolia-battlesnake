import random
from typing import List, Dict
import find_board

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


def remove_move(move: str, possible_moves: List[str]) -> List[str]:
    if move in possible_moves:
        possible_moves.remove(move)
    return possible_moves


def current_direction(my_head: Dict[str, int], my_body: List[dict]) -> str:
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        return "right"
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        return "left"
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        return "up"
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        return "down"


def wall_vision(my_head: Dict[str, int], board: Dict[str, int]) -> List[str]:
    """

    return: A matrix representing the 8 blocks directly surrounding the snake's head.
    """

    top_row = board["height"] - 1
    right_column = board["width"] - 1
    vision = []
    for y in range(my_head["y"]-1, my_head["y"]+2):
        for x in range(my_head["x"]-1, my_head["x"]+2):
            if y < 0 or y > top_row:  # near wall
                vision.append("X")
            elif x < 0 or x > right_column:  # near wall
                vision.append("X")
            elif my_head["x"] == x and my_head["y"] == y:
                vision.append("H")
            else:
                vision.append("S")
    return vision


def apple_vision(size: int, my_head: Dict[str, int], board: Dict[str, int]) -> str:
    """

    return: A matrix representing the blocks directly surrounding the snake's head.
    """

    vision = ''
    x_range = range(my_head['x'] - size//2, my_head['x'] + size//2 + 1)
    y_range = range(my_head['y'] - size//2, my_head['y'] + size//2 + 1)

    for y in y_range:
        for x in x_range:
            space = "S"
            if my_head["x"] == x and my_head["y"] == y:
                space = "H"
            else:
                for apple in board["food"]:
                    if x == apple["x"] and y == apple["y"]:
                        space = "O"
            vision += space
    return vision


def print_vision(size: int, board: str):
    for i in range(len(board), 0, -size):
        row = ''
        for j in range(i - size, i):
            row += board[j]
        print(row)


def avoid_walls(my_head: Dict[str, int], board: Dict[str, int], possible_moves: List[str]) -> List[str]:
    top_row = board["height"] - 1
    right_column = board["width"] - 1

    if my_head["x"] == 0:  # near left wall
        print("Detected left wall")
        remove_move("left", possible_moves)
    elif my_head["x"] == right_column:  # near right wall
        print("Detected right wall")
        remove_move("right", possible_moves)

    if my_head["y"] == 0:  # near bottom wall
        print("Detected bottom wall")
        remove_move("down", possible_moves)
    elif my_head["y"] == top_row:  # near top wall
        print("Detected top wall")
        remove_move("up", possible_moves)

    return possible_moves


def avoid_snakes(my_head: Dict[str, int], snakes: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    snakes: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves not blocked by other snakes
    """
    for snake in snakes:
        for segment in snake["body"]:
            if my_head["x"] - 1 == segment["x"] and my_head["y"] == segment["y"]:
                print("Segment to the left")
                remove_move("left", possible_moves)
            if my_head["x"] + 1 == segment["x"] and my_head["y"] == segment["y"]:
                print("Segment to the right")
                remove_move("right", possible_moves)
            if my_head["x"] == segment["x"] and my_head["y"] - 1 == segment["y"]:
                print("Segment below")
                remove_move("down", possible_moves)
            if my_head["x"] == segment["x"] and my_head["y"] + 1 == segment["y"]:
                print("Segment above")
                remove_move("up", possible_moves)

            # We're going to be super conservative if we're near another head
            # to avoid head on collisions
            if my_head["x"] - 2 == snake["head"]["x"] and my_head["y"] == snake["head"]["y"]:
                print("Dodge the head!")
                remove_move("left", possible_moves)
            if my_head["x"] + 2 == snake["head"]["x"] and my_head["y"] == snake["head"]["y"]:
                print("Dodge the head!")
                remove_move("right", possible_moves)
            if my_head["x"] == snake["head"]["x"] and my_head["y"] - 2 == snake["head"]["y"]:
                print("Dodge the head!")
                remove_move("down", possible_moves)
            if my_head["x"] == snake["head"]["x"] and my_head["y"] + 2 == snake["head"]["y"]:
                print("Dodge the head!")
                remove_move("up", possible_moves)
            if my_head["x"] - 1 == snake["head"]["x"] and my_head["y"] + 1 == snake["head"]["y"]:
                print("Dodge the head!")
                remove_move("left", possible_moves)
                remove_move("up", possible_moves)
            if my_head["x"] - 1 == snake["head"]["x"] and my_head["y"] - 1 == snake["head"]["y"]:
                print("Dodge the head!")
                remove_move("left", possible_moves)
                remove_move("down", possible_moves)
            if my_head["x"] + 1 == snake["head"]["x"] and my_head["y"] + 1 == snake["head"]["y"]:
                print("Dodge the head!")
                remove_move("right", possible_moves)
                remove_move("up", possible_moves)
            if my_head["x"] + 1 == snake["head"]["x"] and my_head["y"] - 1 == snake["head"]["y"]:
                print("Dodge the head!")
                remove_move("right", possible_moves)
                remove_move("down", possible_moves)
    return possible_moves


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    # my_vision = wall_vision(my_head, data["board"])
    # print_vision(my_vision)
    my_apple_vision = apple_vision(5, my_head, data["board"])
    # print_vision(3, my_apple_vision)

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    # print(f"All board data this turn: {data}")
    print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    print(f"My Battlesnakes head this turn is: {my_head}")
    print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # TODO: Using information from 'data', find the edges of the board and don't let your Battlesnake move beyond them
    possible_moves = avoid_walls(my_head, data["board"], possible_moves)
    """
    # Right now edge detection is minimal -- it's not worth using search here.
    # If we can build out the edge detection to include combinations of walls
    # and snakes, this could be worth a second search
    """
    # possible_moves = find_board.avoid_walls(my_vision, possible_moves)

    # TODO Using information from 'data', don't let your Battlesnake pick a move that would hit its own body
    # TODO: Using information from 'data', don't let your Battlesnake pick a move that would collide with another Battlesnake
    possible_moves = avoid_snakes(my_head, data["board"]["snakes"], possible_moves)

    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board
    best_moves = find_board.find_food(5, my_apple_vision, possible_moves)
    print(f"Best moves: {best_moves}")

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = ''
    if possible_moves:
        for best_move in best_moves:
            if best_move in possible_moves:
                move = best_move
                print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked as best move {possible_moves}")
                return move
        direction = current_direction(my_head, my_body)
        if direction in possible_moves:
            move = direction
            print(f"{data['game']['id']} MOVE {data['turn']}: Continue going {move}")
            return move
        if "left" in possible_moves and "right" in possible_moves:
            if my_head["x"] > data["board"]["width"]//2:
                move = "left"
                print(f"{data['game']['id']} MOVE {data['turn']}: More room {move}")
                return move
            else:
                move = "right"
                print(f"{data['game']['id']} MOVE {data['turn']}: More room {move}")
                return move
        if "up" in possible_moves and "down" in possible_moves:
            if my_head["y"] > data["board"]["height"]//2:
                move = "down"
                print(f"{data['game']['id']} MOVE {data['turn']}: More room {move}")
                return move
            else:
                move = "up"
                print(f"{data['game']['id']} MOVE {data['turn']}: More room {move}")
                return move
        move = random.choice(possible_moves)
        print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked randomly from all valid options in {possible_moves}")
        return move
    else:
        print("No possible moves.")
        return "down"
    # TODO: Explore new strategies for picking a move that are better than random
