from algoliasearch.search_client import SearchClient
from typing import List, Dict

client = SearchClient.create('3X7W8M7P92', 'd8205d3319b85f7c42a0ccd39f20d84b')

def vision_to_string(vision: List[str]) -> str:
  return ''.join(vision)

def remove_move(move: str, possible_moves: List[str]) -> List[str]:
  if move in possible_moves:
    possible_moves.remove(move)
  return possible_moves

def avoid_walls(vision: List[str], possible_moves: List[str]) -> List[str]:
  index = client.init_index('boards-walls')
  print("Searching for walls in " + vision_to_string(vision))
  results = index.search(vision_to_string(vision))
  if results['hits']:
    print("Search detected " + results['hits'][0]['description'])
    for move in results['hits'][0]['remove_moves']:
      possible_moves = remove_move(move, possible_moves)
  return possible_moves
  
def find_food(size: int, vision: str, possible_moves: List[str]) -> List[str]:
  best_moves = []
  board_index = 'boards-apples-' + str(size) + 'x' + str(size)
  index = client.init_index(board_index)
  print("Searching for food in " + vision)
  results = index.search(vision)
  if results['hits']:
    print("Search detected " + results['hits'][0]['description'])
    for move in results['hits'][0]['best_move']:
      if move in possible_moves:
        best_moves.append(move)
        print("Added " + move + " to best moves [" + str(best_moves) + "]")
  return best_moves
