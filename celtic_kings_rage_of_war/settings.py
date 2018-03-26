# -*- Mode: Python; coding: utf-8; -*-

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import gettext
import imp

try:
    from ConfigParser import ConfigParser as ConfigParser
except:
    from configparser import ConfigParser as ConfigParser

nebula_dir = os.getenv('NEBULA_DIR')
app_icon = GdkPixbuf.Pixbuf.new_from_file(nebula_dir + '/images/icon.png')

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
        config_parser = ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('Settings'):
            self.language = 'English'
            self.custom_res = False
            self.custom_width = 1024
            self.custom_height = 768

            config_parser.add_section('Settings')
            config_parser.set('Settings', 'custom_width', str(self.custom_width))
            config_parser.set('Settings', 'custom_height', str(self.custom_height))

            new_config_file = open(config_file, 'w')
            config_parser.write(new_config_file)
            new_config_file.close()

        else:

            self.custom_width = config_parser.get('Settings', 'custom_width')
            self.custom_height = config_parser.get('Settings', 'custom_height')

    def config_save(self):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        config_parser.set('Settings', 'custom_width', str(self.custom_width))
        config_parser.set('Settings', 'custom_height', str(self.custom_height))

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Celtic Kings: Rage of War"),
            icon = app_icon,
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

        self.label_info = Gtk.Label(
            label = _("Minimum width = 1024, maximum width = 1600,\n" +
                    "minimum height = 768, maximum height = 1200\n" +
                    "Other values may not work or work incorrectly.")
        )

        self.button_save = Gtk.Button(
            label = _("Save and quit")
        )
        self.button_save.connect('clicked', self.cb_button_save)

        self.grid.attach(self.entry_custom_width, 0, 0, 1, 1)
        self.grid.attach(self.entry_custom_height, 1, 0, 1, 1)
        self.grid.attach(self.label_info, 0, 1, 2, 1)
        self.grid.attach(self.button_save, 0, 2, 2, 1)

        self.main_window.add(self.grid)

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

    def cb_button_save(self, button):

        width = int(self.custom_width)
        height = int(self.custom_height)

        if (width > 1600) or (height > 1200):
            self.simple_message(
                    Gtk.MessageType.ERROR,
                    _("Error"),
                    _("Maximum resolution exceeded (1600x1200).")
            )

            return

        if (len(self.custom_height) < 3) or (len(self.custom_width) < 4):

            self.simple_message(
                    Gtk.MessageType.ERROR,
                    _("Error"),
                    _("Incorrect input value")
            )

            return

        elif len(self.custom_height) == 3:
            width_offset = 0x11e466
            height_offset = 0x11e475
            resolution_id = '1'
        elif len(self.custom_height) == 4:
            width_offset = 0x11e483
            height_offset = 0x11e492
            resolution_id = '2'

        if height < 768:
            self.simple_message(
                    Gtk.MessageType.WARNING,
                    _("Warning"),
                    _("You're set resolution that lower than minimum.\n" + \
                    "It may work incorrectly.")
            )

        settings_dat = current_dir + '/game/data.pak'

        if not os.path.exists(settings_dat + '.bak'):
            os.system('cp ' + settings_dat + ' ' + settings_dat + '.bak')

        settings_file = open(settings_dat, 'r+b')
        settings_file.seek(width_offset)
        settings_file.write(str(width))
        settings_file.seek(height_offset)
        settings_file.write(str(height))
        settings_file.close()

        vx_settings_path = current_dir + '/game/vxSettings.ini'
        vx_settings_file = open(vx_settings_path, 'r')
        vx_settings = vx_settings_file.readlines()
        vx_settings_file.close()

        if len(vx_settings) <= 2:
            vx_settings_file = open(vx_settings_path, 'a')
            vx_settings_file.write('\n')
            vx_settings_file.write('[Options]\n')
            vx_settings_file.write('ReverseSpeakers=0\n')
            vx_settings_file.write('NoObjectAnimations=0\n')
            vx_settings_file.write('NoWaterAnimation=0\n')
            vx_settings_file.write('Music=1\n')
            vx_settings_file.write('SoundFX=1\n')
            vx_settings_file.write('NatureSounds=1\n')
            vx_settings_file.write('Speech=1\n')
            vx_settings_file.write('Conversations=1\n')
            vx_settings_file.write('GameSpeed=14\n')
            vx_settings_file.write('ScrollSpeed=50\n')
            vx_settings_file.write('SoundVolume=50\n')
            vx_settings_file.write('MusicVolume=50\n')
            vx_settings_file.write('SpeechVolume=50\n')
            vx_settings_file.write('Resolution=' + resolution_id + '\n')
        else:
            vx_settings_file = open(vx_settings_path, 'w')
            for i in range(len(vx_settings)):
                if 'Resolution=' in vx_settings[i]:
                    vx_settings[i] = 'Resolution=' + resolution_id
                vx_settings_file.write(vx_settings[i])

        vx_settings_file.close()

        self.config_save()
        Gtk.main_quit()

    def simple_message(self, message_type, text_1, text_2):

        message_dialog = Gtk.MessageDialog(
            None,
            0,
            message_type,
            Gtk.ButtonsType.OK,
            text_1
        )

        message_dialog.format_secondary_text(text_2)
        content_area = message_dialog.get_content_area()
        content_area.set_property('margin-left', 10)
        content_area.set_property('margin-right', 10)
        content_area.set_property('margin-top', 10)
        content_area.set_property('margin-bottom', 10)
        content_area_label = content_area.get_children()[0].get_children()[0].get_children()[1]
        content_area_label.set_property('justify', Gtk.Justification.CENTER)

        self.main_window.hide()

        while Gtk.events_pending():
            Gtk.main_iteration()

        message_dialog.run()
        message_dialog.destroy()

        self.main_window.show()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
