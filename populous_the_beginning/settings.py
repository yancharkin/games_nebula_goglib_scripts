#!/usr/bin/env python2
# -*- Mode: Python; coding: utf-8; -*-

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import ConfigParser
import gettext

current_dir = sys.path[0]

class GUI:

    def __init__(self, wine_path, wineprefix_path, nebula_dir):

        gettext.bindtextdomain('games_nebula', nebula_dir + '/locale')
        gettext.textdomain('games_nebula')
        self._ = gettext.gettext

        self.wine_path = wine_path
        self.wineprefix_path = wineprefix_path

        self.popres_exe = current_dir + '/game/popres.exe'
        
        self.get_global_settings()
        self.config_load()
        self.create_main_window()
        
    def get_global_settings(self):
    
        global_config_file = os.getenv('HOME') + '/.games_nebula/config/config.ini'
        global_config_parser = ConfigParser.ConfigParser()
        global_config_parser.read(global_config_file)
        gtk_theme = global_config_parser.get('visuals', 'gtk_theme')
        gtk_dark = global_config_parser.getboolean('visuals', 'gtk_dark')
        icon_theme = global_config_parser.get('visuals', 'icon_theme')
        font = global_config_parser.get('visuals','font')
        screen = Gdk.Screen.get_default()
        gsettings = Gtk.Settings.get_for_screen(screen)
        gsettings.set_property('gtk-theme-name', gtk_theme)
        gsettings.set_property('gtk-application-prefer-dark-theme', gtk_dark)
        gsettings.set_property('gtk-icon-theme-name', icon_theme)
        gsettings.set_property('gtk-font-name', font)
        
    def config_load(self):
        
        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)
        
        if not config_parser.has_section('Settings'):
            self.exe = 'D3DPopTB.exe'

            config_parser.add_section('Settings')
            config_parser.set('Settings', 'exe', self.exe)

            new_config_file = open(config_file, 'w')
            config_parser.write(new_config_file)
            new_config_file.close()
        
        else:
            self.exe = config_parser.get('Settings', 'exe')

    def create_main_window(self):
        
        self.main_window = Gtk.Window(
            title = self._("Populous: The Beginning"), 
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            )
        self.main_window.connect('delete-event', self.quit_app)
        
        box_main = Gtk.Box(
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            spacing = 10,
            orientation = Gtk.Orientation.VERTICAL
            )
        
        frame_launch = Gtk.Frame(
            label = self._("Launch options"),
            label_xalign = 0.5
            )
        
        box_launch = Gtk.Box(
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            spacing = 10,
            orientation = Gtk.Orientation.VERTICAL
            )
        
        radiobutton_d3dpoptb = Gtk.RadioButton(
            label = self._("Populous: The Beginning"),
            name = 'D3DPopTB.exe'
            )

        radiobutton_poptb = Gtk.RadioButton(
            label = self._("Populous: The Beginning (software rendering)"),
            name = 'popTB.exe'
            )
        radiobutton_poptb.join_group(radiobutton_d3dpoptb)

        radiobutton_d3dpoptbuw = Gtk.RadioButton(
            label = self._("Populous: Undiscovered Worlds"),
            name = 'D3DPopTBUW.exe'
            )
        radiobutton_d3dpoptbuw.join_group(radiobutton_d3dpoptb)
        
        radiobutton_poptbuw = Gtk.RadioButton(
            label = self._("Populous: Undiscovered Worlds (software rendering)"),
            name = 'popTBUW.exe'
            )
        radiobutton_poptbuw.join_group(radiobutton_d3dpoptb)

        box_launch.pack_start(radiobutton_d3dpoptb, True, True, 0)
        box_launch.pack_start(radiobutton_poptb, True, True, 0)
        box_launch.pack_start(radiobutton_d3dpoptbuw, True, True, 0)
        box_launch.pack_start(radiobutton_poptbuw, True, True, 0)
        frame_launch.add(box_launch)
        
        for radiobutton in box_launch.get_children():
            if radiobutton.get_name() == self.exe:
                radiobutton.set_active(True)
        
        radiobutton_d3dpoptb.connect('clicked', self.cb_radiobuttons)
        radiobutton_poptb.connect('clicked', self.cb_radiobuttons)
        radiobutton_d3dpoptbuw.connect('clicked', self.cb_radiobuttons)
        radiobutton_poptbuw.connect('clicked', self.cb_radiobuttons)
        
        frame_patches = Gtk.Frame(
            label =self. _("Patches"),
            label_xalign = 0.5
            )
        
        box_patches = Gtk.Box(
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            orientation = Gtk.Orientation.VERTICAL
            )
        
        button_res_changer = Gtk.Button(
            label = self._("Resolution Changer")
            )
        button_res_changer.connect('clicked', self.cb_button_res_changer)
        
        if not os.path.exists(self.popres_exe):
            button_res_changer.set_sensitive(False)
            
        linkbutton = Gtk.LinkButton(
            label = self._("More patches"),
            uri = 'https://www.popre.net/downloads.php#patches',
            )
            
        box_patches.pack_start(button_res_changer, True, True, 0)
        box_patches.pack_start(linkbutton, True, True, 0)
        frame_patches.add(box_patches)
        
        button_ok = Gtk.Button(
            label = self._("OK")
            )
        button_ok.connect('clicked', self.cb_button_ok)

        box_main.pack_start(frame_launch, True, True, 0)
        box_main.pack_start(frame_patches, True, True, 0)
        box_main.pack_start(button_ok, True, True, 0)
        
        self.main_window.add(box_main)
        self.main_window.show_all()
 
    def modify_start_file(self):

        new_launch_command = 'python "$NEBULA_DIR/launcher_wine.py" populous_the_beginning "' \
        + self.exe + ' -allres"'

        start_file = open(current_dir + '/start.sh', 'r')
        start_file_content = start_file.readlines()
        start_file.close()
        
        for i in range(len(start_file_content)):
            if '.exe' in start_file_content[i]:
                start_file_content[i] = new_launch_command
                
        start_file = open(current_dir + '/start.sh', 'w')
        start_file.writelines(start_file_content)
        start_file.close()
    
    def cb_radiobuttons(self, radiobutton):
        self.exe = radiobutton.get_name()
    
    def cb_button_ok(self, button):
        
        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)
        
        config_parser.set('Settings', 'exe', self.exe)
        
        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()
        
        self.modify_start_file()
        
        Gtk.main_quit()
    
    def cb_button_res_changer(self, button):
        
        if self.wine_path == 'wine':
            export_command = 'export WINELOADER=wine && ' + \
            'export WINEPREFIX=' + self.wineprefix_path
        else:
            export_command = 'export WINE=' + self.wine_path + '/bin/wine && ' + \
            'export WINELOADER=' + self.wine_path + '/bin/wine && ' + \
            'export WINESERVER=' + self.wine_path + '/bin/wineserver && ' + \
            'export WINEDLLPATH=' + self.wine_path + '/lib && ' + \
            'export WINEPREFIX=' + self.wineprefix_path

        launch_command = '"$WINELOADER" "' + self.popres_exe + '"'
            
        self.main_window.hide()

        while Gtk.events_pending():
            Gtk.main_iteration()

        os.system(export_command + '\n' + launch_command)
        
        self.main_window.show()

    def quit_app(self, window, event):
        Gtk.main_quit()

def main():
    import sys
    app = GUI(sys.argv[1], sys.argv[2], sys.argv[3])
    Gtk.main()
        
if __name__ == '__main__':
    sys.exit(main())