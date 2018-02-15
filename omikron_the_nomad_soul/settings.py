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

wineloader = os.getenv('WINELOADER')
current_dir = sys.path[0]

class GUI:

    def __init__(self):
        self.create_main_window()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Omikron: The Nomad Soul"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            )
        self.main_window.connect('delete-event', self.quit_app)

        button_patch = Gtk.Button(
            label = _("Old Games Widescreen Patch"),
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10
            )
        button_patch.connect('clicked', self.cb_button_patch)

        self.main_window.add(button_patch)
        self.main_window.show_all()

    def cb_button_patch(self, button):

        self.main_window.hide()

        while Gtk.events_pending():
            Gtk.main_iteration()

        os.system('cd "' + current_dir + '/game" && ' + wineloader + ' "./Old_Games_Widescreen_Patch.exe"')

        self.main_window.show()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
