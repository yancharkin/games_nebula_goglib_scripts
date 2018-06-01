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
download_dir = os.getenv('DOWNLOAD_DIR')
install_dir = os.getenv('INSTALL_DIR')
game_dir = install_dir + '/bloodrayne_2/game'
wineloader = os.getenv('WINELOADER')
video_dir = current_dir + '/game/video'
video_dir_bak = video_dir + '/bak'

os.system('mkdir -p "' + download_dir + '/_distr/bloodrayne_2"')

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
            title = _("Blood Rayne 2"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 360
            )
        self.main_window.connect('delete-event', self.quit_app)

        box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            spacing = 10
            )

        frame_crop = Gtk.Frame(
            label = _("Crop videos (FFmpeg)"),
            label_xalign = 0.5
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

        self.button_crop = Gtk.Button(label=_("Start"))
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

        frame_patch = Gtk.Frame(
            label = _("FSAA Patch"),
            label_xalign = 0.5
            )

        box_frame_patch = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10
            )

        self.linkbutton_download = Gtk.LinkButton(
            label = _("Download patch"),
            uri = 'http://www.coopdb.com/modules.php?name=BR2fsaa&op=Download',
            no_show_all = True
            )

        self.linkbutton_put = Gtk.LinkButton(
            label = _("Put it here"),
            uri = 'file://' + download_dir + '/_distr/bloodrayne_2',
            no_show_all = True
            )

        self.button_patch = Gtk.Button()
        self.button_patch.connect('clicked', self.cb_button_patch)

        box_frame_patch.pack_start(self.linkbutton_download, True, True, 0)
        box_frame_patch.pack_start(self.linkbutton_put, True, True, 0)
        box_frame_patch.pack_start(self.button_patch, True, True, 0)

        frame_patch.add(box_frame_patch)

        box.pack_start(frame_crop, True, True, 0)
        box.pack_start(frame_patch, True, True, 0)

        self.fsaa_options_visibility()
        self.main_window.add(box)
        self.main_window.show_all()

    def fsaa_options_visibility(self):
        if os.path.exists(game_dir + '/' + 'br2fsaaConfig.exe'):
            self.linkbutton_download.set_visible(False)
            self.linkbutton_put.set_visible(False)
            self.button_patch.set_label(_("FSAA Patch settings"))
        else:
            self.linkbutton_download.set_visible(True)
            self.linkbutton_put.set_visible(True)
            self.button_patch.set_label(_("Install"))

    def cb_button_patch(self, button):

        if os.path.exists(game_dir + '/' + 'br2fsaaConfig.exe'):
            self.launch_fsaa_settings()
        else:

            patch_path = download_dir + '/_distr/bloodrayne_2/BR2_FSAA_Patch_1.666.rar'

            if not os.path.exists(patch_path):

                message_dialog = Gtk.MessageDialog(
                    self.main_window,
                    0,
                    Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.OK,
                    _("Patch not found in download directory.")
                    )
                content_area = message_dialog.get_content_area()
                content_area.set_property('margin-left', 10)
                content_area.set_property('margin-right', 10)
                content_area.set_property('margin-top', 10)
                content_area.set_property('margin-bottom', 10)

                self.main_window.hide()
                message_dialog.run()
                message_dialog.destroy()
                self.main_window.show()

            else:

                self.button_patch.set_sensitive(False)

                while Gtk.events_pending():
                    Gtk.main_iteration_do(False)

                command = ['7z', 'e', '-aoa', '-o' + game_dir, patch_path]

                self.pid, stdin, stdout, stderr = GLib.spawn_async(command,
                                            flags=GLib.SpawnFlags.SEARCH_PATH|GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                                            standard_output=True,
                                            standard_error=True)

                io = GLib.IOChannel(stdout)

                self.source_id_out = io.add_watch(GLib.IO_IN|GLib.IO_HUP,
                                     self.watch_process,
                                     'extracting',
                                     priority=GLib.PRIORITY_HIGH)

    def cb_button_crop(self, button):

        self.button_patch.set_sensitive(False)
        self.combobox_crop.set_sensitive(False)
        self.button_crop.set_visible(False)
        self.progressbar.set_visible(True)

        crop = self.combobox_crop.get_active()

        if crop != self.crop:

            self.crop = crop

            self.n_files = 0

            if crop == 0:
                if os.path.exists(video_dir_bak):
                    for file_name in os.listdir(video_dir):
                        if '.mpg' in file_name:
                            self.n_files += 1
                            os.system('rm "' + video_dir + '/' + file_name + '"')
                    os.system('mv "' + video_dir_bak + '/"* "' + video_dir + '"')
                    os.system('rm -r "' + video_dir_bak + '"')

                self.config_save_crop(self.crop)

            else:

                if not os.path.exists(video_dir_bak):
                    os.system('mkdir -p "' + video_dir_bak + '"')
                    for file_name in os.listdir(video_dir):
                        if '.mpg' in file_name:
                            self.n_files += 1
                            os.system('mv "' + video_dir + '/' + file_name + '" "' + video_dir_bak + '"')
                else:
                    for file_name in os.listdir(video_dir):
                        if '.mpg' in file_name:
                            self.n_files += 1
                            os.system('rm "' + video_dir + '/' + file_name + '"')

                for file_name in os.listdir(video_dir_bak):
                    if '.mpg' in file_name:
                        self.crop_file(file_name, crop)
        else:
            self.button_patch.set_sensitive(True)
            self.combobox_crop.set_sensitive(True)
            self.button_crop.set_visible(True)
            self.progressbar.set_visible(False)

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
        self.button_patch.set_sensitive(True)

    def launch_fsaa_settings(self):

        self.main_window.hide()

        while Gtk.events_pending():
            Gtk.main_iteration_do(False)

        os.system(wineloader + ' "' + game_dir + '/br2fsaaConfig.exe"')
        self.main_window.show()

    def watch_process(self, io, condition, process_name):

        if condition is GLib.IO_HUP:

            if process_name == 'extracting':

                self.launch_fsaa_settings()

                self.button_patch.set_sensitive(True)
                self.fsaa_options_visibility()

                return False

            elif process_name == 'cropping_video':

                self.progressbar.pulse()

                self.n_files -= 1

                if self.n_files == 0:
                    self.config_save_crop(self.crop)

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
