import json
import os
import re
import sys
import time
import urllib
import urllib2

base_url = 'https://ps4.octolus.net/dataApi?id={}&env=NP&method=patches'
headers = {
  'User-Agent' :
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

def report_hook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    if duration <= 0:
      duration = 1
    speed = int(progress_size / (1024 * duration))
    if total_size <= 0:
      total_size = 1
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()

def download_pkg(download_url, folder_path):
  if not download_url:
    raise KeyError('Could not find download URL')
  filename = download_url.split('/')[-1]
  save_location = os.path.join(folder_path, filename)
  print 'Saving file "' + filename + '" at path: ' + save_location
  urllib.urlretrieve(download_url, save_location, report_hook)

current_dir = os.getcwd()
for name in os.listdir(current_dir):
  folder_path = os.path.join(current_dir, name)
  if os.path.isdir(folder_path):
    version_path = os.path.join(folder_path, "version.txt")
    current_version = ''
    with open(version_path, 'r') as version_file:
      current_version = version_file.read()

    game_id_path = os.path.join(folder_path, "id.txt")
    game_id = ''
    with open(game_id_path, 'r') as game_id_file:
      game_id = game_id_file.read()
    if game_id:
      url = base_url.format(game_id)
      request = urllib2.Request(url, headers=headers)
      response = urllib2.urlopen(request)
      response_data = response.read()
      sanitized_data = re.sub('<.+\n', '', response_data, flags=re.MULTILINE)
      data = json.loads(sanitized_data)
      version = ''
      try:
        error = data.get('error', False)
        if error:
          raise KeyError('Error found')

        version = data.get('tag', {}).get('package', {}).get('@attributes', {}).get('version', '')
        if not version and not current_version:
          # No patches available, so move on to the next game.
          continue
        elif not version:
          raise KeyError('Could not find a valid version number')
        if version != current_version:
          download_url = data.get('tag', {}).get('package', {}).get('delta_info_set', {}).get('@attributes', {}).get('url', '')
          if not download_url:
            download_url = data.get('tag', {}).get('package', {}).get('@attributes', {}).get('manifest_url', '')
          if download_url.endswith('.pkg'):
            download_pkg(download_url, folder_path)
          elif download_url.endswith('.json'):
            print 'Downloading manifest file at URL: ' + download_url
            request = urllib2.Request(download_url, headers=headers)
            response = urllib2.urlopen(request)
            manifest = json.loads(response.read())
            count = int(manifest.get('numberOfSplitFiles', 0))
            for i in range(count):
              pkg_url = manifest.get('pieces')[i].get('url', '')
              if pkg_url:
                download_pkg(pkg_url, folder_path)
          else:
            raise KeyError('Could not download at URL: ' + download_url)
          with open(version_path, 'w') as version_file:
            version_file.write(version)
          print 'Updated ' + name + ' to version v' + version
      except KeyError as k:
        print 'failed for game' + name
        print k
