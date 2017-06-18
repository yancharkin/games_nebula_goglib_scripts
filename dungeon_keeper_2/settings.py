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

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Dungeon Keeper 2"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            )
        self.main_window.connect('delete-event', self.quit_app)

        box_main = Gtk.Box(
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            spacing = 10,
            orientation = Gtk.Orientation.VERTICAL
            )

        frame_rendering = Gtk.Frame(
            label = _("Rendering"),
            label_xalign = 0.5,
            )

        box_rendering = Gtk.Box(
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            spacing = 10,
            orientation = Gtk.Orientation.VERTICAL
            )

        radiobutton_dk2dx = Gtk.RadioButton(
            label = _("GOG HW Patch"),
            name = 'DKII-DX.exe'
            )

        radiobutton_dk2 = Gtk.RadioButton(
            label = _("Hardware rendering"),
            name = 'DKII.EXE'
            )
        radiobutton_dk2.join_group(radiobutton_dk2dx)

        radiobutton_dk2soft = Gtk.RadioButton(
            label = _("Software rendering"),
            name = 'DKII_SOFT.EXE'
            )
        radiobutton_dk2soft.join_group(radiobutton_dk2dx)

        box_rendering.pack_start(radiobutton_dk2dx, True, True, 0)
        box_rendering.pack_start(radiobutton_dk2, True, True, 0)
        box_rendering.pack_start(radiobutton_dk2soft, True, True, 0)
        frame_rendering.add(box_rendering)

        box_res = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL,
            spacing = 10
            )

        label_res = Gtk.Label(
            label = _("Resolution")
            )

        entry_width = Gtk.Entry(
            placeholder_text = _("Width"),
            xalign = 0.5,
            max_length = 4,
            text = self.width,
            name = 'width'
            )
        entry_width.connect('changed', self.cb_entries_res)

        entry_height = Gtk.Entry(
            placeholder_text = _("Height"),
            xalign = 0.5,
            max_length = 4,
            text = self.height,
            name = 'height'
            )
        entry_height.connect('changed', self.cb_entries_res)

        box_res.pack_start(label_res, True, True, 0)
        box_res.pack_start(entry_width, True, True, 0)
        box_res.pack_start(entry_height, True, True, 0)

        button_save = Gtk.Button(
            label = _("Save and quit")
            )
        button_save.connect('clicked', self.cb_button_save)

        box_main.pack_start(frame_rendering, True, True, 0)
        box_main.pack_start(box_res, True, True, 0)
        box_main.pack_start(button_save, True, True, 0)

        for radiobutton in box_rendering.get_children():
            if radiobutton.get_name() == self.exe:
                radiobutton.set_active(True)

        radiobutton_dk2dx.connect('clicked', self.cb_radiobuttons)
        radiobutton_dk2.connect('clicked', self.cb_radiobuttons)
        radiobutton_dk2soft.connect('clicked', self.cb_radiobuttons)

        self.main_window.add(box_main)
        self.main_window.show_all()

    def config_load(self):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('Settings'):
            config_parser.add_section('Settings')

        if not config_parser.has_option('Settings', 'exe'):
            self.exe = 'DKII-DX.exe'
            config_parser.set('Settings', 'exe', self.exe)
        else:
            self.exe = config_parser.get('Settings', 'exe')

        if not config_parser.has_option('Settings', 'width'):
            self.width = 640
            config_parser.set('Settings', 'width', self.width)
        else:
            self.width = config_parser.get('Settings', 'width')

        if not config_parser.has_option('Settings', 'height'):
            self.height = 480
            config_parser.set('Settings', 'height', self.height)
        else:
            self.height = config_parser.get('Settings', 'height')

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def modify_start_file(self):

        new_launch_command = 'python2 "$NEBULA_DIR/launcher_wine.py" dungeon_keeper_2 ' + self.exe

        start_file = open(current_dir + '/start.sh', 'r')
        start_file_content = start_file.readlines()
        start_file.close()

        for i in range(len(start_file_content)):
            if '.EXE' in start_file_content[i]:
                start_file_content[i] = new_launch_command

        start_file = open(current_dir + '/start.sh', 'w')
        start_file.writelines(start_file_content)
        start_file.close()

    def modify_registry(self):

        regedit_command = '"$WINELOADER" reg add ' + \
        '"HKEY_CURRENT_USER\Software\Bullfrog Productions Ltd\Dungeon Keeper II\Configuration\Video" /v ' + \
        '"Screen Width" /t REG_DWORD /d ' + str(hex(int(self.width))) + ' /f && ' + \
        '"$WINELOADER" reg add ' + \
        '"HKEY_CURRENT_USER\Software\Bullfrog Productions Ltd\Dungeon Keeper II\Configuration\Video" /v ' + \
        '"Screen Height" /t REG_DWORD /d ' + str(hex(int(self.height))) + ' /f'

        os.system(regedit_command)

    def cb_radiobuttons(self, radiobutton):
        self.exe = radiobutton.get_name()

    def cb_entries_res(self, entry):
        text = entry.get_text().strip()
        new_text = (''.join([i for i in text if i in '0123456789']))
        entry.set_text(new_text)

        if entry.get_name() == 'width':
            self.width = new_text
        elif entry.get_name() == 'height':
            self.height = new_text

    def cb_button_save(self, button):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        config_parser.set('Settings', 'exe', self.exe)
        config_parser.set('Settings', 'width', self.width)
        config_parser.set('Settings', 'height', self.height)

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

        self.modify_start_file()
        self.modify_registry()
        Gtk.main_quit()

    def quit_app(self, window, event):
        Gtk.main_quit()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
