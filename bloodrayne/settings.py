#!/usr/bin/env python2
# -*- Mode: Python; coding: utf-8; -*-

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
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
video_dir = current_dir + '/game/video'
video_dir_bak = video_dir + '/bak'

class GUI:

    def __init__(self):
        self.config_load()
        self.create_main_window()

    def create_main_window(self):

        main_window = Gtk.Window(
            title = _("Blood Rayne"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            )
        main_window.connect('delete-event', self.quit_app)

        grid = Gtk.Grid(
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            row_spacing = 10,
            column_spacing = 10,
            )

        self.label_res = Gtk.Label(
            label = _("Resolution"),
            halign = Gtk.Align.START
            )

        self.entry_width = Gtk.Entry(
            placeholder_text = _("Width"),
            xalign = 0.5,
            max_length = 4,
            text = self.width,
            name = 'width'
            )
        self.entry_width.connect('changed', self.cb_entries_res)

        self.entry_height = Gtk.Entry(
            placeholder_text = _("Height"),
            xalign = 0.5,
            max_length = 4,
            text = self.height,
            name = 'height'
            )
        self.entry_height.connect('changed', self.cb_entries_res)

        self.label_crop = Gtk.Label(
            label = _("Crop videos (FFmpeg)"),
            halign = Gtk.Align.START
            )

        self.combobox_crop = Gtk.ComboBoxText()
        self.combobox_crop.append_text(_("4:3 (no cropping)"))
        self.combobox_crop.append_text('16:9')
        self.combobox_crop.append_text('16:10')
        self.combobox_crop.set_active(self.crop)

        self.button_save = Gtk.Button(label=_("Save and quit"))
        self.button_save.connect('clicked', self.cb_button_save)

        self.progressbar = Gtk.ProgressBar(
            hexpand = True,
            show_text = True,
            text = _("Processing..."),
            pulse_step = 0.1,
            no_show_all = True
            )

        grid.attach(self.label_res, 0, 0, 1, 1)
        grid.attach(self.entry_width, 1, 0, 1, 1)
        grid.attach(self.entry_height, 2, 0, 1, 1)
        grid.attach(self.label_crop, 0, 1, 1, 1)
        grid.attach(self.combobox_crop, 1, 1, 2, 1)
        grid.attach(self.button_save, 0, 2, 3, 1)
        grid.attach(self.progressbar, 0, 3, 3, 1)

        main_window.add(grid)
        main_window.show_all()

    def config_load(self):

        config_file_path = current_dir + '/game/system/rayne.ini'
        config_file = open(config_file_path, 'r')
        config_file_content = config_file.readlines()
        config_file.close()

        if not os.path.exists(config_file_path) or \
                ('gamePIXY' not in ' '.join(config_file_content)) or \
                ('gamePIXX' not in ' '.join(config_file_content)):

            self.width = 640
            self.height = 480

            config_file_content = []
            config_file_content.append('[Graphics]')
            config_file_content.append('gamePIXY=480')
            config_file_content.append('gamePIXX=640')

            config_file = open(config_file_path, 'w')
            for line in config_file_content:
                config_file.write(line + '\r\n')
            config_file.close()

        else:
            for line in config_file_content:
                if 'gamePIXX' in line:
                    self.width = line.split('=')[1].strip('\r\n')
                if 'gamePIXY' in line:
                    self.height = line.split('=')[1].strip('\r\n')

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('Settings'):
            config_parser.add_section('Settings')

        if not config_parser.has_option('Settings', 'crop'):
            self.crop = 0
            config_parser.set('Settings', 'crop', self.crop)
        else:
            self.crop = config_parser.getint('Settings', 'crop')

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

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

        self.label_res.set_sensitive(False)
        self.label_crop.set_sensitive(False)
        self.entry_width.set_sensitive(False)
        self.entry_height.set_sensitive(False)
        self.combobox_crop.set_sensitive(False)
        self.button_save.set_visible(False)
        self.progressbar.set_visible(True)

        config_file_path = current_dir + '/game/system/rayne.ini'
        config_file = open(config_file_path, 'r')
        config_file_content = config_file.readlines()
        config_file.close()

        config_file_path = current_dir + '/game/system/rayne.ini'
        config_file = open(config_file_path, 'w')

        for line in config_file_content:
            if 'gamePIXX' in line:
                config_file.write('gamePIXX=' + self.width + '\r\n')
            elif 'gamePIXY' in line:
                config_file.write('gamePIXY=' + self.height + '\r\n')
            else:
                config_file.write(line)

        config_file.close()

        crop = self.combobox_crop.get_active()

        if crop != self.crop:

            self.crop = crop

            self.n_files = 0

            if crop == 0:
                if os.path.exists(video_dir_bak):
                    for file_name in os.listdir(video_dir):
                        if '.mpg' in file_name:
                            self.n_files += 1
                            os.system('rm ' + video_dir + '/' + file_name)
                    os.system('mv ' + video_dir_bak + '/* ' + video_dir)
                    os.system('rm -r ' + video_dir_bak)

                self.config_save_crop(self.crop)

            else:

                if not os.path.exists(video_dir_bak):
                    os.system('mkdir -p ' + video_dir_bak)
                    for file_name in os.listdir(video_dir):
                        if '.mpg' in file_name:
                            self.n_files += 1
                            os.system('mv ' + video_dir + '/' + file_name + ' ' + video_dir_bak)
                else:
                    for file_name in os.listdir(video_dir):
                        if '.mpg' in file_name:
                            self.n_files += 1
                            os.system('rm ' + video_dir + '/' + file_name)

                for file_name in os.listdir(video_dir_bak):
                    if '.mpg' in file_name:
                        self.crop_file(file_name, crop)
        else:

            Gtk.main_quit()

    def config_save_crop(self, crop):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        config_parser.set('Settings', 'crop', crop)

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

        Gtk.main_quit()

    def crop_file(self, file_name, crop):

        if crop == 1:
            region = '640:360:0:60'
        elif crop == 2:
            region = '640:400:0:40'

        command = ['ffmpeg', '-i', video_dir_bak + '/' + file_name, '-filter:v',
        'crop=' + region, '-q', '1', video_dir + '/' + file_name]

        self.pid, stdin, stdout, stderr = GLib.spawn_async(command,
                                    flags=GLib.SpawnFlags.SEARCH_PATH|GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                                    standard_output=True,
                                    standard_error=True)

        io = GLib.IOChannel(stdout)

        self.source_id_out = io.add_watch(GLib.IO_IN|GLib.IO_HUP,
                             self.watch_process,
                             'cropping_video',
                             priority=GLib.PRIORITY_HIGH)

    def watch_process(self, io, condition, process_name):

        if condition is GLib.IO_HUP:

            self.progressbar.pulse()

            self.n_files -= 1

            if self.n_files == 0:
                self.config_save_crop(self.crop)

            return False

        while Gtk.events_pending():
            Gtk.main_iteration_do(False)

        return True

    def quit_app(self, window, event):
        Gtk.main_quit()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
