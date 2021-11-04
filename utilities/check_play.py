from objects.food_plays import create_play
import math

board = 'SSSSSSSSSSSSHSSSSSSSSOSSS'

board_length = int(math.sqrt(len(board)))
print(board_length)
print(create_play(board_length, board))
