#!/usr/bin/env python2
# -*- Mode: Python; coding: utf-8 -*-

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import ConfigParser
import gettext
import stat
import imp

nebula_dir = os.getenv('NEBULA_DIR')

modules_dir = nebula_dir + '/modules'
set_visuals = imp.load_source('set_visuals', modules_dir + '/set_visuals.py')

gettext.bindtextdomain('games_nebula', nebula_dir + '/locale')
gettext.textdomain('games_nebula')
_ = gettext.gettext

current_dir = sys.path[0]

class GUI:

    def __init__(self):
        self.create_main_window()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Baldur's Gate: The Original Saga"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            width_request = 360
            )
        self.main_window.connect('delete-event', self.quit_app)

        box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            spacing = 10,
            )

        button_widescreen = Gtk.Button(
            label = _("Install Widescreen Mod"),
            )
        button_widescreen.connect('clicked', self.cb_button_widescreen)

        button_gui_fix = Gtk.Button(
            label = _("Install TWM GUI"),
            )
        button_gui_fix.connect('clicked', self.cb_button_gui_fix)

        button_ub = Gtk.Button(
            label = _("Install Unfinished Business"),
            )
        button_ub.connect('clicked', self.cb_button_ub)

        button_tp = Gtk.Button(
            label = _("Install Tweaks"),
            )
        button_tp.connect('clicked', self.cb_button_tp)

        box.pack_start(button_widescreen, True, True, 0)
        box.pack_start(button_gui_fix, True, True, 0)
        box.pack_start(button_ub, True, True, 0)
        box.pack_start(button_tp, True, True, 0)

        self.main_window.add(box)
        self.main_window.show_all()

    def cb_button_widescreen(self, button):

        self.main_window.hide()

        while Gtk.events_pending():
            Gtk.main_iteration()

        os.system('cd "' + current_dir + '/game" && ' + \
        'xterm -fg green -bg black -fn 10x20 -e ./widescreen.sh')

        self.main_window.show()

    def cb_button_gui_fix(self, button):

        self.main_window.hide()

        while Gtk.events_pending():
            Gtk.main_iteration()

        os.system('cd "' + current_dir + '/game" && ' + \
        'xterm -fg green -bg black -fn 10x20 -e ./gui_fix.sh')

        self.main_window.show()

    def cb_button_ub(self, button):

        self.main_window.hide()

        while Gtk.events_pending():
            Gtk.main_iteration()

        os.system('cd "' + current_dir + '/game" && ' + \
        'xterm -fg green -bg black -fn 10x20 -e ./ub.sh')

        self.main_window.show()

    def cb_button_tp(self, button):

        self.main_window.hide()

        while Gtk.events_pending():
            Gtk.main_iteration()

        os.system('cd "' + current_dir + '/game" && ' + \
        'xterm -fg green -bg black -fn 10x20 -e ./tweakpack.sh')

        self.main_window.show()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
