#!/usr/bin/env python2
# -*- Mode: Python; coding: utf-8 -*-

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import ConfigParser
import gettext
import stat
import imp

nebula_dir = os.getenv('NEBULA_DIR')

modules_dir = nebula_dir + '/modules'
set_visuals = imp.load_source('set_visuals', modules_dir + '/set_visuals.py')

gettext.bindtextdomain('games_nebula', nebula_dir + '/locale')
gettext.textdomain('games_nebula')
_ = gettext.gettext

wineloader = os.getenv('WINELOADER')
current_dir = sys.path[0]
config_file_path = current_dir + '/game/Larry.ini'

class GUI:

    def __init__(self):
        self.config_load()
        self.create_main_window()

    def config_load(self):
        config_file = open(config_file_path, 'r')
        config_content = config_file.readlines()
        config_file.close()

        for line in config_content:
            if '\tResolution' in line:
                self.custom_width = line.split(' ')[1]
                self.custom_height = line.split(' ')[2].strip('\r\n')

    def config_save(self):

        config_file = open(config_file_path, 'r')
        config_content = config_file.readlines()
        config_file.close()

        config_file = open(config_file_path, 'w')

        for line in config_content:
            if '\tResolution' in line:
                config_file.write('\tResolution ' + self.custom_width + ' ' + self.custom_height + '\r\n')
            else:
                config_file.write(line)

        config_file.close()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Leisure Suit Larry: Magna Cum Laude: Uncut and Uncensored!"),
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

        label_custom_res = Gtk.Label(
            label = _("Custom resolution:")
            )

        self.entry_custom_width = Gtk.Entry(
            placeholder_text = _("Width"),
            max_length = 4,
            xalign = 0.5,
            text = self.custom_width
            )
        self.entry_custom_width.connect('changed', self.cb_entry_custom_width)

        self.entry_custom_height = Gtk.Entry(
            placeholder_text = _("Height"),
            max_length = 4,
            xalign = 0.5,
            text = self.custom_height
            )
        self.entry_custom_height.connect('changed', self.cb_entry_custom_height)

        button_more = Gtk.Button(
            label = _("More settings"),
            )
        button_more.connect('clicked', self.cb_button_more)

        button_save = Gtk.Button(
            label = _("Save and quit"),
            )
        button_save.connect('clicked', self.cb_button_save)

        grid.attach(label_custom_res, 0, 0, 2, 1)
        grid.attach(self.entry_custom_width, 0, 1, 1, 1)
        grid.attach(self.entry_custom_height, 1, 1, 1, 1)
        grid.attach(button_more, 0, 2, 2, 1)
        grid.attach(button_save, 0, 3, 2, 1)

        self.main_window.add(grid)
        self.main_window.show_all()

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

    def cb_button_more(self, button):

        self.main_window.hide()

        while Gtk.events_pending():
            Gtk.main_iteration()

        os.system('cd "' + current_dir + '/game" && ' + wineloader + ' "./ConfigUtil.exe"')

        self.config_load()
        self.entry_custom_width.set_text(self.custom_width)
        self.entry_custom_height.set_text(self.custom_height)

        self.main_window.show()

    def cb_button_save(self, button):

        if (self.custom_width == '') or (self.custom_height == ''):
            message_dialog = Gtk.MessageDialog(
                self.main_window,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK,
                _("Error")
                )
            message_dialog.format_secondary_text(_("You have to set width and height."))
            content_area = message_dialog.get_content_area()
            content_area.set_property('margin-left', 10)
            content_area.set_property('margin-right', 10)
            content_area.set_property('margin-top', 10)
            content_area.set_property('margin-bottom', 10)
            message_dialog.run()
            message_dialog.destroy()

            return

        self.config_save()
        Gtk.main_quit()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
