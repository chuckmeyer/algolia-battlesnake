from typing import List, Dict, Set
from copy import deepcopy
import json

from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


def load_plays(filename: str) -> List[dict]:
  print("Loading file {}...".format(filename))
  play_file = open(filename, 'r')
  return json.load(play_file)


def update_index(plays: str, index: str = ''):
  # Create the index
  print("Updating index {}".format(index))
  client = SearchClient.create(os.getenv('APP_ID'), os.getenv('API_KEY'))
  index = client.init_index(index)
  index.clear_objects()
  index.save_objects(plays)


if __name__ == "__main__":
  BOARD_SIZE = 5
  plays = load_plays("../outputs/{}x{}-food-plays.json".format(BOARD_SIZE, BOARD_SIZE))
  index = "boards-apples-{}x{}".format(BOARD_SIZE, BOARD_SIZE)
  #for play in plays:
  #  print(play["board"])
  print("Importing records...")
  update_index(plays, index)