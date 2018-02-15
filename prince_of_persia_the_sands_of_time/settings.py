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

        config_file = current_dir + '/game/pop.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('MAIN'):
            config_parser.add_section('MAIN')

        if not config_parser.has_option('MAIN', 'Width'):
            self.width = '1280'
            config_parser.set('MAIN', 'Width', str(self.width))
        else:
            self.width = config_parser.get('MAIN', 'Width')

        if not config_parser.has_option('MAIN', 'Height'):
            self.height = '720'
            config_parser.set('MAIN', 'Height', str(self.height))
        else:
            self.height = config_parser.get('MAIN', 'Height')

        if not config_parser.has_section('HUD'):
            config_parser.add_section('HUD')

        if not config_parser.has_option('HUD', 'HUD_posX_auto'):
            self.hud_posx = '1'
            config_parser.set('HUD', 'HUD_posX_auto', str(self.hud_posx))
        else:
            self.hud_posx = config_parser.get('HUD', 'HUD_posX_auto').split(' // ')[0]

        if not config_parser.has_section('MISC'):
            config_parser.add_section('MISC')

        if not config_parser.has_option('MISC', 'cutscenes_black_borders'):
            self.cutscenes_black_borders = '1'
            config_parser.set('MISC', 'cutscenes_black_borders', str(self.cutscenes_black_borders))
        else:
            self.cutscenes_black_borders = config_parser.get('MISC', 'cutscenes_black_borders').split(' // ')[0]

        if not config_parser.has_option('MISC', 'Xbox_fov'):
            self.xbox_fov = '1'
            config_parser.set('MISC', 'Xbox_fov', str(self.xbox_fov))
        else:
            self.xbox_fov = config_parser.get('MISC', 'Xbox_fov').split(' // ')[0]

        if not config_parser.has_option('MISC', 'fov_multiplier'):
            self.fov_multiplier = '1'
            config_parser.set('MISC', 'fov_multiplier', str(self.fov_multiplier))
        else:
            self.fov_multiplier = config_parser.get('MISC', 'fov_multiplier').split(' // ')[0]

        if not config_parser.has_option('MISC', 'fog_bug_fix'):
            self.fog_bug_fix = '0'
            config_parser.set('MISC', 'fog_bug_fix', str(self.fog_bug_fix))
        else:
            self.fog_bug_fix = config_parser.get('MISC', 'fog_bug_fix')

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def config_save(self):

        config_file = current_dir + '/game/pop.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        config_parser.set('MAIN', 'Width', str(self.width))
        config_parser.set('MAIN', 'Height', str(self.height))
        config_parser.set('HUD', 'HUD_posX_auto', str(self.hud_posx))
        config_parser.set('MISC', 'cutscenes_black_borders', str(self.cutscenes_black_borders))
        config_parser.set('MISC', 'Xbox_fov', str(self.xbox_fov))
        config_parser.set('MISC', 'fov_multiplier', str(self.fov_multiplier))
        config_parser.set('MISC', 'fog_bug_fix', str(self.fog_bug_fix))

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

        config_file = current_dir + '/game/Hardware.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('CAPS'):
            config_parser.add_section('CAPS')

        if self.fog_bug_fix == '1':
            config_parser.set('CAPS', 'ForceVSFog', '1')
            config_parser.set('CAPS', 'InvertFogRange', '0')
        elif self.fog_bug_fix == '0':
            config_parser.set('CAPS', 'ForceVSFog', '0')
            config_parser.set('CAPS', 'InvertFogRange', '1')

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Prince of Persia: The Sands of Time"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            )
        self.main_window.connect('delete-event', self.quit_app)

        grid = Gtk.Grid(
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            row_spacing = 10,
            column_spacing = 10,
            )

        label_resolution = Gtk.Label(
            label = _("Resolution:"),
            halign = Gtk.Align.START
            )

        entry_width = Gtk.Entry(
            name = 'width',
            text=self.width,
            placeholder_text = _("Width"),
            max_length = 4,
            xalign = 0.5,
            )
        entry_width.connect('changed', self.cb_entries)

        entry_height = Gtk.Entry(
            name = 'height',
            text=self.height,
            placeholder_text = _("Height"),
            max_length = 4,
            xalign = 0.5,
            )
        entry_height.connect('changed', self.cb_entries)

        label_hud_posx = Gtk.Label(
            label = _("HUD auto position:"),
            halign = Gtk.Align.START
            )

        switch_hud_posx = Gtk.Switch(
            halign = Gtk.Align.END
            )
        if self.hud_posx == '1':
            switch_hud_posx.set_active(True)
        else:
            switch_hud_posx.set_active(False)
        switch_hud_posx.connect('state-set', self.cb_switch_hud_posx)

        label_cutscenes_black_borders = Gtk.Label(
            label = _("Cutscenes black borders:"),
            halign = Gtk.Align.START
            )

        switch_cutscenes_black_borders = Gtk.Switch(
            halign = Gtk.Align.END
            )
        if self.cutscenes_black_borders == '1':
            switch_cutscenes_black_borders.set_active(True)
        else:
            switch_cutscenes_black_borders.set_active(False)
        switch_cutscenes_black_borders.connect('state-set', self.cb_switch_cutscenes_black_borders)

        label_xbox_fov = Gtk.Label(
            label = _("Xbox FOV:"),
            halign = Gtk.Align.START
            )

        switch_xbox_fov = Gtk.Switch(
            halign = Gtk.Align.END
            )
        if self.xbox_fov == '1':
            switch_xbox_fov.set_active(True)
        else:
            switch_xbox_fov.set_active(False)
        switch_xbox_fov.connect('state-set', self.cb_switch_xbox_fov)

        label_fog_bug_fix = Gtk.Label(
            label = _("Fog bug fix:"),
            halign = Gtk.Align.START
            )

        switch_fog_bug_fix = Gtk.Switch(
            halign = Gtk.Align.END
            )
        if self.fog_bug_fix == '1':
            switch_fog_bug_fix.set_active(True)
        else:
            switch_fog_bug_fix.set_active(False)
        switch_fog_bug_fix.connect('state-set', self.cb_switch_fog_bug_fix)

        label_fov_multiplier = Gtk.Label(
            label = _("FOV multiplier:"),
            halign = Gtk.Align.START
            )

        entry_fov_multiplier = Gtk.Entry(
            name = 'fov_multiplier',
            text = self.fov_multiplier,
            max_length = 3,
            xalign = 0.5,
            )
        entry_fov_multiplier.connect('changed', self.cb_entries)

        button_save = Gtk.Button(
            label = _("Save and quit"),
            )
        button_save.connect('clicked', self.cb_button_save)

        grid.attach(label_resolution, 0, 0, 1, 1)
        grid.attach(entry_width, 1, 0, 1, 1)
        grid.attach(entry_height, 2, 0, 1, 1)
        grid.attach(label_fov_multiplier, 0, 1, 1, 1)
        grid.attach(entry_fov_multiplier, 1, 1, 2, 1)
        grid.attach(label_xbox_fov, 0, 2, 1, 1)
        grid.attach(switch_xbox_fov, 1, 2, 2, 1)
        grid.attach(label_hud_posx, 0, 3, 1, 1)
        grid.attach(switch_hud_posx, 1, 3, 2, 1)
        grid.attach(label_cutscenes_black_borders, 0, 4, 1, 1)
        grid.attach(switch_cutscenes_black_borders, 1, 4, 2, 1)
        grid.attach(label_fog_bug_fix, 0, 5, 1, 1)
        grid.attach(switch_fog_bug_fix, 1, 5, 2, 1)
        grid.attach(button_save, 0, 6, 3, 1)

        self.main_window.add(grid)
        self.main_window.show_all()

    def cb_button_save(self, button):
        self.config_save()
        Gtk.main_quit()

    def cb_entries(self, entry):
        text = entry.get_text().strip()
        new_text = (''.join([i for i in text if i in '0123456789.']))
        entry.set_text(new_text)
        if entry.get_name() == 'width':
            self.width = new_text
        elif entry.get_name() == 'height':
            self.height = new_text
        elif entry.get_name() == 'fov_multiplier':
            self.fov_multiplier = new_text

    def cb_switch_hud_posx(self, switch, event):
        if switch.get_active():
            self.hud_posx = '1'
        else:
            self.hud_posx = '0'

    def cb_switch_cutscenes_black_borders(self, switch, event):
        if switch.get_active():
            self.cutscenes_black_borders = '1'
        else:
            self.cutscenes_black_borders = '0'

    def cb_switch_xbox_fov(self, switch, event):
        if switch.get_active():
            self.xbox_fov = '1'
        else:
            self.xbox_fov = '0'

    def cb_switch_fog_bug_fix(self, switch, event):
        if switch.get_active():
            self.fog_bug_fix = '1'
        else:
            self.fog_bug_fix = '0'

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
