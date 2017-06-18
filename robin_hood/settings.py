#!/usr/bin/env python2
# -*- Mode: Python; coding: utf-8; -*-

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

class GUI:

    def __init__(self):
        self.config_load()
        self.create_main_window()

    def config_load(self):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('Settings'):
            config_parser.add_section('Settings')

        if not config_parser.has_option('Settings', 'mode'):
            self.mode = 'windowed1'
            config_parser.set('Settings', 'mode', self.mode)
        else:
            self.mode = config_parser.get('Settings', 'mode')

        if not config_parser.has_option('Settings', 'monitor_index'):
            self.monitor_index = 0
            config_parser.set('Settings', 'monitor_index', self.monitor_index)
        else:
            self.monitor_index = config_parser.getint('Settings', 'monitor_index')

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def config_save(self):

        if self.mode == 'fullscreen':
            new_launch_command = '"$DIR/game/robin"'
        elif self.mode == 'windowed1':
            new_launch_command = '"$DIR/game/robin" -NOFULLSCREEN'
        elif self.mode == 'windowed2':
            new_launch_command = 'SDL_VIDEO_X11_XRANDR=0 SDL_VIDEO_FULLSCREEN_HEAD=' + \
            str(self.monitor_index) + ' "$DIR/game/robin"'

        start_file = open(current_dir + '/start_gn.sh', 'r')
        start_file_content = start_file.readlines()
        start_file.close()

        for i in range(len(start_file_content)):
            if 'robin' in start_file_content[i]:
                start_file_content[i] = new_launch_command

        start_file = open(current_dir + '/start_gn.sh', 'w')
        start_file.writelines(start_file_content)
        start_file.close()

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        config_parser.set('Settings', 'mode', self.mode)
        config_parser.set('Settings', 'monitor_index', self.monitor_index)

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Robin Hood: The Legend of Sherwood"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 360,
            )
        self.main_window.connect('delete-event', self.quit_app)

        label = Gtk.Label(
            halign = Gtk.Align.FILL,
            label = _("Mode:"),
            )

        radiobutton_fullscreen = Gtk.RadioButton(
            label = _("Fullscreen"),
            name = 'fullscreen'
            )
        radiobutton_fullscreen.connect('toggled', self.cb_radiobuttons)

        radiobutton_windowed1 = Gtk.RadioButton(
            label = _("Windowed 1"),
            name = 'windowed1'
            )
        radiobutton_windowed1.connect('toggled', self.cb_radiobuttons)
        radiobutton_windowed1.join_group(radiobutton_fullscreen)

        radiobutton_windowed2 = Gtk.RadioButton(
            label = _("Windowed 2"),
            name = 'windowed2'
            )
        radiobutton_windowed2.connect('toggled', self.cb_radiobuttons)
        radiobutton_windowed2.join_group(radiobutton_fullscreen)

        self.label_monitor = Gtk.Label(
            label = _("Monitor index:"),
            halign = Gtk.Align.FILL,
            no_show_all = True
            )

        self.combobox_monitor = Gtk.ComboBoxText(
            no_show_all = True
            )

        screen = Gdk.Screen.get_default()
        self.n_monitors = screen.get_n_monitors()

        if self.n_monitors > 1:
            for i in range(self.n_monitors):
                self.combobox_monitor.append_text(str(i))
        else:
            self.combobox_monitor.append_text('0')
            self.monitor_index = 0

        self.combobox_monitor.set_active(self.monitor_index)
        self.combobox_monitor.connect('changed', self.cb_combobox_monitor)

        box1 = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 10
            )

        box1.pack_start(self.label_monitor, True, True, 0)
        box1.pack_start(self.combobox_monitor, True, True, 0)

        if self.mode == 'fullscreen':
            radiobutton_fullscreen.set_active(True)
        elif self.mode == 'windowed1':
            radiobutton_windowed1.set_active(True)
        elif self.mode == 'windowed2':
            radiobutton_windowed2.set_active(True)

        button_save = Gtk.Button(
            label = _("Save and quit"),
            )
        button_save.connect('clicked', self.cb_button_save)

        box2 = Gtk.Box(
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            spacing = 10,
            orientation = Gtk.Orientation.VERTICAL
            )

        box2.pack_start(label, True, True, 0)
        box2.pack_start(radiobutton_fullscreen, True, True, 0)
        box2.pack_start(radiobutton_windowed1, True, True, 0)
        box2.pack_start(radiobutton_windowed2, True, True, 0)
        box2.pack_start(box1, True, True, 0)
        box2.pack_start(button_save, True, True, 0)

        self.main_window.add(box2)
        self.main_window.show_all()

    def cb_button_save(self, button):
        self.config_save()
        Gtk.main_quit()

    def cb_radiobuttons(self, radiobutton):
        if radiobutton.get_active():
            self.mode = radiobutton.get_name()

            if (radiobutton.get_name() == 'windowed2') and (self.n_monitors > 1):
                self.label_monitor.set_visible(True)
                self.combobox_monitor.set_visible(True)
            else:
                self.label_monitor.set_visible(False)
                self.combobox_monitor.set_visible(False)

    def cb_combobox_monitor(self, combobox):
        self.monitor_index = combobox.get_active()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
