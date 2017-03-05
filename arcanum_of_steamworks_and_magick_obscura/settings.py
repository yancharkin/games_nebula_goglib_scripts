#!/usr/bin/env python2
# -*- Mode: Python; coding: utf-8; indent-tabs-install_mode: t; c-basic-offset: 4; tab-width: 4 -*- 

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import ConfigParser
import gettext

current_dir = sys.path[0]

gettext.bindtextdomain('arcanum', current_dir + '/locale')
gettext.textdomain('arcanum')
_ = gettext.gettext

class GUI:

	def __init__(self, wine_path, wineprefix_path):

		self.wine_path = wine_path
		self.wineprefix_path = wineprefix_path
		
		if self.wine_path == 'wine':
			self.export_command = 'export WINELOADER=wine && ' + \
			'export WINEPREFIX=' + self.wineprefix_path
		else:
			self.export_command = 'export WINE=' + self.wine_path + '/bin/wine && ' + \
			'export WINELOADER=' + self.wine_path + '/bin/wine && ' + \
			'export WINESERVER=' + self.wine_path + '/bin/wineserver && ' + \
			'export WINEDLLPATH=' + self.wine_path + '/lib && ' + \
			'export WINEPREFIX=' + self.wineprefix_path

		self.get_global_settings()
		self.config_load()
		self.create_main_window()
		
	def get_global_settings(self):
	
		global_config_file = os.getenv('HOME') + '/.games_nebula/config/config.ini'
		global_config_parser = ConfigParser.ConfigParser()
		global_config_parser.read(global_config_file)
		gtk_theme = global_config_parser.get('Visuals', 'gtk_theme')
		gtk_dark = global_config_parser.getboolean('Visuals', 'gtk_dark')
		icon_theme = global_config_parser.get('Visuals', 'icon_theme')
		font = global_config_parser.get('Visuals','font')
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
			
			self.module = 'arcanum'
			self.scrolling_distance = 10
			self.scrolling_speed = 35
			self.no3d = False
			self.doublebuffer = False
			self.fullscreen = False
			self.nosound = False
			self.norandom = False
			self.fps = False
			self.msmousez = False
			self.mpautojoin = False
			self.mpnobcast = False

			config_parser.add_section('Settings')
			config_parser.set('Settings', 'module', self.module)
			config_parser.set('Settings', 'scrolling_distance', self.scrolling_distance)
			config_parser.set('Settings', 'scrolling_speed', self.scrolling_speed)
			config_parser.set('Settings', 'no3d', self.no3d)
			config_parser.set('Settings', 'doublebuffer', self.doublebuffer)
			config_parser.set('Settings', 'fullscreen', self.fullscreen)
			config_parser.set('Settings', 'nosound', self.nosound)
			config_parser.set('Settings', 'norandom', self.norandom)
			config_parser.set('Settings', 'fps', self.fps)
			config_parser.set('Settings', 'msmousez', self.msmousez)
			config_parser.set('Settings', 'mpautojoin', self.mpautojoin)
			config_parser.set('Settings', 'mpnobcast', self.mpnobcast)

			new_config_file = open(config_file, 'w')
			config_parser.write(new_config_file)
			new_config_file.close()
		
		else:
			
			self.module = config_parser.get('Settings', 'module')
			self.scrolling_distance = config_parser.getint('Settings', 'scrolling_distance')
			self.scrolling_speed = config_parser.getint('Settings', 'scrolling_speed')
			self.no3d = config_parser.getboolean('Settings', 'no3d')
			self.doublebuffer = config_parser.getboolean('Settings', 'doublebuffer')
			self.fullscreen = config_parser.getboolean('Settings', 'fullscreen')
			self.nosound = config_parser.getboolean('Settings', 'nosound')
			self.norandom = config_parser.getboolean('Settings', 'norandom')
			self.fps = config_parser.getboolean('Settings', 'fps')
			self.msmousez = config_parser.getboolean('Settings', 'msmousez')
			self.mpautojoin = config_parser.getboolean('Settings', 'mpautojoin')
			self.mpnobcast = config_parser.getboolean('Settings', 'mpnobcast')
			
	def config_save(self):
		
		parameters_list = []

		self.scrolling_distance = int(self.adjustment_scrolling_distance.get_value())
		if self.scrolling_distance != 10:
			parameters_list.append('-scrolldist:' + str(int(self.scrolling_distance)))
		
		self.scrolling_speed = int(self.adjustment_scrolling_speed.get_value())
		if self.scrolling_speed != 35:
			parameters_list.append('-scrollfps:' + str(int(self.scrolling_speed)))
		
		self.no3d = self.checkbutton_no3d.get_active()
		if self.no3d:
			parameters_list.append(self.checkbutton_no3d.get_name())
		
		self.doublebuffer = self.checkbutton_doublebuffer.get_active()
		if self.doublebuffer:
			parameters_list.append(self.checkbutton_doublebuffer.get_name())
		
		self.fullscreen = self.checkbutton_fullscreen.get_active()
		if self.fullscreen:
			parameters_list.append(self.checkbutton_fullscreen.get_name())
		
		self.nosound = self.checkbutton_nosound.get_active()
		if self.nosound:
			parameters_list.append(self.checkbutton_nosound.get_name())
		
		self.norandom = self.checkbutton_norandom.get_active()
		if self.norandom:
			parameters_list.append(self.checkbutton_norandom.get_name())
		
		self.fps = self.checkbutton_fps.get_active()
		if self.fps:
			parameters_list.append(self.checkbutton_fps.get_name())
		
		self.msmousez = self.checkbutton_msmousez.get_active()
		if self.msmousez:
			parameters_list.append(self.checkbutton_msmousez.get_name())
		
		self.mpautojoin = self.checkbutton_mpautojoin.get_active()
		if self.mpautojoin:
			parameters_list.append(self.checkbutton_mpautojoin.get_name())
		
		self.mpnobcast = self.checkbutton_mpnobcast.get_active()
		if self.mpnobcast:
			parameters_list.append(self.checkbutton_mpnobcast.get_name())
			
		self.module = self.combobox_module.get_active_text()
		if self.module != 'arcanum':
			parameters_list.append('-mod:' + self.module)
			
		parameters_str = ' '.join(parameters_list)

		new_launch_command = 'python $NEBULA_DIR/launcher_wine.py ' + \
		'arcanum_of_steamworks_and_magick_obscura "arcanum.exe' + ' ' + parameters_str + '"'

		start_file = open(current_dir + '/start.sh', 'r')
		start_file_content = start_file.readlines()
		start_file.close()
		
		for i in range(len(start_file_content)):
			if 'Arcanum.exe' in start_file_content[i]:
				start_file_content[i] = new_launch_command
				
		start_file = open(current_dir + '/start.sh', 'w')
		start_file.writelines(start_file_content)
		start_file.close()

		config_file = current_dir + '/settings.ini'
		config_parser = ConfigParser.ConfigParser()
		config_parser.read(config_file)
		
		config_parser.set('Settings', 'module', self.module)
		config_parser.set('Settings', 'scrolling_distance', self.scrolling_distance)
		config_parser.set('Settings', 'scrolling_speed', self.scrolling_speed)
		config_parser.set('Settings', 'no3d', self.no3d)
		config_parser.set('Settings', 'doublebuffer', self.doublebuffer)
		config_parser.set('Settings', 'fullscreen', self.fullscreen)
		config_parser.set('Settings', 'nosound', self.nosound)
		config_parser.set('Settings', 'norandom', self.norandom)
		config_parser.set('Settings', 'fps', self.fps)
		config_parser.set('Settings', 'msmousez', self.msmousez)
		config_parser.set('Settings', 'mpautojoin', self.mpautojoin)
		config_parser.set('Settings', 'mpnobcast', self.mpnobcast)
		
		new_config_file = open(config_file, 'w')
		config_parser.write(new_config_file)
		new_config_file.close()

	def quit_app(self, window, event):
		Gtk.main_quit()

	def create_main_window(self):
		
		self.main_window = Gtk.Window(
			title = _("Arcanum"), 
			type = Gtk.WindowType.TOPLEVEL,
			window_position = Gtk.WindowPosition.CENTER_ALWAYS,
			resizable = False,
			)
		self.main_window.connect('delete-event', self.quit_app)
		
		
		self.label_module = Gtk.Label(
			halign = Gtk.Align.START,
			label = _("Module to run at startup:")
			)
		
		self.combobox_module = Gtk.ComboBoxText(
			hexpand = True
			)
		self.populate_modules_list()
		
		self.label_scrolling_distance = Gtk.Label(
			halign = Gtk.Align.START,
			label = _("Scrolling distance:"),
			)
		
		self.adjustment_scrolling_distance = Gtk.Adjustment(int(self.scrolling_distance), 0, 100, 1, 10)
		
		self.scale_scrolling_distance = Gtk.Scale(
			width_request = 150,
			orientation = Gtk.Orientation.HORIZONTAL,
			draw_value = True,
			value_pos = Gtk.PositionType.RIGHT,
			show_fill_level = True,
			adjustment = self.adjustment_scrolling_distance,
			digits = 0,
			round_digits = 0,
			hexpand = True
			)
		
		self.label_scrolling_speed = Gtk.Label(
			halign = Gtk.Align.START,
			label = _("Scrolling speed:")
			)
		
		self.adjustment_scrolling_speed = Gtk.Adjustment(int(self.scrolling_speed), 0, 100, 1, 10)
		
		self.scale_scrolling_speed = Gtk.Scale(
			width_request = 150,
			orientation = Gtk.Orientation.HORIZONTAL,
			draw_value = True,
			value_pos = Gtk.PositionType.RIGHT,
			show_fill_level = True,
			adjustment = self.adjustment_scrolling_speed,
			digits = 0,
			round_digits = 0,
			hexpand = True
			)
		
		self.checkbutton_no3d = Gtk.CheckButton(
			halign = Gtk.Align.START,
			name = '-no3d',
			active = self.no3d
			)
		
		self.label_no3d = Gtk.Label(
			halign = Gtk.Align.START,
			label = _("Software rendering mode")
			)
		
		self.checkbutton_fullscreen = Gtk.CheckButton(
			halign = Gtk.Align.START,
			name = '-fullscreen',
			active = self.fullscreen
			)
		
		self.label_fullscreen = Gtk.Label(
			halign = Gtk.Align.START,
			label = _("Compact UI")
			)
		
		self.checkbutton_doublebuffer = Gtk.CheckButton(
			halign = Gtk.Align.START,
			name = '-doublebuffer',
			active = self.doublebuffer
			)
		
		self.label_doublebuffer = Gtk.Label(
			halign = Gtk.Align.START,
			label = _("Doublebuffer")
			)
		
		self.checkbutton_nosound = Gtk.CheckButton(
			halign = Gtk.Align.START,
			name = '-nosound',
			active = self.nosound
			)
		
		self.label_nosound = Gtk.Label(
			halign = Gtk.Align.START,
			label = _("No sound")
			)
		
		self.checkbutton_norandom = Gtk.CheckButton(
			halign = Gtk.Align.START,
			name = '-norandom',
			active = self.norandom
			)
		
		self.label_norandom = Gtk.Label(
			halign = Gtk.Align.START,
			label = _("No random encounters")
			)
		
		self.checkbutton_fps = Gtk.CheckButton(
			halign = Gtk.Align.START,
			name = '-fps',
			active = self.fps
			)
		
		self.label_fps = Gtk.Label(
			halign = Gtk.Align.START,
			label = _("Show FPS")
			)
		
		self.checkbutton_msmousez = Gtk.CheckButton(
			halign = Gtk.Align.START,
			name = '-msmousez',
			active = self.msmousez
			)
		
		self.label_msmousez = Gtk.Label(
			halign = Gtk.Align.START,
			label = _("Alternative mouse wheel behavior")
			)
		
		self.checkbutton_mpautojoin = Gtk.CheckButton(
			halign = Gtk.Align.START,
			name = '-mpautojoin',
			active = self.mpautojoin
			)
		
		self.label_mpautojoin = Gtk.Label(
			halign = Gtk.Align.START,
			label = _("Multiplayer - AutoJoin")
			)
		
		self.checkbutton_mpnobcast = Gtk.CheckButton(
			halign = Gtk.Align.START,
			name = '-mpnobcast',
			active = self.mpnobcast
			)
		
		self.label_mpnobcast = Gtk.Label(
			halign = Gtk.Align.START,
			label = _("Multiplayer - NoBroadcast")
			)
		
		self.grid = Gtk.Grid(
			#halign = Gtk.Align.FILL,
			row_spacing = 5,
			column_spacing = 10,
			row_homogeneous = True
			)
		
		self.grid.attach(self.label_module, 1, 0, 1, 1)
		self.grid.attach(self.combobox_module, 2, 0, 1, 1)
		self.grid.attach(self.label_scrolling_distance, 1, 1, 1, 1)
		self.grid.attach(self.scale_scrolling_distance, 2, 1, 1, 1)
		self.grid.attach(self.label_scrolling_speed, 1, 2, 1, 1)
		self.grid.attach(self.scale_scrolling_speed, 2, 2, 1, 1)
		self.grid.attach(self.checkbutton_no3d, 0, 3, 1, 1)
		self.grid.attach(self.label_no3d, 1, 3, 2, 1)
		self.grid.attach(self.checkbutton_doublebuffer, 0, 4, 1, 1)
		self.grid.attach(self.label_doublebuffer, 1, 4, 2, 1)
		self.grid.attach(self.checkbutton_fullscreen, 0, 5, 1, 1)
		self.grid.attach(self.label_fullscreen, 1, 5, 2, 1)
		self.grid.attach(self.checkbutton_nosound, 0, 6, 1, 1)
		self.grid.attach(self.label_nosound, 1, 6, 2, 1)
		self.grid.attach(self.checkbutton_norandom, 0, 7, 1, 1)
		self.grid.attach(self.label_norandom, 1, 7, 2, 1)
		self.grid.attach(self.checkbutton_fps, 0, 8, 1, 1)
		self.grid.attach(self.label_fps, 1, 8, 2, 1)
		self.grid.attach(self.checkbutton_msmousez, 0, 9, 1, 1)
		self.grid.attach(self.label_msmousez, 1, 9, 2, 1)
		self.grid.attach(self.checkbutton_mpautojoin, 0, 10, 1, 1)
		self.grid.attach(self.label_mpautojoin, 1, 10, 2, 1)
		self.grid.attach(self.checkbutton_mpnobcast, 0, 11, 1, 1)
		self.grid.attach(self.label_mpnobcast, 1, 11, 2, 1)
	
		self.button_save = Gtk.Button(
			label = _("Save and quit")
			)
		self.button_save.connect('clicked', self.cb_button_save)
		
		self.button_quit = Gtk.Button(
			label = _("Quit without saving")
			)
		self.button_quit.connect('clicked', Gtk.main_quit)
		
		self.box_small = Gtk.Box(
			spacing = 5,
			orientation = Gtk.Orientation.HORIZONTAL,
			homogeneous = True
			)
			
		self.box_small.pack_start(self.button_quit, True, True, 0)
		self.box_small.pack_start(self.button_save, True, True, 0)
		
		self.box_large = Gtk.Box(
			spacing = 5,
			orientation = Gtk.Orientation.VERTICAL,
			margin_top = 5,
			margin_bottom = 5,
			margin_left = 5,
			margin_right = 5,
			)
			
		self.box_large.pack_start(self.grid, True, True, 0)
		self.box_large.pack_start(self.box_small, True, True, 0)
		
		self.main_window.add(self.box_large)
		
		self.main_window.show_all()

	
	def cb_button_save(self, button):
		self.config_save()
		Gtk.main_quit()
		
	def populate_modules_list(self):
		
		modules_list = []
		
		path = current_dir + '/game/modules'
		full_list = os.listdir(path)
		
		for file_name in full_list:
			if ('dat' in file_name) and (file_name.split('.')[0] not in modules_list):
				module_name = file_name.split('.')[0]
				modules_list.append(module_name)
				os.system('mkdir -p ' + path + '/' + module_name)
		
		modules_list = sorted(modules_list)
		
		for i in range(len(modules_list)):
			self.combobox_module.append_text(modules_list[i])
			if modules_list[i] == self.module:
				self.combobox_module.set_active(i)
		
def main():
	import sys
	app = GUI(sys.argv[1], sys.argv[2])
	Gtk.main()
		
if __name__ == '__main__':
	sys.exit(main())
