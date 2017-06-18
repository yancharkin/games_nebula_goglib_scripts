#!/usr/bin/env python2
# -*- Mode: Python; coding: utf-8; -*-

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import ConfigParser
import gettext
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
        self.config_load()
        self.create_main_window()
        self.create_window_hires()

    def config_load(self):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('Settings'):
            config_parser.add_section('Settings')

        if not config_parser.has_option('Settings', 'module'):
            self.module = 'arcanum'
            config_parser.set('Settings', 'module', self.module)
        else:
            self.module = config_parser.get('Settings', 'module')

        if not config_parser.has_option('Settings', 'scrolling_distance'):
            self.scrolling_distance = 10
            config_parser.set('Settings', 'scrolling_distance', self.scrolling_distance)
        else:
            self.scrolling_distance = config_parser.getint('Settings', 'scrolling_distance')

        if not config_parser.has_option('Settings', 'scrolling_speed'):
            self.scrolling_speed = 35
            config_parser.set('Settings', 'scrolling_speed', self.scrolling_speed)
        else:
            self.scrolling_speed = config_parser.getint('Settings', 'scrolling_speed')

        if not config_parser.has_option('Settings', 'no3d'):
            self.no3d = False
            config_parser.set('Settings', 'no3d', self.no3d)
        else:
            self.no3d = config_parser.getboolean('Settings', 'no3d')

        if not config_parser.has_option('Settings', 'doublebuffer'):
            self.doublebuffer = False
            config_parser.set('Settings', 'doublebuffer', self.doublebuffer)
        else:
            self.doublebuffer = config_parser.getboolean('Settings', 'doublebuffer')

        if not config_parser.has_option('Settings', 'fullscreen'):
            self.fullscreen = False
            config_parser.set('Settings', 'fullscreen', self.fullscreen)
        else:
            self.fullscreen = config_parser.getboolean('Settings', 'fullscreen')

        if not config_parser.has_option('Settings', 'nosound'):
            self.nosound = False
            config_parser.set('Settings', 'nosound', self.nosound)
        else:
            self.nosound = config_parser.getboolean('Settings', 'nosound')

        if not config_parser.has_option('Settings', 'norandom'):
            self.norandom = False
            config_parser.set('Settings', 'norandom', self.norandom)
        else:
            self.norandom = config_parser.getboolean('Settings', 'norandom')

        if not config_parser.has_option('Settings', 'fps'):
            self.fps = False
            config_parser.set('Settings', 'fps', self.fps)
        else:
            self.fps = config_parser.getboolean('Settings', 'fps')

        if not config_parser.has_option('Settings', 'msmousez'):
            self.msmousez = False
            config_parser.set('Settings', 'msmousez', self.msmousez)
        else:
            self.msmousez = config_parser.getboolean('Settings', 'msmousez')

        if not config_parser.has_option('Settings', 'mpautojoin'):
            self.mpautojoin = False
            config_parser.set('Settings', 'mpautojoin', self.mpautojoin)
        else:
            self.mpautojoin = config_parser.getboolean('Settings', 'mpautojoin')

        if not config_parser.has_option('Settings', 'mpnobcast'):
            self.mpnobcast = False
            config_parser.set('Settings', 'mpnobcast', self.mpnobcast)
        else:
            self.mpnobcast = config_parser.getboolean('Settings', 'mpnobcast')


        if not config_parser.has_section('HiRes Patch'):
            config_parser.add_section('HiRes Patch')

        if not config_parser.has_option('HiRes Patch', 'hires_applied'):
            self.hires_applied = False
        else:
            self.hires_applied = config_parser.getboolean('HiRes Patch', 'hires_applied')

        if not config_parser.has_option('HiRes Patch', 'width'):
            self.width = ''
            config_parser.set('HiRes Patch', 'width', self.width)
        else:
            self.width = config_parser.get('HiRes Patch', 'width')

        if not config_parser.has_option('HiRes Patch', 'height'):
            self.height = ''
            config_parser.set('HiRes Patch', 'height', self.height)
        else:
            self.height = config_parser.get('HiRes Patch', 'height')

        if not config_parser.has_option('HiRes Patch', 'dialog_font'):
            self.dialog_font = _("default")
            config_parser.set('HiRes Patch', 'dialog_font', self.dialog_font)
        else:
            self.dialog_font = config_parser.get('HiRes Patch', 'dialog_font')

        if not config_parser.has_option('HiRes Patch', 'large_logbook'):
            self.large_logbook = False
            config_parser.set('HiRes Patch', 'large_logbook', self.large_logbook)
        else:
            self.large_logbook = config_parser.getboolean('HiRes Patch', 'large_logbook')

        if not config_parser.has_option('HiRes Patch', 'compact'):
            self.compact = False
            config_parser.set('HiRes Patch', 'compact', self.compact)
        else:
            self.compact = config_parser.getboolean('HiRes Patch', 'compact')

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

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

        new_launch_command = 'python2 "$NEBULA_DIR/launcher_wine.py" ' + \
        'arcanum_of_steamworks_and_magick_obscura "arcanum.exe' + ' ' + parameters_str + '"'

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

        if not config_parser.has_section('HiRes Patch'):
            config_parser.add_section('HiRes Patch')

        config_parser.set('HiRes Patch', 'width', self.width)
        config_parser.set('HiRes Patch', 'height', self.height)
        config_parser.set('HiRes Patch', 'dialog_font', self.dialog_font)
        config_parser.set('HiRes Patch', 'large_logbook', self.large_logbook)
        config_parser.set('HiRes Patch', 'compact', self.compact)

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


        label_module = Gtk.Label(
            halign = Gtk.Align.START,
            label = _("Module to run at startup:")
            )

        self.combobox_module = Gtk.ComboBoxText(
            hexpand = True
            )
        self.populate_modules_list()

        label_scrolling_distance = Gtk.Label(
            halign = Gtk.Align.START,
            label = _("Scrolling distance:"),
            )

        self.adjustment_scrolling_distance = Gtk.Adjustment(int(self.scrolling_distance), 0, 100, 1, 10)

        scale_scrolling_distance = Gtk.Scale(
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

        label_scrolling_speed = Gtk.Label(
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
            label = _("Software rendering mode"),
            halign = Gtk.Align.START,
            name = '-no3d',
            active = self.no3d
            )

        self.checkbutton_fullscreen = Gtk.CheckButton(
            label = _("Compact UI"),
            halign = Gtk.Align.START,
            name = '-fullscreen',
            active = self.fullscreen
            )

        self.checkbutton_doublebuffer = Gtk.CheckButton(
            label = _("Doublebuffer"),
            halign = Gtk.Align.START,
            name = '-doublebuffer',
            active = self.doublebuffer
            )

        self.checkbutton_nosound = Gtk.CheckButton(
            label = _("No sound"),
            halign = Gtk.Align.START,
            name = '-nosound',
            active = self.nosound
            )

        self.checkbutton_norandom = Gtk.CheckButton(
            label = _("No random encounters"),
            halign = Gtk.Align.START,
            name = '-norandom',
            active = self.norandom
            )

        self.checkbutton_fps = Gtk.CheckButton(
            label = _("Show FPS"),
            halign = Gtk.Align.START,
            name = '-fps',
            active = self.fps
            )

        self.checkbutton_msmousez = Gtk.CheckButton(
            label = _("Alternative mouse wheel behavior"),
            halign = Gtk.Align.START,
            name = '-msmousez',
            active = self.msmousez
            )

        self.checkbutton_mpautojoin = Gtk.CheckButton(
            label = _("Multiplayer - AutoJoin"),
            halign = Gtk.Align.START,
            name = '-mpautojoin',
            active = self.mpautojoin
            )

        self.checkbutton_mpnobcast = Gtk.CheckButton(
            label = _("Multiplayer - NoBroadcast"),
            halign = Gtk.Align.START,
            name = '-mpnobcast',
            active = self.mpnobcast
            )

        grid1 = Gtk.Grid(
            row_spacing = 5,
            column_spacing = 10,
            #row_homogeneous = True
            )

        grid1.attach(label_module, 0, 0, 1, 1)
        grid1.attach(self.combobox_module, 1, 0, 1, 1)
        grid1.attach(label_scrolling_distance, 0, 1, 1, 1)
        grid1.attach(scale_scrolling_distance, 1, 1, 1, 1)
        grid1.attach(label_scrolling_speed, 0, 2, 1, 1)
        grid1.attach(self.scale_scrolling_speed, 1, 2, 1, 1)
        grid1.attach(self.checkbutton_no3d, 0, 3, 2, 1)
        grid1.attach(self.checkbutton_doublebuffer, 0, 4, 2, 1)

        expander = Gtk.Expander(
            label = _("More options"),
            margin_top = 5
            )

        expander.connect('activate', self.cb_expander)

        self.grid2 = Gtk.Grid(
            margin_top = 10,
            row_spacing = 5,
            column_spacing = 10,
            #row_homogeneous = True
            )

        self.grid2.attach(self.checkbutton_fullscreen, 0, 0, 2, 1)
        self.grid2.attach(self.checkbutton_nosound, 0, 1, 2, 1)
        self.grid2.attach(self.checkbutton_norandom, 0, 2, 2, 1)
        self.grid2.attach(self.checkbutton_fps, 0, 3, 2, 1)
        self.grid2.attach(self.checkbutton_msmousez, 0, 4, 2, 1)
        self.grid2.attach(self.checkbutton_mpautojoin, 0, 5, 2, 1)
        self.grid2.attach(self.checkbutton_mpnobcast, 0, 6, 2, 1)

        expander.add(self.grid2)

        self.button_save = Gtk.Button(
            label = _("Save and quit"),
            margin_top = 10
            )
        self.button_save.connect('clicked', self.cb_button_save)

        self.button_uap = Gtk.Button(
            label = _("Unofficial Patch"),
            margin_top = 10
            )
        self.button_uap.connect('clicked', self.cb_button_uap)

        self.button_hires = Gtk.Button(
            label = _("High Resolution Patch"),
            margin_top = 10
            )
        self.button_hires.connect('clicked', self.cb_button_hires)

        self.box_large = Gtk.Box(
            #spacing = 10,
            orientation = Gtk.Orientation.VERTICAL,
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            )

        self.box_large.pack_start(grid1, True, True, 0)
        self.box_large.pack_start(expander, True, True, 0)
        self.box_large.pack_start(self.button_uap, True, True, 0)
        self.box_large.pack_start(self.button_hires, True, True, 0)
        self.box_large.pack_start(self.button_save, True, True, 0)

        self.main_window.add(self.box_large)
        self.main_window.show_all()

    def create_window_hires(self):

        self.window_hires = Gtk.Window(
            title = _("Arcanum"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            )
        self.window_hires.connect('delete-event', self.hide_window)

        grid = Gtk.Grid(
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            row_spacing = 10,
            column_spacing = 10,
            )

        label_res = Gtk.Label(
            label = _("Resolution: ")
            )

        entry_width = Gtk.Entry(
            placeholder_text = _("Width"),
            max_length = 4,
            xalign = 0.5,
            text = self.width
            )
        entry_width.connect('changed', self.cb_entry_width)

        entry_height = Gtk.Entry(
            placeholder_text = _("Height"),
            max_length = 4,
            xalign = 0.5,
            text = self.height
            )
        entry_height.connect('changed', self.cb_entry_height)

        label_dialog_font = Gtk.Label(
            label = _("Dialog font: ")
            )

        combobox_dialog_font = Gtk.ComboBoxText()

        font_size = [_("default"), '14', '18']

        font_index = 0
        for i in range(len(font_size)):
            combobox_dialog_font.append_text(font_size[i])
            if font_size[i] == self.dialog_font:
                font_index = i
        combobox_dialog_font.set_active(font_index)

        combobox_dialog_font.connect('changed', self.cb_combobox_dialog_font)

        checkbutton_larger_logbook_font = Gtk.CheckButton(
            label = _("Larger logbook font"),
            active = self.large_logbook
            )
        checkbutton_larger_logbook_font.connect('clicked', self.cb_checkbutton_larger_logbook_font)

        checkbutton_compact_opt_screen = Gtk.CheckButton(
            label = _("Compact options screen"),
            active = self.compact
            )
        checkbutton_compact_opt_screen.connect('clicked', self.cb_checkbutton_compact_opt_screen)

        button_patch = Gtk.Button(
            label = _("Patch")
            )
        button_patch.connect('clicked', self.cb_button_patch)

        grid.attach(label_res, 0, 0, 1, 1)
        grid.attach(entry_width, 1, 0, 1, 1)
        grid.attach(entry_height, 2, 0, 1, 1)
        grid.attach(label_dialog_font, 0, 1, 1, 1)
        grid.attach(combobox_dialog_font, 1, 1, 2, 1)
        grid.attach(checkbutton_larger_logbook_font, 0, 2, 3, 1)
        grid.attach(checkbutton_compact_opt_screen, 0, 3, 3, 1)
        grid.attach(button_patch, 0, 4, 3, 1)

        self.window_hires.add(grid)

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

    def hide_window(self, window, event):
        window.hide()
        self.main_window.show()
        return True

    def cb_expander(self, expander):
        if expander.get_expanded() == False:
            expander.remove(self.grid2)
            self.box_large.remove(expander)
            self.box_large.remove(self.button_save)
            self.box_large.remove(self.button_uap)
            self.box_large.remove(self.button_hires)
            self.box_large.pack_start(self.grid2, True, True, 0)
            self.box_large.pack_start(self.button_uap, True, True, 0)
            self.box_large.pack_start(self.button_hires, True, True, 0)
            self.box_large.pack_start(self.button_save, True, True, 0)

            self.grid2.set_property('margin-top', 5)

    def cb_button_save(self, button):
        self.config_save()
        Gtk.main_quit()

    def cb_button_uap(self, button):

        game_dir = current_dir + '/game'
        game_dir_win = 'Z:\\' + game_dir.replace('/', '\\')

        launch_command = '"$WINELOADER" "' + current_dir + \
        '/game/uap091225.exe" /D="' + game_dir_win + '"'

        self.main_window.hide()

        message_dialog = Gtk.MessageDialog(
            self.main_window,
            0,
            Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK,
            _("Attention")
            )
        message_dialog.format_secondary_text(_("Do not change default installation path"))
        content_area = message_dialog.get_content_area()
        content_area.set_property('margin-left', 10)
        content_area.set_property('margin-right', 10)
        content_area.set_property('margin-top', 10)
        content_area.set_property('margin-bottom', 10)
        message_dialog.run()
        message_dialog.destroy()

        while Gtk.events_pending():
            Gtk.main_iteration()

        os.system(launch_command)

        self.main_window.show()

    def cb_button_hires(self, button):
        self.main_window.hide()
        self.window_hires.show_all()

    def cb_entry_width(self, entry):
        text = entry.get_text().strip()
        new_text = (''.join([i for i in text if i in '0123456789']))
        entry.set_text(new_text)
        self.width = new_text

    def cb_entry_height(self, entry):
        text = entry.get_text().strip()
        new_text = (''.join([i for i in text if i in '0123456789']))
        entry.set_text(new_text)
        self.height = new_text

    def cb_combobox_dialog_font(self, combobox):
        self.dialog_font = combobox.get_active_text()

    def cb_checkbutton_larger_logbook_font(self, checkbutton):
        self.large_logbook = checkbutton.get_active()

    def cb_checkbutton_compact_opt_screen(self, checkbutton):
        self.compact = checkbutton.get_active()

    def cb_button_patch(self, button):
        self.config_save()

        cd_command = 'cd ' + current_dir + '/game'

        if self.compact == True:
            compact = 'y'
        else:
            compact = 'n'

        if self.hires_applied == False:

            if self.large_logbook == True:
                large_logbook = 'i'
            else:
                large_logbook = 'n'

            if self.dialog_font != _("default"):

                if self.dialog_font == '14':
                    dialog_font = '1'
                elif self.dialog_font == '18':
                    dialog_font = '2'

                patch_command = "printf 'n\ni\n" + self.width + "\n" + self.height + \
                "\n"+ compact +"\ny\n" + dialog_font + "\n" + large_logbook +"\n'" + \
                '| ./weidu --nogame ./setup-highres.tp2'

            else:
                patch_command = "printf 'n\ni\n" + self.width + "\n" + self.height + \
                "\n"+ compact +"\nn\n" + large_logbook +"\n'" + \
                '| ./weidu --nogame ./setup-highres.tp2'

        elif self.hires_applied == True:

            if self.large_logbook == True:
                large_logbook = 'i'
            else:
                large_logbook = 'u'

            if self.dialog_font != _("default"):

                if self.dialog_font == '14':
                    dialog_font = '1'
                elif self.dialog_font == '18':
                    dialog_font = '2'

                patch_command = "printf 'i\n" + self.width + "\n" + self.height + \
                "\n"+ compact +"\ni\n" + dialog_font + "\n" + large_logbook +"\n'" + \
                ' | ./weidu --nogame ./setup-highres.tp2'

            else:
                patch_command = "printf 'i\n" + self.width + "\n" + self.height + \
                "\n"+ compact +"\nu\n" + large_logbook +"\n'" + \
                ' | ./weidu --nogame ./setup-highres.tp2'

        os.system(cd_command + ' && ' + patch_command)

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('HiRes Patch'):
            config_parser.add_section('HiRes Patch')
        config_parser.set('HiRes Patch', 'hires_applied', True)

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

        self.window_hires.hide()
        self.main_window.show()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
