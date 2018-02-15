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
game_dir = install_dir + '/konung_legend_of_the_north/game'
patch_path = download_dir + '/_distr/konung_legend_of_the_north/konung_widescreen_v2_co.7z'
link_patch = 'http://www.wsgf.org/dr/konung-legends-north/en'

os.system('mkdir -p ' + download_dir + '/_distr/konung_legend_of_the_north')

is_english_version = os.path.exists(game_dir + '/MUSIC')

class GUI:

    def __init__(self):

        self.config_load()

        if is_english_version:
            self.create_chooser_window()
        else:
            if os.path.exists(patch_path):
                if not os.path.exists(game_dir + '/res_patch'):
                    os.system('7z x -aoa -o' + game_dir + '/res_patch ' + patch_path)
                self.create_set_res_window()
                self.set_res_window.show_all()
            else:
                self.create_download_window()
                self.download_window.show_all()

    def config_load(self):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('Settings'):
            config_parser.add_section('Settings')

        if is_english_version:
            if not config_parser.has_option('Settings', 'exe'):
                self.exe = 'KONUNG.EXE'
                config_parser.set('Settings', 'exe', str(self.exe))
            else:
                self.exe = config_parser.get('Settings', 'exe')
        else:
            if not config_parser.has_option('Settings', 'resolution'):
                self.resolution = 0
                config_parser.set('Settings', 'resolution', str(self.resolution))
            else:
                self.resolution = config_parser.getint('Settings', 'resolution')

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def create_chooser_window(self):

        self.chooser_window = Gtk.Window(
            title = _("Konung: Legends of the North"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 360
            )
        self.chooser_window.connect('delete-event', self.quit_app)

        frame_launch = Gtk.Frame(
            label = _("Launch options"),
            label_xalign = 0.5,
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10
            )

        box_launch = Gtk.Box(
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            spacing = 10,
            orientation = Gtk.Orientation.VERTICAL
            )

        radiobutton_single = Gtk.RadioButton(
            label = _("Singleplayer"),
            name = 'KONUNG.EXE'
            )

        radiobutton_lan = Gtk.RadioButton(
            label = _("LAN multiplayer"),
            name = 'LAN_KONG.EXE'
            )
        radiobutton_lan.join_group(radiobutton_single)

        radiobutton_tutorial = Gtk.RadioButton(
            label = _("Tutorial"),
            name = 'TUTORIAL.EXE'
            )
        radiobutton_tutorial.join_group(radiobutton_single)

        button_save = Gtk.Button(
            label = _("Save and quit")
            )
        button_save.connect('clicked', self.cb_button_save)

        box_launch.pack_start(radiobutton_single, True, True, 0)
        box_launch.pack_start(radiobutton_lan, True, True, 0)
        box_launch.pack_start(radiobutton_tutorial, True, True, 0)
        box_launch.pack_start(button_save, True, True, 0)
        frame_launch.add(box_launch)

        for radiobutton in box_launch.get_children():
            if radiobutton.get_name() == self.exe:
                radiobutton.set_active(True)

        radiobutton_single.connect('clicked', self.cb_radiobuttons)
        radiobutton_lan.connect('clicked', self.cb_radiobuttons)
        radiobutton_tutorial.connect('clicked', self.cb_radiobuttons)

        self.chooser_window.add(frame_launch)
        self.chooser_window.show_all()

    def create_download_window(self):

        self.download_window = Gtk.Window(
            title = _("Konung: Legends of the North"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 360
            )
        self.download_window.connect('delete-event', self.quit_app)

        box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            spacing = 10
            )

        linkbutton_download = Gtk.LinkButton(
            label = _("Download resolution patch"),
            uri = link_patch
            )

        linkbutton_put = Gtk.LinkButton(
            label = _("Put it here"),
            uri = 'file://' + download_dir + '/_distr/konung_legend_of_the_north'
            )

        button_install = Gtk.Button(label=_("Install"))
        button_install.connect('clicked', self.cb_button_install)

        box.pack_start(linkbutton_download, True, True, 0)
        box.pack_start(linkbutton_put, True, True, 0)
        box.pack_start(button_install, True, True, 0)

        self.download_window.add(box)

    def create_set_res_window(self):

        self.set_res_window = Gtk.Window(
            title = _("Konung: Legends of the North"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 360
            )
        self.set_res_window.connect('delete-event', self.quit_app)

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

        self.combobox_resolution = Gtk.ComboBoxText()
        resolutions_list = sorted(os.listdir(game_dir + '/res_patch'))
        for resolution in resolutions_list:
            self.combobox_resolution.append_text(resolution)
        self.combobox_resolution.set_active(self.resolution)

        self.combobox_resolution.connect('changed', self.cb_combobox_resolution)

        button_save = Gtk.Button(
            label = _("Save and quit"),
            )
        button_save.connect('clicked', self.cb_button_save)

        grid.attach(label_custom_res, 0, 0, 1, 1)
        grid.attach(self.combobox_resolution, 1, 0, 1, 1)
        grid.attach(button_save, 0, 2, 2, 1)

        self.set_res_window.add(grid)

    def modify_start_file(self):

        new_launch_command = \
        'python "$NEBULA_DIR/launcher_wine.py" konung_legend_of_the_north "' + self.exe + '"'

        start_file = open(current_dir + '/start.sh', 'r')
        start_file_content = start_file.readlines()
        start_file.close()

        for i in range(len(start_file_content)):
            if '.exe' in start_file_content[i].lower():
                start_file_content[i] = new_launch_command

        start_file = open(current_dir + '/start.sh', 'w')
        start_file.writelines(start_file_content)
        start_file.close()

    def cb_button_install(self, button):

        if not os.path.exists(patch_path):

            self.download_window.hide()

            message_dialog = Gtk.MessageDialog(
                self.download_window,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK,
                _("Error")
                )
            message_dialog.format_secondary_text(_("Patch not found in download directory."))
            content_area = message_dialog.get_content_area()
            content_area.set_property('margin-left', 10)
            content_area.set_property('margin-right', 10)
            content_area.set_property('margin-top', 10)
            content_area.set_property('margin-bottom', 10)
            message_dialog.run()
            message_dialog.destroy()

            self.download_window.show()

        else:
            os.system('7z x -aoa -o' + game_dir + '/res_patch ' + patch_path)

            while Gtk.events_pending():
                Gtk.main_iteration()

            self.download_window.hide()
            self.create_set_res_window()
            self.set_res_window.show_all()

    def cb_combobox_resolution(self, combobox):
        self.resolution = combobox.get_active()

    def cb_button_save(self, button):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        if is_english_version:
            self.modify_start_file()
            config_parser.set('Settings', 'exe', str(self.exe))
        else:

            if not os.path.exists(game_dir + '/konung.exe.original'):
                os.system('mv ' + game_dir + '/konung.exe ' + game_dir + '/konung.exe.original')

            selected_resolution = self.combobox_resolution.get_active_text()
            os.system('cp ' + game_dir + '/res_patch/' + selected_resolution + '/* ' + game_dir)

            config_parser.set('Settings', 'resolution', str(self.resolution))

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

        Gtk.main_quit()

    def cb_radiobuttons(self, radiobutton):
        self.exe = radiobutton.get_name()

    def quit_app(self, window, event):
        Gtk.main_quit()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
