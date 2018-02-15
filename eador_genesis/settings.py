import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
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

        if not config_parser.has_option('Settings', 'fullscreen'):
            self.fullscreen = False
            config_parser.set('Settings', 'fullscreen', str(self.fullscreen))
        else:
            self.fullscreen = config_parser.getboolean('Settings', 'fullscreen')

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def config_save(self):

        if self.fullscreen:
            new_launch_command = 'python "$NEBULA_DIR/launcher_wine.py" eador_genesis "Eador.exe f"'
        else:
            new_launch_command = 'python "$NEBULA_DIR/launcher_wine.py" eador_genesis "Eador.exe"'

        start_file = open(current_dir + '/start.sh', 'r')
        start_file_content = start_file.readlines()
        start_file.close()

        for i in range(len(start_file_content)):
            if '.exe' in start_file_content[i]:
                start_file_content[i] = new_launch_command

        start_file = open(current_dir + '/start.sh', 'w')
        start_file.writelines(start_file_content)
        start_file.close()

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        config_parser.set('Settings', 'fullscreen', str(self.fullscreen))

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Eador: Genesis"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 360,
            default_height = 180
            )
        self.main_window.connect('delete-event', self.quit_app)

        label = Gtk.Label(
            halign = Gtk.Align.FILL,
            label = _("Mode:"),
            )

        radiobutton_windowed = Gtk.RadioButton(
            label = _("Windowed"),
            name = 'windowed'
            )
        radiobutton_windowed.connect('toggled', self.cb_radiobuttons)

        radiobutton_fullscreen = Gtk.RadioButton(
            label = _("Fullscreen"),
            name = 'fullscreen'
            )
        radiobutton_fullscreen.join_group(radiobutton_windowed)
        radiobutton_fullscreen.connect('toggled', self.cb_radiobuttons)

        if not self.fullscreen:
            radiobutton_windowed.set_active(True)
        else:
            radiobutton_fullscreen.set_active(True)

        button_save = Gtk.Button(
            label = _("Save and quit"),
            )
        button_save.connect('clicked', self.cb_button_save)

        box = Gtk.Box(
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            spacing = 10,
            orientation = Gtk.Orientation.VERTICAL
            )

        box.pack_start(label, True, True, 0)
        box.pack_start(radiobutton_windowed, True, True, 0)
        box.pack_start(radiobutton_fullscreen, True, True, 0)
        box.pack_start(button_save, True, True, 0)

        self.main_window.add(box)
        self.main_window.show_all()

    def cb_button_save(self, button):
        self.config_save()
        Gtk.main_quit()

    def cb_radiobuttons(self, radiobutton):
        if radiobutton.get_active() and (radiobutton.get_name() == 'fullscreen'):
            self.fullscreen = True
        else:
            self.fullscreen = False

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
