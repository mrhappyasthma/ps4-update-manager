import json
import os
import urllib2

current_dir = os.getcwd()
for name in os.listdir(current_dir):
  folder_path = os.path.join(current_dir, name)
  if os.path.isdir(folder_path):
    game_id_path = os.path.join(folder_path, "id.txt")
    game_id = ''
    with open(game_id_path, 'r') as file:
      game_id = file.read()

    if not game_id:
      print 'Missing game ID info for: ' + name
