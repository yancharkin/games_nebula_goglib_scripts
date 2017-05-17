#!/usr/bin/env python2
# -*- Mode: Python; coding: utf-8; indent-tabs-install_mode: t; c-basic-offset: 4; tab-width: 4 -*-

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import ConfigParser
import gettext

current_dir = sys.path[0]

dict_lang = {
    'English':'ENG',
    'Français':'FRE',
    'Deutsch':'GER',
    'Italiano':'ITA',
    'Español':'SPA',
    'Svenska':'SWE',
    'Polski':'POL',
    'Nederlands':'DUT',
    #~ 'Hungarian':'HUN',
    #~ 'Korean':'KOR',
    #~ 'Dansk':'DAN',
    #~ 'Norsk':'NOR',
    'Česky':'CZE',
    #~ 'Arabic':'ARA',
    'Русский':'RUS',
    '日本語':'JPN',
    '简体中文':'CHI',
    '繁體中文':'CHT',
    #~ 'Portuguese':'POR',
    #~ 'Hindi':'HIN',
    #~ 'Bengali':'BEN',
    #~ 'Javanese':'JAV',
    #~ 'sermo Latinus':'LAT'
    }

class GUI:

    def __init__(self, nebula_dir):

        gettext.bindtextdomain('games_nebula', nebula_dir + '/locale')
        gettext.textdomain('games_nebula')
        self._ = gettext.gettext


        self.get_global_settings()
        self.config_load()
        self.create_main_window()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = self._("Dungeon Keeper"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            )
        self.main_window.connect('delete-event', self.quit_app)

        grid = Gtk.Grid(
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            row_spacing = 10,
            column_spacing = 10
            )

        label_game_res = Gtk.Label(
            halign = Gtk.Align.START,
            label = self._("In-game resolution")
            )

        self.entry_game_width = Gtk.Entry(
            placeholder_text = self._("Width"),
            xalign = 0.5,
            max_length = 4,
            text = self.game_width
            )
        self.entry_game_width.connect('changed', self.cb_entries_res)

        self.entry_game_height = Gtk.Entry(
            placeholder_text = self._("Height"),
            xalign = 0.5,
            max_length = 4,
            text = self.game_height
            )
        self.entry_game_height.connect('changed', self.cb_entries_res)

        label_menu_res = Gtk.Label(
            halign = Gtk.Align.START,
            label = self._("Menu resolution")
            )

        self.entry_menu_width = Gtk.Entry(
            placeholder_text = self._("Width"),
            xalign = 0.5,
            max_length = 4,
            text = self.menu_width
            )
        self.entry_menu_width.connect('changed', self.cb_entries_res)

        self.entry_menu_height = Gtk.Entry(
            placeholder_text = self._("Height"),
            xalign = 0.5,
            max_length = 4,
            text = self.menu_height
            )
        self.entry_menu_height.connect('changed', self.cb_entries_res)

        label_movies_res = Gtk.Label(
            halign = Gtk.Align.START,
            label = self._("Movies resolution")
            )

        self.entry_movies_width = Gtk.Entry(
            placeholder_text = self._("Width"),
            xalign = 0.5,
            max_length = 4,
            text = self.movies_width
            )
        self.entry_movies_width.connect('changed', self.cb_entries_res)

        self.entry_movies_height = Gtk.Entry(
            placeholder_text = self._("Height"),
            xalign = 0.5,
            max_length = 4,
            text = self.movies_height
            )
        self.entry_movies_height.connect('changed', self.cb_entries_res)

        label_failure_res = Gtk.Label(
            halign = Gtk.Align.START,
            label = self._("Failure resolution")
            )

        self.entry_failure_width = Gtk.Entry(
            placeholder_text = self._("Width"),
            xalign = 0.5,
            max_length = 4,
            text = self.failure_width
            )
        self.entry_failure_width.connect('changed', self.cb_entries_res)

        self.entry_failure_height = Gtk.Entry(
            placeholder_text = self._("Height"),
            xalign = 0.5,
            max_length = 4,
            text = self.failure_height
            )
        self.entry_failure_height.connect('changed', self.cb_entries_res)

        label_speed = Gtk.Label(
            halign = Gtk.Align.START,
            label = self._("Game speed")
            )

        self.adj_speed = Gtk.Adjustment(int(self.speed), 1, 100, 1, 10)

        scale_speed = Gtk.Scale(
            adjustment = self.adj_speed,
            orientation = Gtk.Orientation.HORIZONTAL,
            draw_value = True,
            value_pos = Gtk.PositionType.RIGHT,
            show_fill_level = True,
            digits = 0,
            round_digits = 0,
            )

        label_msensitivity = Gtk.Label(
            halign = Gtk.Align.START,
            label = self._("Mouse sensitivity")
            )

        self.adj_msensitivity = Gtk.Adjustment(int(self.msensitivity), 1, 100, 1, 10)

        scale_msensitivity = Gtk.Scale(
            adjustment = self.adj_msensitivity,
            orientation = Gtk.Orientation.HORIZONTAL,
            draw_value = True,
            value_pos = Gtk.PositionType.RIGHT,
            show_fill_level = True,
            digits = 0,
            round_digits = 0,
            )

        label_nointro = Gtk.Label(
            halign = Gtk.Align.START,
            label = self._("Skip intro animation")
            )

        self.switch_nointro = Gtk.Switch(
            halign = Gtk.Align.END,
            active = self.nointro
            )

        label_smooth = Gtk.Label(
            halign = Gtk.Align.START,
            label = self._("Smoothen video")
            )

        self.switch_smooth = Gtk.Switch(
            halign = Gtk.Align.END,
            active = self.smooth
            )

        label_nosound = Gtk.Label(
            halign = Gtk.Align.START,
            label = self._("Disable sound")
            )

        self.switch_nosound = Gtk.Switch(
            halign = Gtk.Align.END,
            active = self.nosound
            )

        label_censorship = Gtk.Label(
            halign = Gtk.Align.START,
            label = self._("Censorship")
            )

        self.switch_censorship = Gtk.Switch(
            halign = Gtk.Align.END,
            active = self.censorship
            )

        label_screenshots = Gtk.Label(
            halign = Gtk.Align.START,
            label = self._("Screenshots format")
            )

        self.combobox_screenshots = Gtk.ComboBoxText()

        format_list = ['BMP', 'HSI']
        format_index = 0
        for i in range(len(format_list)):
            self.combobox_screenshots.append_text(format_list[i])
            if format_list[i] == self.screenshots:
                format_index = i
        self.combobox_screenshots.set_active(format_index)

        label_lang = Gtk.Label(
            halign = Gtk.Align.START,
            label = self._("Language")
            )

        self.combobox_lang = Gtk.ComboBoxText()

        active_lang = 1
        i = 0
        for lang in sorted(dict_lang):
            self.combobox_lang.append_text(lang)
            if lang == self.language:
                active_lang = i
            i += 1
        self.combobox_lang.set_active(active_lang)

        label_sessions = Gtk.Label(
            halign = Gtk.Align.START,
            label = self._("TCP/IP sessions")
            )

        self.entry_sessions = Gtk.Entry(
            placeholder_text = self._("IP address"),
            text = self.sessions
            )

        button_save = Gtk.Button(
            label = self._("Save and quit"),
            )
        button_save.connect('clicked', self.cb_button_save)

        grid.attach(label_game_res, 0, 0, 1, 1)
        grid.attach(self.entry_game_width, 1, 0, 1, 1)
        grid.attach(self.entry_game_height, 2, 0, 1, 1)
        grid.attach(label_menu_res, 0, 1, 1, 1)
        grid.attach(self.entry_menu_width, 1, 1, 1, 1)
        grid.attach(self.entry_menu_height, 2, 1, 1, 1)
        grid.attach(label_movies_res, 0, 2, 1, 1)
        grid.attach(self.entry_movies_width, 1, 2, 1, 1)
        grid.attach(self.entry_movies_height, 2, 2, 1, 1)
        grid.attach(label_failure_res, 0, 3, 1, 1)
        grid.attach(self.entry_failure_width, 1, 3, 1, 1)
        grid.attach(self.entry_failure_height, 2, 3, 1, 1)
        grid.attach(label_speed, 0, 4, 1, 1)
        grid.attach(scale_speed, 1, 4, 2, 1)
        grid.attach(label_msensitivity, 0, 5, 1, 1)
        grid.attach(scale_msensitivity, 1, 5, 2, 1)
        grid.attach(label_nointro, 0, 6, 1, 1)
        grid.attach(self.switch_nointro, 1, 6, 2, 1)
        grid.attach(label_smooth, 0, 7, 1, 1)
        grid.attach(self.switch_smooth, 1, 7, 2, 1)
        grid.attach(label_nosound, 0, 8, 1, 1)
        grid.attach(self.switch_nosound, 1, 8, 2, 1)
        grid.attach(label_censorship, 0, 9, 1, 1)
        grid.attach(self.switch_censorship, 1, 9, 2, 1)
        grid.attach(label_screenshots, 0, 10, 1, 1)
        grid.attach(self.combobox_screenshots, 1, 10, 2, 1)
        grid.attach(label_lang, 0, 11, 1, 1)
        grid.attach(self.combobox_lang, 1, 11, 2, 1)
        grid.attach(label_sessions, 0, 12, 1, 1)
        grid.attach(self.entry_sessions, 1, 12, 2, 1)
        grid.attach(button_save, 0, 13, 3, 1)

        self.main_window.add(grid)
        self.main_window.show_all()

    def get_global_settings(self):

        global_config_file = os.getenv('HOME') + '/.games_nebula/config/config.ini'
        global_config_parser = ConfigParser.ConfigParser()
        global_config_parser.read(global_config_file)
        gtk_theme = global_config_parser.get('visuals', 'gtk_theme')
        gtk_dark = global_config_parser.getboolean('visuals', 'gtk_dark')
        icon_theme = global_config_parser.get('visuals', 'icon_theme')
        font = global_config_parser.get('visuals','font')
        screen = Gdk.Screen.get_default()
        gsettings = Gtk.Settings.get_for_screen(screen)
        gsettings.set_property('gtk-theme-name', gtk_theme)
        gsettings.set_property('gtk-application-prefer-dark-theme', gtk_dark)
        gsettings.set_property('gtk-icon-theme-name', icon_theme)
        gsettings.set_property('gtk-font-name', font)

    def config_load(self):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('Settings'):
            config_parser.add_section('Settings')

        if not config_parser.has_option('Settings', 'game_width'):
            self.game_width = 640
            config_parser.set('Settings', 'game_width', self.game_width)
        else:
            self.game_width = config_parser.get('Settings', 'game_width')

        if not config_parser.has_option('Settings', 'game_height'):
            self.game_height = 480
            config_parser.set('Settings', 'game_height', self.game_height)
        else:
            self.game_height = config_parser.get('Settings', 'game_height')

        if not config_parser.has_option('Settings', 'menu_width'):
            self.menu_width = 640
            config_parser.set('Settings', 'menu_width', self.menu_width)
        else:
            self.menu_width = config_parser.get('Settings', 'menu_width')

        if not config_parser.has_option('Settings', 'menu_height'):
            self.menu_height = 480
            config_parser.set('Settings', 'menu_height', self.menu_height)
        else:
            self.menu_height = config_parser.get('Settings', 'menu_height')

        if not config_parser.has_option('Settings', 'movies_width'):
            self.movies_width = 640
            config_parser.set('Settings', 'movies_width', self.movies_width)
        else:
            self.movies_width = config_parser.get('Settings', 'movies_width')

        if not config_parser.has_option('Settings', 'movies_height'):
            self.movies_height = 480
            config_parser.set('Settings', 'movies_height', self.movies_height)
        else:
            self.movies_height = config_parser.get('Settings', 'movies_height')

        if not config_parser.has_option('Settings', 'failure_width'):
            self.failure_width = 640
            config_parser.set('Settings', 'failure_width', self.failure_width)
        else:
            self.failure_width = config_parser.get('Settings', 'failure_width')

        if not config_parser.has_option('Settings', 'failure_height'):
            self.failure_height = 480
            config_parser.set('Settings', 'failure_height', self.failure_height)
        else:
            self.failure_height = config_parser.get('Settings', 'failure_height')

        if not config_parser.has_option('Settings', 'speed'):
            self.speed = 20
            config_parser.set('Settings', 'speed', self.speed)
        else:
            self.speed = config_parser.getint('Settings', 'speed')

        if not config_parser.has_option('Settings', 'msensitivity'):
            self.msensitivity = 100
            config_parser.set('Settings', 'msensitivity', self.msensitivity)
        else:
            self.msensitivity = config_parser.getint('Settings', 'msensitivity')

        if not config_parser.has_option('Settings', 'nointro'):
            self.nointro = False
            config_parser.set('Settings', 'nointro', self.nointro)
        else:
            self.nointro = config_parser.getboolean('Settings', 'nointro')

        if not config_parser.has_option('Settings', 'smooth'):
            self.smooth = False
            config_parser.set('Settings', 'smooth', self.smooth)
        else:
            self.smooth = config_parser.getboolean('Settings', 'smooth')

        if not config_parser.has_option('Settings', 'nosound'):
            self.nosound = False
            config_parser.set('Settings', 'nosound', self.nosound)
        else:
            self.nosound = config_parser.getboolean('Settings', 'nosound')

        if not config_parser.has_option('Settings', 'censorship'):
            self.censorship = False
            config_parser.set('Settings', 'censorship', self.censorship)
        else:
            self.censorship = config_parser.getboolean('Settings', 'censorship')

        if not config_parser.has_option('Settings', 'screenshots'):
            self.screenshots = 'BMP'
            config_parser.set('Settings', 'screenshots', self.screenshots)
        else:
            self.screenshots = config_parser.get('Settings', 'screenshots')

        if not config_parser.has_option('Settings', 'language'):
            self.language = 'English'
            config_parser.set('Settings', 'language', self.language)
        else:
            self.language = config_parser.get('Settings', 'language')

        if not config_parser.has_option('Settings', 'sessions'):
            self.sessions = ''
            config_parser.set('Settings', 'sessions', self.sessions)
        else:
            self.sessions = config_parser.get('Settings', 'sessions')

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def config_save(self):

        self.language = self.combobox_lang.get_active_text()
        self.screenshots = self.combobox_screenshots.get_active_text()
        self.game_width = self.entry_game_width.get_text()
        self.game_height = self.entry_game_height.get_text()
        self.menu_width = self.entry_menu_width.get_text()
        self.menu_height = self.entry_menu_height.get_text()
        self.movies_width = self.entry_movies_width.get_text()
        self.movies_height = self.entry_movies_height.get_text()
        self.failure_width = self.entry_failure_width.get_text()
        self.failure_height = self.entry_failure_height.get_text()
        self.msensitivity = int(self.adj_msensitivity.get_value())
        self.censorship = self.switch_censorship.get_active()

        self.speed = int(self.adj_speed.get_value())
        self.nointro = self.switch_nointro.get_active()
        self.smooth = self.switch_smooth.get_active()
        self.nosound = self.switch_nosound.get_active()
        self.sessions = self.entry_sessions.get_text()

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        config_parser.set('Settings', 'language', self.language)
        config_parser.set('Settings', 'screenshots', self.screenshots)
        config_parser.set('Settings', 'game_width', self.game_width)
        config_parser.set('Settings', 'game_height', self.game_height)
        config_parser.set('Settings', 'menu_width', self.menu_width)
        config_parser.set('Settings', 'menu_height', self.menu_height)
        config_parser.set('Settings', 'movies_width', self.movies_width)
        config_parser.set('Settings', 'movies_height', self.movies_height)
        config_parser.set('Settings', 'failure_width', self.failure_width)
        config_parser.set('Settings', 'failure_height', self.failure_height)
        config_parser.set('Settings', 'msensitivity', self.msensitivity)
        config_parser.set('Settings', 'censorship', self.censorship)

        config_parser.set('Settings', 'speed', self.speed)
        config_parser.set('Settings', 'nointro', self.nointro)
        config_parser.set('Settings', 'smooth', self.smooth)
        config_parser.set('Settings', 'nosound', self.nosound)
        config_parser.set('Settings', 'sessions', self.sessions)

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

        self.modify_keeperfx_cfg()
        self.modify_start_file()

    def modify_keeperfx_cfg(self):

        keeperfx_cfg = open(current_dir + '/game/keeperfx.cfg', 'w')

        keeperfx_cfg.write('; Path to the DK files. Usually leaving it as "./" will work.' + '\n')
        keeperfx_cfg.write('INSTALL_PATH=./' + '\n')
        keeperfx_cfg.write('; How many of the game files are on disk; irrelevant option.' + '\n')
        keeperfx_cfg.write('INSTALL_TYPE=MAX' + '\n')
        keeperfx_cfg.write('; Language definition; sets options for displaying texts.' + '\n')
        keeperfx_cfg.write('LANGUAGE=' + dict_lang[self.language] + '\n')
        keeperfx_cfg.write('; Keyboard definition; irrelevant.' + '\n')
        keeperfx_cfg.write('KEYBOARD=101' + '\n')
        keeperfx_cfg.write('; File format in which screenshots are written; BMP or HSI.' + '\n')
        keeperfx_cfg.write('SCREENSHOT=' + self.screenshots + '\n')

        failsafe_res = self.failure_width + 'x' + self.failure_height + 'x32'
        movies_res = self.movies_width + 'x' + self.movies_height + 'x32'
        menu_res = self.menu_width + 'x' + self.menu_height + 'x32'
        keeperfx_cfg.write('; Three frontend resolutions: failsafe, movies and menu resolution.' + '\n')
        keeperfx_cfg.write('FRONTEND_RES=' + failsafe_res + ' ' + movies_res + \
        ' ' + menu_res + '\n')

        game_res = self.game_width + 'x' + self.game_height + 'x32'
        keeperfx_cfg.write('; Original DK resolutions were FRONTEND_RES=320x200x8 320x200x8 640x480x8\n; List of in-game resolutions. ALT+R will switch between them.' + '\n')
        keeperfx_cfg.write('INGAME_RES=' + game_res + '\n')

        keeperfx_cfg.write(';Original DK resolutions were INGAME_RES=320x200x8 640x400x8\n; Mouse pointer movement speed; 100 percent means normal OS speed' + '\n')
        keeperfx_cfg.write('POINTER_SENSITIVITY=' + str(self.msensitivity) + '\n')

        if self.censorship:
            censorship = 'ON'
        else:
            censorship = 'OFF'
        keeperfx_cfg.write('; Censorship - originally was ON only if language is german.' + '\n')
        keeperfx_cfg.write('CENSORSHIP=' + censorship + '\n')

        keeperfx_cfg.close()

    def modify_start_file(self):

        parameters_list = []

        parameters_list.append('-nocd')

        if self.speed != 20:
            parameters_list.append('-fps ' + str(int(self.speed)))

        if self.nointro:
            parameters_list.append('-nointro')

        if self.smooth:
             parameters_list.append('-vidsmooth')

        if self.nosound:
            parameters_list.append('-nosound')

        if self.sessions != '':
            if ' ' in self.sessions:
                sessions_list = self.sessions.split(' ')
                sessions_string = ':5555;'.join(sessions_list)
            else:
                sessions_string = self.sessions

            parameters_list.append('-sessions ' + sessions_string  + ':5555')

        parameters_str = ' '.join(parameters_list)

        new_launch_command = 'python2 "$NEBULA_DIR/launcher_wine.py" ' + \
        'dungeon_keeper "keeperfx.exe' + ' ' + parameters_str + '"'

        start_file = open(current_dir + '/start.sh', 'r')
        start_file_content = start_file.readlines()
        start_file.close()

        for i in range(len(start_file_content)):
            if 'keeperfx.exe' in start_file_content[i]:
                start_file_content[i] = new_launch_command

        start_file = open(current_dir + '/start.sh', 'w')
        start_file.writelines(start_file_content)
        start_file.close()

    def cb_entries_res(self, entry):
        text = entry.get_text().strip()
        new_text = (''.join([i for i in text if i in '0123456789']))
        entry.set_text(new_text)

    def cb_button_save(self, button):
        self.config_save()
        Gtk.main_quit()

    def quit_app(self, window, event):
        Gtk.main_quit()

def main():
    import sys
    app = GUI(sys.argv[1])
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
