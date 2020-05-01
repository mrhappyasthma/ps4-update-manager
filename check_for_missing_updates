import argparse
import json
import os
import urllib2

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help='Prints the status of all games', action='store_true')
args = parser.parse_args()

base_url = 'https://ps4.octolus.net/dataApi?id={}&env=NP&method=patches'
headers = {
  'User-Agent' :
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

current_dir = os.getcwd()
for name in os.listdir(current_dir):
  folder_path = os.path.join(current_dir, name)
  if os.path.isdir(folder_path):
    version_path = os.path.join(folder_path, "version.txt")
    current_version = ''
    with open(version_path, 'r') as file:
      current_version = file.read()

    game_id_path = os.path.join(folder_path, "id.txt")
    game_id = ''
    with open(game_id_path, 'r') as file:
      game_id = file.read()

    if game_id and current_version:
      url = base_url.format(game_id)
      request = urllib2.Request(url, headers=headers)
      response = urllib2.urlopen(request)
      data = json.loads(response.read())
      version = ''
      try:
        version = data['tag']['package']['@attributes']['version']
        if version == current_version:
          if args.verbose:
            print name + ' is up to date'
        else:
          print 'New version ' + version + ' is available for ' + name
      except KeyError:
        print 'failed for game' + name
        print game_id
        print url
