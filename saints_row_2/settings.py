#!/usr/bin/env python2
# -*- Mode: Python; coding: utf-8; indent-tabs-install_mode: t; c-basic-offset: 4; tab-custom_width: 4 -*-

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import ConfigParser
import gettext

current_dir = sys.path[0]

dict_lang = {
    'English':'forcelang_en',
    'Deutsch':'forcelang_de',
    'Français':'forcelang_fr',
    'Español':'forcelang_es',
    'Italiano':'forcelang_it',
    'Nederlands':'forcelang_nl',
    'Svenska':'forcelang_se',
    'Dansk':'forcelang_dk',
    'Polski':'forcelang_pl',
    'Čeština':'forcelang_cz',
    'Русский':'forcelang_ru',
    '中文':'forcelang_ch',
    '日本語':'forcelang_jp'
    }

class GUI:

    def __init__(self, nebula_dir):
        
        gettext.bindtextdomain('games_nebula', nebula_dir + '/locale')
        gettext.textdomain('games_nebula')
        self._ = gettext.gettext

        self.get_global_settings()
        self.config_load()
        self.create_main_window()

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
            self.language = 'English'
            self.custom_res = False
            self.custom_width = 1024
            self.custom_height = 768

            config_parser.add_section('Settings')
            config_parser.set('Settings', 'language', self.language)
            config_parser.set('Settings', 'custom_res', self.custom_res)
            config_parser.set('Settings', 'custom_width', self.custom_width)
            config_parser.set('Settings', 'custom_height', self.custom_height)

            new_config_file = open(config_file, 'w')
            config_parser.write(new_config_file)
            new_config_file.close()

        else:
            self.language = config_parser.get('Settings', 'language')
            self.custom_res = config_parser.getboolean('Settings', 'custom_res')
            self.custom_width = config_parser.get('Settings', 'custom_width')
            self.custom_height = config_parser.get('Settings', 'custom_height')

    def config_save(self):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        config_parser.set('Settings', 'language', self.language)
        config_parser.set('Settings', 'custom_res', self.custom_res)
        config_parser.set('Settings', 'custom_width', self.custom_width)
        config_parser.set('Settings', 'custom_height', self.custom_height)

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

        self.modify_start_file()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = self._("Saints Row 2"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            )
        self.main_window.connect('delete-event', self.quit_app)

        self.grid = Gtk.Grid(
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            row_spacing = 10,
            column_spacing = 10,
            column_homogeneous = True,
            )

        self.label_language = Gtk.Label(
            label = self._("Language")
            )

        self.combobox_language = Gtk.ComboBoxText()
        i = 0
        for lang in sorted(dict_lang):
            self.combobox_language.append_text(lang)
            if lang == self.language:
                active_lang = i
            i += 1

        self.combobox_language.set_active(active_lang)
        self.combobox_language.connect('changed', self.cb_combobox_language)

        self.checkbutton_custom_res = Gtk.CheckButton(
            label = self._("Custom resolution"),
            active = self.custom_res,
            )
        self.checkbutton_custom_res.connect('toggled', self.cb_checkbutton_custom_res)

        self.entry_custom_width = Gtk.Entry(
            placeholder_text = self._("Width"),
            no_show_all = True,
            max_length = 4,
            xalign = 0.5,
            text = self.custom_width
            )
        self.entry_custom_width.set_visible(self.custom_res)
        self.entry_custom_width.connect('changed', self.cb_entry_custom_width)

        self.entry_custom_height = Gtk.Entry(
            placeholder_text = self._("Height"),
            no_show_all = True,
            max_length = 4,
            xalign = 0.5,
            text = self.custom_height
            )
        self.entry_custom_height.set_visible(self.custom_res)
        self.entry_custom_height.connect('changed', self.cb_entry_custom_height)

        self.button_save = Gtk.Button(
            label = self._("Save and quit")
            )
        self.button_save.connect('clicked', self.cb_button_save)

        self.button_quit = Gtk.Button(
            label = self._("Quit without saving")
            )
        self.button_quit.connect('clicked', Gtk.main_quit)

        self.grid.attach(self.label_language, 0, 0, 1, 1)
        self.grid.attach(self.combobox_language, 1, 0, 1, 1)
        self.grid.attach(self.checkbutton_custom_res, 0, 1, 2, 1)
        self.grid.attach(self.entry_custom_width, 0, 2, 1, 1)
        self.grid.attach(self.entry_custom_height, 1, 2, 1, 1)
        self.grid.attach(self.button_save, 0, 3, 2, 1)
        self.grid.attach(self.button_quit, 0, 4, 2, 1)

        self.main_window.add(self.grid)

        self.main_window.show_all()

    def cb_combobox_language(self, combobox):
        self.language = combobox.get_active_text()

    def cb_checkbutton_custom_res(self, button):
        self.custom_res = button.get_active()
        self.entry_custom_width.set_visible(self.custom_res)
        self.entry_custom_height.set_visible(self.custom_res)

    def cb_entry_custom_width(self, entry):
        text = entry.get_text().strip()
        new_text = (''.join([i for i in text if i in '0123456789']))
        entry.set_text(new_text)
        self.custom_width = new_text

    def cb_entry_custom_height(self, entry):
        text = entry.get_text().strip()
        new_text = (''.join([i for i in text if i in '0123456789']))
        entry.set_text(new_text)
        self.custom_height = new_text

    def cb_button_save(self, button):
        self.config_save()
        self.modify_settings_dat()
        Gtk.main_quit()

    def modify_start_file(self):

        new_launch_command = 'python $NEBULA_DIR/launcher_wine.py ' + \
        'saints_row_2 "SR2_pc.exe' + ' ' + dict_lang[self.language] + '"'

        start_file = open(current_dir + '/start.sh', 'r')
        start_file_content = start_file.readlines()
        start_file.close()

        for i in range(len(start_file_content)):
            if 'SR2_pc' in start_file_content[i]:
                start_file_content[i] = new_launch_command

        start_file = open(current_dir + '/start.sh', 'w')
        start_file.writelines(start_file_content)
        start_file.close()

    def modify_settings_dat(self):

        settings_dat = current_dir + '/game/settings.dat'

        if self.custom_res:
            width = int(self.custom_width)
            height = int(self.custom_height)
        else:
            width = 1024
            height = 768

        width_offset1 = 0x3c
        width_offset2 = 0x3d
        height_offset1 = 0x40
        height_offset2 = 0x41

        hex_width = list('0' + hex(width).split('x')[1])
        width_offset1_value = hex_width[2] + hex_width[3]
        width_offset2_value = hex_width[0] + hex_width[1]

        hex_height = list('0' + hex(height).split('x')[1])
        height_offset1_value = hex_height[2] + hex_height[3]
        height_offset2_value = hex_height[0] + hex_height[1]

        settings_file = open(settings_dat, 'r+b')
        settings_file.seek(width_offset1)
        settings_file.write(chr(int(width_offset1_value, 16)))
        settings_file.seek(width_offset2)
        settings_file.write(chr(int(width_offset2_value, 16)))
        settings_file.seek(height_offset1)
        settings_file.write(chr(int(height_offset1_value, 16)))
        settings_file.seek(height_offset2)
        settings_file.write(chr(int(height_offset2_value, 16)))
        settings_file.close()

def main():
    import sys
    app = GUI(sys.argv[1])
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
