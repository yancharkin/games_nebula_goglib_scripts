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
            self.custom_width = ''
            self.custom_height = ''

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

        config_file = current_dir + '/game/Battle_Realms.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)
        config_parser.set('VideoState', 'width', str(self.custom_width))
        config_parser.set('VideoState', 'height', str(self.custom_height))
        config_parser.set('VideoState', 'hardwaretl', '1')
        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Battle Realms: Winter of the Wolf"),
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
            label = _("Set custom resolution:")
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

        button_patch = Gtk.Button(
            label = _("Patch")
            )
        button_patch.connect('clicked', self.cb_button_patch)

        grid.attach(label_custom_res, 0, 0, 2, 1)
        grid.attach(entry_custom_width, 0, 1, 1, 1)
        grid.attach(entry_custom_height, 1, 1, 1, 1)
        grid.attach(button_patch, 0, 2, 2, 1)

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

    def cb_button_patch(self, button):

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
        self.modify_exe()
        Gtk.main_quit()

    def modify_exe(self):

        exe_path = current_dir + '/game/Battle_Realms_F.exe'

        if not os.path.exists(exe_path + '.bak'):
            os.system('cp ' + exe_path + ' ' + exe_path + '.bak')

        width = int(self.custom_width)
        height = int(self.custom_height)

        hex_width = list('0' + hex(width).split('x')[1])
        width_offset1_value = hex_width[2] + hex_width[3]
        width_offset2_value = hex_width[0] + hex_width[1]

        hex_height = list('0' + hex(height).split('x')[1])
        height_offset1_value = hex_height[2] + hex_height[3]
        height_offset2_value = hex_height[0] + hex_height[1]

        width_offsets = [
                        [0x2380ad, 0x2380ae],
                        [0x23822c, 0x23822d],
                        [0x2445c4, 0x2445c5],
                        [0x2447b6, 0x2447b7]
                        ]

        height_offsets = [
                        [0x2380b5, 0x2380b6],
                        [0x238235, 0x238236],
                        [0x2445ce, 0x2445cf],
                        [0x2447bf, 0x2447c0]
                        ]

        exe_file = open(exe_path, 'r+b')

        for offset in width_offsets:
            exe_file.seek(offset[0])
            width_offset1_value_b = self.to_bytes(int(width_offset1_value, 16))
            exe_file.write(width_offset1_value_b)
            exe_file.seek(offset[1])
            width_offset2_value_b = self.to_bytes(int(width_offset2_value, 16))
            exe_file.write(width_offset2_value_b)

        for offset in height_offsets:
            exe_file.seek(offset[0])
            height_offset1_value_b = self.to_bytes(int(height_offset1_value, 16))
            exe_file.write(height_offset1_value_b)
            exe_file.seek(offset[1])
            height_offset2_value_b = self.to_bytes(int(height_offset2_value, 16))
            exe_file.write(height_offset2_value_b)

        exe_file.close()

    def to_bytes(self, value):

        if sys.version_info[0] == 2:
            return chr(value)
        elif sys.version_info[0] == 3:
            return bytes([value])

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
