#!/usr/bin/env python2
# -*- Mode: Python; coding: utf-8 -*-

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import ConfigParser
import gettext
import imp

nebula_dir = os.getenv('NEBULA_DIR')

modules_dir = nebula_dir + '/modules'
set_visuals = imp.load_source('set_visuals', modules_dir + '/set_visuals.py')

gettext.bindtextdomain('games_nebula', nebula_dir + '/locale')
gettext.textdomain('games_nebula')
_ = gettext.gettext

current_dir = sys.path[0]
game_dir = current_dir + '/game'

class GUI:

    def __init__(self):
        self.config_load()
        self.create_main_window()

    def config_load(self):

        config_file = game_dir + '/corsairs.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('GENERAL'):
            self.lang = 'English'

            config_parser.add_section('LANGUAGE')
            config_parser.set('GENERAL', 'LANGUAGE', self.lang)

            new_config_file = open(config_file, 'w')
            config_parser.write(new_config_file)
            new_config_file.close()

        else:
            self.lang = config_parser.get('GENERAL', 'LANGUAGE')

    def config_save(self):

        config_file = game_dir + '/corsairs.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        config_parser.set('GENERAL', 'LANGUAGE', self.lang)

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Corsairs Gold"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            )
        self.main_window.connect('delete-event', self.quit_app)

        grid = Gtk.Grid(
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            row_spacing = 10,
            column_spacing = 10,
            column_homogeneous = True,
            )

        label_lang = Gtk.Label(
            label = _("Language:")
            )

        lang_list = ['Dutch', 'English', 'German', 'French', 'Italian', 'Polish',
                    'Portuguese', 'Spanish']

        combobox_lang = Gtk.ComboBoxText()
        index = 1
        for i in range(len(lang_list)):
            combobox_lang.append_text(lang_list[i])
            if self.lang == lang_list[i]:
                index = i
        combobox_lang.set_active(index)
        combobox_lang.connect('changed', self.cb_combobox_lang)

        button_save = Gtk.Button(
            label = _("Save and quit")
            )
        button_save.connect('clicked', self.cb_button_save)

        grid.attach(label_lang, 0, 0, 1, 1)
        grid.attach(combobox_lang, 1, 0, 1, 1)
        grid.attach(button_save, 0, 1, 2, 1)

        self.main_window.add(grid)

        self.main_window.show_all()

    def cb_combobox_lang(self, combobox):
        self.lang = combobox.get_active_text()

    def cb_button_save(self, button):
        self.config_save()
        Gtk.main_quit()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
