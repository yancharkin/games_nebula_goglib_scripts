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

current_dir = sys.path[0]
config_file_dir = current_dir + '/game/Deus Ex - Invisible War'
config_file_path = config_file_dir + '/user.ini'

class GUI:

    def __init__(self):
        self.config_load()
        self.create_main_window()

    def config_load(self):

        if os.path.exists(config_file_path):
            config_file = open(config_file_path, 'r')
            config_content = config_file.readlines()
            config_file.close()

            for line in config_content:
                if 'FullscreenViewportX' in line:
                    self.custom_width = line.split('=')[1].strip('\r\n')
                if 'FullscreenViewportY' in line:
                    self.custom_height = line.split('=')[1].strip('\r\n')
        else:

            message_dialog = Gtk.MessageDialog(
                None,
                0,
                Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK,
                _("Launch the game at least once before using this utility.")
                )
            content_area = message_dialog.get_content_area()
            content_area.set_property('margin-left', 10)
            content_area.set_property('margin-right', 10)
            content_area.set_property('margin-top', 10)
            content_area.set_property('margin-bottom', 10)
            message_dialog.run()
            message_dialog.destroy()
            sys.exit()

    def config_save(self):

        if os.path.exists(config_file_path):
            config_file = open(config_file_path, 'r')
            config_content = config_file.readlines()
            config_file.close()

            config_file = open(config_file_path, 'w')

            for line in config_content:
                if 'FullscreenViewportY' in line:
                    config_file.write('FullscreenViewportY=' + self.custom_height + '\r\n')
                elif 'FullscreenViewportX' in line:
                    config_file.write('FullscreenViewportX=' + self.custom_width + '\r\n')
                else:
                    config_file.write(line)

            config_file.close()

        else:
            self.custom_width = '1024'
            self.custom_height = '768'

            config_file = open(config_file_path, 'w')
            config_file.write('[WinDrv.WindowsClient]')
            config_file.write('FullscreenViewportY=' + self.custom_height)
            config_file.write('FullscreenViewportX=' + self.custom_width)
            config_file.close()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Deus Ex 2: Invisible War"),
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

        entry_custom_width = Gtk.Entry(
            placeholder_text = _("Width"),
            max_length = 4,
            xalign = 0.5,
            text = self.custom_width
            )
        entry_custom_width.connect('changed', self.cb_entry_custom_width)

        entry_custom_height = Gtk.Entry(
            placeholder_text = _("Height"),
            max_length = 4,
            xalign = 0.5,
            text = self.custom_height
            )
        entry_custom_height.connect('changed', self.cb_entry_custom_height)

        st = os.stat(config_file_path)

        writable = bool(st.st_mode & stat.S_IWUSR)
        protected = not writable

        self.button_set = Gtk.Button(
            label = _("Set"),
            sensitive = writable
            )
        self.button_set.connect('clicked', self.cb_button_set)

        checkbutton = Gtk.CheckButton(
            label = _("Protect settings file from overwriting (root)"),
            active = protected
            )
        checkbutton.connect('clicked', self.cb_checkbutton)

        grid.attach(label_custom_res, 0, 0, 2, 1)
        grid.attach(entry_custom_width, 0, 1, 1, 1)
        grid.attach(entry_custom_height, 1, 1, 1, 1)
        grid.attach(self.button_set, 0, 2, 2, 1)
        grid.attach(checkbutton, 0, 3, 2, 1)

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

    def cb_checkbutton(self, button):

        user = os.getenv('USER')

        if button.get_active():

            os.system('chmod -w "' + config_file_path +
            '" && gksudo chown root:root "' + config_file_path + '"')

            self.button_set.set_sensitive(False)
        else:
            os.system('gksudo chown ' + user + ':' + user + ' "' + config_file_path +
            '" && chmod +w "' + config_file_path + '"')

            self.button_set.set_sensitive(True)

    def cb_button_set(self, button):

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

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
