# Scripts for ['Games Nebula'](https://github.com/yancharkin/games_nebula) (GOG games)

All linux native games, scummvm and dosbox wrapped games, some windows games will work out of the box. For games that doesn't work or require additional components there are two solutions in 'Games Nebula':  **autosetup.ini** and **bash scripts**.

Also this repository contains gui utilities (written in python) for configurating and (sometimes) patching games.


## autosetup.ini
#### Available option:

- **image** - image url. If option exists ‘Games Nebula’ will download this image and use it to represent game in you library.
- **native_exe** - path to main executable (linux) (1)
- **native_settings_exe** - path to configuration utility (linux) (1)
- **win_exe** - path to main executable (windows) (1)
- **win_settings_exe** - path to configuration utility (windows) (1)
- **winetricks** - components to install with winetricks
- **dos_iso** - path to disk image (1)
- **dos_exe** - path to main executable (dos) (1)
- **dos_settings_exe** - path to configuration utility (dos) (1)
- **scummvm_name** - name used in ScummVM
- **scummvm_id** - id used in ScummVM
- **special** - additional commands (copy, move, remove files, etc.) (2)
- **win_reg1, win_reg2, etc.** - keys to add to registry (windows) (2). **This option(s) should be at the end!**

*(1) - path relative to 'game' directory*

*(2) - see existing examples*
## Bash scripts
If for some reason **autosetup.ini** is not enough, it's possible to use bash script. It will be executed during installation. See existing examples.
#### Available environment variables:
- **$DOWNLOAD_DIR** - absolute path to download directory
- **$INSTALL_DIR** - absolute path to install directory
- **$WINE_PATH** - absolute path to directory containing wine or 'wine' if system wine version used
- **$GAME_NAME** - game id used by gog
- **$START_FILE** - absolute path to 'start.sh'
- **$START_GOG_FILE** - absolute path to 'start_gog.sh'
- **$START_GN_FILE** - absolute path to 'start_gn.sh'
- **$SETTINGS_FILE** - absolute path to 'settings.sh'
- **$ADDITIONS_FILE** - absolute path to 'additions.sh'
- **$DOSBOX_GAME_CONF** - absolute path to 'dosbox_game.conf'
- **$DOSBOX_SETTINGS_CONF** - absolute path to 'dosbox_settings.conf'
