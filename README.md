# ps4-update-manager
A collection of utilities to help manage PS4 update downloads from https://ps4database.io/.

Place these scripts into the root directory where you want to manage the PS4 game updates.

The expected folder structure for each game is:

- Can be named anything
- Must contain `id.txt`, containing the appropriate game ID. (As found on https://ps4database.io/)
- A `version.txt`, which is updated by the script to track the latest downloaded version.

The following scripts can be used to manage these directories:

1. `check_for_incomplete_dirs.py` - Checks all the sub-directories and outputs any that do not have a populated `id.txt`.
2. `check_for_missing_updates.py` - Checks all sub-directories to see if any have pending updates available. Optionally takes `-v` to print the status of every sub-directory. Otherwise it just prints the games with new updates available.
3. `download_missing_updates.py` - Goes through all sub-directories and downloads the update file for any sub-dirs that need it.
