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

        config_file = current_dir + '/game/bge.ini'
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

        if not config_parser.has_option('MISC', 'PillarBox'):
            self.pillarbox = '1'
            config_parser.set('MISC', 'PillarBox', str(self.pillarbox))
        else:
            self.pillarbox = config_parser.get('MISC', 'PillarBox').split(' // ')[0]

        if not config_parser.has_option('MISC', 'Gameplay_FOV'):
            self.fov = '1'
            config_parser.set('MISC', 'Gameplay_FOV', str(self.fov))
        else:
            self.fov = config_parser.get('MISC', 'Gameplay_FOV').split(' // ')[0]

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def config_save(self):

        config_file = current_dir + '/game/bge.ini'
        config_parser = ConfigParser()
        config_parser.read(config_file)

        config_parser.set('MAIN', 'Width', str(self.width))
        config_parser.set('MAIN', 'Height', str(self.height))
        config_parser.set('HUD', 'HUD_posX_auto', str(self.hud_posx))
        config_parser.set('MISC', 'PillarBox', str(self.pillarbox))
        config_parser.set('MISC', 'Gameplay_FOV', str(self.fov))

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Beyond Good & Evil"),
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

        label_pillarbox = Gtk.Label(
            label = _("Pillarbox:"),
            halign = Gtk.Align.START
            )

        combobox_pillarbox = Gtk.ComboBoxText()
        pillarbox_options = {
                            '0':_("Off"),
                            '1':_("On"),
                            '2':_("Advanced pillarboxing")
                            }
        index = 0
        for i in range(len(pillarbox_options)):
            combobox_pillarbox.append_text(pillarbox_options[str(i)])
            if str(i) == self.pillarbox:
                index = i
        combobox_pillarbox.set_active(index)
        combobox_pillarbox.connect('changed', self.cb_combobox)

        label_fov = Gtk.Label(
            label = _("FOV:"),
            halign = Gtk.Align.START
            )

        entry_fov = Gtk.Entry(
            name = 'fov',
            text = self.fov,
            placeholder_text = _("FOV"),
            max_length = 3,
            xalign = 0.5,
            )
        entry_fov.connect('changed', self.cb_entries)

        button_more = Gtk.Button(
            label = _("More settings"),
            margin_top = 10
            )
        button_more.connect('clicked', self.cb_button_more)

        button_save = Gtk.Button(
            label = _("Save and quit"),
            )
        button_save.connect('clicked', self.cb_button_save)

        grid.attach(label_resolution, 0, 0, 1, 1)
        grid.attach(entry_width, 1, 0, 1, 1)
        grid.attach(entry_height, 2, 0, 1, 1)
        grid.attach(label_fov, 0, 1, 1, 1)
        grid.attach(entry_fov, 1, 1, 2, 1)
        grid.attach(label_pillarbox, 0, 2, 1, 1)
        grid.attach(combobox_pillarbox, 1, 2, 2, 1)
        grid.attach(label_hud_posx, 0, 3, 1, 1)
        grid.attach(switch_hud_posx, 1, 3, 2, 1)
        grid.attach(button_more, 0, 4, 3, 1)
        grid.attach(button_save, 0, 5, 3, 1)

        self.main_window.add(grid)
        self.main_window.show_all()

    def cb_button_save(self, button):
        self.config_save()
        Gtk.main_quit()

    def cb_button_more(self, button):

        settings_exe = current_dir + '/game/SettingsApplication.exe'
        launch_command = '"$WINELOADER" "' + settings_exe + '"'

        self.main_window.hide()

        while Gtk.events_pending():
            Gtk.main_iteration()

        os.system(launch_command)

        self.main_window.show()

    def cb_entries(self, entry):
        text = entry.get_text().strip()
        new_text = (''.join([i for i in text if i in '0123456789.']))
        entry.set_text(new_text)
        if entry.get_name() == 'width':
            self.width = new_text
        elif entry.get_name() == 'height':
            self.height = new_text
        elif entry.get_name() == 'fov':
            self.fov = new_text

    def cb_switch_hud_posx(self, switch, event):
        if switch.get_active():
            self.hud_posx = '1'
        else:
            self.hud_posx = '0'

    def cb_combobox(self, combobox):
        if combobox.get_active_text() == _("Off"):
             self.pillarbox = '0'
        elif combobox.get_active_text() == _("On"):
            self.pillarbox = '1'
        elif combobox.get_active_text() == _("Advanced pillarboxing"):
            self.pillarbox = '2'

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
