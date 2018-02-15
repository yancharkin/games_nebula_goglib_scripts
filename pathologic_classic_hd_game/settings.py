import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import gettext
import imp

try:
    from ConfigParser import ConfigParser as ConfigParser
except:
    from configparser import ConfigParser as ConfigParser

nebula_dir = os.getenv('NEBULA_DIR')

modules_dir = nebula_dir + '/modules'
set_visuals = imp.load_source('set_visuals', modules_dir + '/set_visuals.py')

gettext.bindtextdomain('games_nebula', nebula_dir + '/locale')
gettext.textdomain('games_nebula')
_ = gettext.gettext

current_dir = sys.path[0]
install_dir = os.getenv('INSTALL_DIR')
game_dir = install_dir + '/pathologic_classic_hd_game/game'
video_dir = game_dir + '/data/Video'
video_dir_bak = video_dir + '/bak'

list_480 = ['aglaja.wmv', 'army.wmv', 'death.wmv', 'death_fail.wmv', 'fin_beda.wmv',
            'fin_smiren.wmv', 'fin_termit.wmv', 'fin_utop.wmv', 'intro.wmv',
            'intro_danko.wmv', 'NightMasks6.wmv', 'NightMasks7.wmv', 'NightMasks8.wmv', 'NightMasks9.wmv', 'NightMasks10.wmv','NightMasks11.wmv']

list_600 = ['aglaya.wmv', 'intro_burah.wmv', 'intro_klara.wmv',
            'NightMasks1.wmv', 'NightMasks2.wmv', 'NightMasks3.wmv', 'NightMasks4.wmv',
            'NightMasks5.wmv']

full_list = list_480 + list_600

class GUI:

    def __init__(self):
        self.config_load()
        self.create_main_window()

    def config_load(self):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('Settings'):
            config_parser.add_section('Settings')

        if not config_parser.has_option('Settings', 'crop'):
            self.crop = 0
            config_parser.set('Settings', 'crop', str(self.crop))
        else:
            self.crop = config_parser.getint('Settings', 'crop')

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Pathologic Classic HD"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 360
            )
        self.main_window.connect('delete-event', self.quit_app)

        frame_crop = Gtk.Frame(
            label = _("Crop videos (FFmpeg)"),
            label_xalign = 0.5,
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10
            )

        box_frame_crop = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            spacing = 10
            )

        self.combobox_crop = Gtk.ComboBoxText()
        self.combobox_crop.append_text(_("4:3 (no cropping)"))
        self.combobox_crop.append_text('16:9')
        self.combobox_crop.append_text('16:10')
        self.combobox_crop.set_active(self.crop)

        self.button_crop = Gtk.Button(label=_("Crop and quit"))
        self.button_crop.connect('clicked', self.cb_button_crop)

        self.progressbar = Gtk.ProgressBar(
            hexpand = True,
            show_text = True,
            text = _("Processing..."),
            pulse_step = 0.1,
            no_show_all = True
            )

        box_frame_crop.pack_start(self.combobox_crop, True, True, 0)
        box_frame_crop.pack_start(self.button_crop, True, True, 0)
        box_frame_crop.pack_start(self.progressbar, True, True, 0)

        frame_crop.add(box_frame_crop)

        self.main_window.add(frame_crop)
        self.main_window.show_all()

    def cb_button_crop(self, button):

        self.combobox_crop.set_sensitive(False)
        self.button_crop.set_visible(False)
        self.progressbar.set_visible(True)

        n_files_480 = len(list_480)
        n_files_600 = len(list_600)
        self.n_files = n_files_480 + n_files_600

        crop = self.combobox_crop.get_active()

        if crop != self.crop:

            self.crop = crop

            if crop == 0:
                if os.path.exists(video_dir_bak):
                    for file_name in full_list:
                        os.system('rm ' + video_dir + '/' + file_name)
                    os.system('mv ' + video_dir_bak + '/* ' + video_dir)
                    os.system('rm -r ' + video_dir_bak)

                self.config_save_crop(self.crop)
                Gtk.main_quit()

            else:

                if not os.path.exists(video_dir_bak):
                    os.system('mkdir -p ' + video_dir_bak)
                    for file_name in full_list:
                        os.system('mv ' + video_dir + '/' + file_name + ' ' + video_dir_bak)
                else:
                    for file_name in full_list:
                        os.system('rm ' + video_dir + '/' + file_name)

                for file_name in list_480:
                    self.crop_file_480(file_name, crop)

                for file_name in list_600:
                    self.crop_file_600(file_name, crop)
        else:
            Gtk.main_quit()

    def crop_file_480(self, file_name, crop):

        if crop == 1:
            region = '640:360:0:60'
        elif crop == 2:
            region = '640:400:0:40'

        command = ['ffmpeg', '-i', video_dir_bak + '/' + file_name, '-filter:v',
        'crop=' + region, '-vcodec', 'wmv2', '-q', '3', video_dir + '/' + file_name]

        self.pid, stdin, stdout, stderr = GLib.spawn_async(command,
                                    flags=GLib.SpawnFlags.SEARCH_PATH|GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                                    standard_output=True,
                                    standard_error=True)

        io = GLib.IOChannel(stdout)

        self.source_id_out = io.add_watch(GLib.IO_IN|GLib.IO_HUP,
                             self.watch_process,
                             'cropping_video_480',
                             priority=GLib.PRIORITY_HIGH)

    def crop_file_600(self, file_name, crop):

        if crop == 1:
            region = '800:450:0:75'
        elif crop == 2:
            region = '800:500:0:50'

        command = ['ffmpeg', '-i', video_dir_bak + '/' + file_name, '-filter:v',
        'crop=' + region, '-vcodec', 'wmv2', '-q', '5', video_dir + '/' + file_name]

        self.pid, stdin, stdout, stderr = GLib.spawn_async(command,
                                    flags=GLib.SpawnFlags.SEARCH_PATH|GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                                    standard_output=True,
                                    standard_error=True)

        io = GLib.IOChannel(stdout)

        self.source_id_out = io.add_watch(GLib.IO_IN|GLib.IO_HUP,
                             self.watch_process,
                             'cropping_video_600',
                             priority=GLib.PRIORITY_HIGH)

    def config_save_crop(self, crop):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        config_parser.set('Settings', 'crop', str(crop))

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

        self.button_crop.set_visible(True)
        self.progressbar.set_visible(False)
        self.combobox_crop.set_sensitive(True)

    def watch_process(self, io, condition, process_name):

        if condition is GLib.IO_HUP:

            if process_name == 'cropping_video_480':

                self.progressbar.pulse()

                self.n_files -= 1

                if self.n_files == 0:
                    self.config_save_crop(self.crop)
                    Gtk.main_quit()

                return False

            elif process_name == 'cropping_video_600':

                self.progressbar.pulse()

                self.n_files -= 1

                if self.n_files == 0:
                    self.config_save_crop(self.crop)
                    Gtk.main_quit()

                return False

        print(io.readline().strip('\n'))

        return True

    def quit_app(self, window, event):
        Gtk.main_quit()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
