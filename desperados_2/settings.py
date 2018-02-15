import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import gettext
import imp

nebula_dir = os.getenv('NEBULA_DIR')

modules_dir = nebula_dir + '/modules'
set_visuals = imp.load_source('set_visuals', modules_dir + '/set_visuals.py')

gettext.bindtextdomain('games_nebula', nebula_dir + '/locale')
gettext.textdomain('games_nebula')
_ = gettext.gettext

current_dir = sys.path[0]
config_file_path = current_dir + '/game/data/configuration/game/settings.xml'

class GUI:

    def __init__(self):
        self.config_load()
        self.create_main_window()

    def config_load(self):
        config_file = open(config_file_path, 'r')
        config_content = config_file.readlines()
        config_file.close()

        for line in config_content:
            if 'ENGINE_RESOLUTION_X' in line:
                self.custom_width = line.split('="')[2].split('"')[0]
            if 'ENGINE_RESOLUTION_Y' in line:
                self.custom_height = line.split('="')[2].split('"')[0]

    def config_save(self):

        config_file = open(config_file_path, 'r')
        config_content = config_file.readlines()
        config_file.close()

        config_file = open(config_file_path, 'w')

        for line in config_content:
            if 'ENGINE_RESOLUTION_X' in line:
                config_file.write('    <Attribute name="ENGINE_RESOLUTION_X" value="' + self.custom_width + '" type="string" />\n')
            elif 'ENGINE_RESOLUTION_Y' in line:
                config_file.write('    <Attribute name="ENGINE_RESOLUTION_Y" value="' + self.custom_height + '" type="string" />\n')
            else:
                config_file.write(line)

        config_file.close()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Desperados 2: Cooper's Revenge"),
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

        button_save = Gtk.Button(
            label = _("Save and quit"),
            )
        button_save.connect('clicked', self.cb_button_save)

        grid.attach(label_custom_res, 0, 0, 2, 1)
        grid.attach(entry_custom_width, 0, 1, 1, 1)
        grid.attach(entry_custom_height, 1, 1, 1, 1)
        grid.attach(button_save, 0, 3, 2, 1)

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

    def cb_button_save(self, button):

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
        Gtk.main_quit()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
