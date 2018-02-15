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
game_dir = install_dir + '/desperados_wanted_dead_or_alive/game'
link_patch = 'http://www.wsgf.org/dr/desperados-wanted-dead-or-alive/en'
patch_path = download_dir + '/_distr/desperados_wanted_dead_or_alive/Desperados_0.7z'

os.system('mkdir -p ' + download_dir + '/_distr/desperados_wanted_dead_or_alive')

class GUI:

    def __init__(self):

        self.config_load()

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

        if not config_parser.has_option('Settings', 'resolution'):
            self.resolution = 0
            config_parser.set('Settings', 'resolution', str(self.resolution))
        else:
            self.resolution = config_parser.getint('Settings', 'resolution')

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def create_download_window(self):

        self.download_window = Gtk.Window(
            title = _("Desperados: Wanted Dead or Alive"),
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
            label = _("Download patch"),
            uri = link_patch
            )

        linkbutton_put = Gtk.LinkButton(
            label = _("Put it here"),
            uri = 'file://' + download_dir + '/_distr/desperados_wanted_dead_or_alive'
            )

        button_install = Gtk.Button(label=_("Install"))
        button_install.connect('clicked', self.cb_button_install)

        box.pack_start(linkbutton_download, True, True, 0)
        box.pack_start(linkbutton_put, True, True, 0)
        box.pack_start(button_install, True, True, 0)

        self.download_window.add(box)

    def create_set_res_window(self):

        self.set_res_window = Gtk.Window(
            title = _("Desperados: Wanted Dead or Alive"),
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

        if not os.path.exists(game_dir + '/Game/game.exe.original'):
            os.system('mv ' + game_dir + '/Game/game.exe ' + game_dir + '/Game/game.exe.original')

        selected_resolution = self.combobox_resolution.get_active_text()
        os.system('cp ' + game_dir + '/res_patch/' + selected_resolution + '/game.exe ' +
        game_dir + '/Game')

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        config_parser.set('Settings', 'resolution', str(self.resolution))

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

        Gtk.main_quit()

    def quit_app(self, window, event):
        Gtk.main_quit()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
