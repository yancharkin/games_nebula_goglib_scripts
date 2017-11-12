#!/usr/bin/env python2
# -*- Mode: Python; coding: utf-8; -*-

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import gettext
import ConfigParser
import imp

nebula_dir = os.getenv('NEBULA_DIR')

modules_dir = nebula_dir + '/modules'
set_visuals = imp.load_source('set_visuals', modules_dir + '/set_visuals.py')

gettext.bindtextdomain('games_nebula', nebula_dir + '/locale')
gettext.textdomain('games_nebula')
_ = gettext.gettext

current_dir = sys.path[0]
download_dir = os.getenv('DOWNLOAD_DIR')
install_dir = os.getenv('INSTALL_DIR')
game_dir = install_dir + '/pathologic/game'
wineloader = os.getenv('WINELOADER')
video_dir = current_dir + '/game/data/Video'
video_dir_bak = video_dir + '/bak'

os.system('mkdir -p ' + download_dir + '/_distr/pathologic')

class GUI:

    def __init__(self):

        if not os.path.exists(install_dir + '/pathologic/.ws_addon_installed'):
            self.create_window_1()
        else:
            self.config_load()
            self.create_window_2()

    def create_window_1(self):

        self.main_window = Gtk.Window(
            title = _("Pathologic"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 360
            )
        self.main_window.connect('delete-event', self.quit_app)

        box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            spacing = 10
            )

        self.button_config = Gtk.Button(label=_("Configuration"))
        self.button_config.connect('clicked', self.cb_button_config)

        frame_addon = Gtk.Frame(
            label = _("Widescreen Addon"),
            label_xalign = 0.5
            )

        box_frame_addon = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            spacing = 10
            )

        linkbutton_download = Gtk.LinkButton(
            label = _("Download"),
            uri = 'http://www.moddb.com/addons/start/49144?referer=http%3A%2F%2Fwww.moddb.com%2Fgames%2Fpathologic%2Faddons',
            )

        linkbutton_put = Gtk.LinkButton(
            label = _("Put it here"),
            uri = 'file://' + download_dir + '/_distr/pathologic',
            )

        self.button_patch = Gtk.Button(label=_("Install"))
        self.button_patch.connect('clicked', self.cb_button_patch)

        self.progressbar = Gtk.ProgressBar(
            hexpand = True,
            show_text = True,
            text = _("Processing..."),
            pulse_step = 0.1,
            no_show_all = True
            )

        box_frame_addon.pack_start(linkbutton_download, True, True, 0)
        box_frame_addon.pack_start(linkbutton_put, True, True, 0)
        box_frame_addon.pack_start(self.button_patch, True, True, 0)
        box_frame_addon.pack_start(self.progressbar, True, True, 0)

        frame_addon.add(box_frame_addon)

        box.pack_start(self.button_config, True, True, 0)
        box.pack_start(frame_addon, True, True, 0)

        self.main_window.add(box)
        self.main_window.show_all()

    def create_window_2(self):

        self.main_window = Gtk.Window(
            title = _("Pathologic"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 360
            )
        self.main_window.connect('delete-event', self.quit_app)

        grid = Gtk.Grid(
            orientation = Gtk.Orientation.VERTICAL,
            margin_left = 10,
            margin_right = 10,
            margin_top = 10,
            margin_bottom = 10,
            row_spacing = 10,
            column_spacing = 10,
            column_homogeneous = True
            )

        label_res = Gtk.Label(label="Resolution", xalign = 0)

        list_res = ['1280x800', '1360x768', '1366x768', '1440x900', '1600x900', \
                    '1680x1050', '1920x1080', '1920x1200']
        combobox_res = Gtk.ComboBoxText()
        cur_res = self.xres + 'x' + self.yres
        index = 0
        for i in range(len(list_res)):
            combobox_res.append_text(list_res[i])
            if list_res[i] == cur_res:
                index = i
        combobox_res.set_active(index)
        combobox_res.connect('changed', self.cb_combobox_res)


        label_color = Gtk.Label(label="Color", xalign = 0)

        list_color = ['16', '32']
        combobox_color = Gtk.ComboBoxText()
        for i in range(len(list_color)):
            combobox_color.append_text(list_color[i])
        combobox_color.set_active(int(self.depth32))
        combobox_color.connect('changed', self.cb_combobox_color)

        label_vsync = Gtk.Label(label="VSync", xalign = 0)
        switch_vsync = Gtk.Switch()
        switch_vsync.set_active(self.vsync)
        switch_vsync.connect('state-set', self.cb_switch_vsync)

        label_antialias = Gtk.Label(label="Antialiasing", xalign = 0)

        list_antialias = ['(disabled)', '2X', '4X', '8X', '16X']
        combobox_antialias = Gtk.ComboBoxText()
        for i in range(len(list_antialias)):
            combobox_antialias.append_text(list_antialias[i])
        combobox_antialias.set_active(self.antialias)
        combobox_antialias.connect('changed', self.cb_combobox_antialias)

        label_distance = Gtk.Label(label="Detail objects distance", xalign = 0)

        adj_distance = Gtk.Adjustment(self.distance, 0, 50, 1, 10)
        spinbutton_distance = Gtk.SpinButton(
            adjustment = adj_distance,
            numeric=True,
            digits=0,
            max_length = 2,
            )
        spinbutton_distance.connect('value-changed', self.cb_spinbutton_distance)

        label_anisotropy = Gtk.Label(label="Anisotropic filtering", xalign = 0)

        adj_anisotropy = Gtk.Adjustment(self.anisotropy, 0, 16, 1, 2)
        spinbutton_anisotropy = Gtk.SpinButton(
            adjustment = adj_anisotropy,
            numeric=True,
            digits=0,
            max_length = 2,
            )
        spinbutton_anisotropy.connect('value-changed', self.cb_spinbutton_anisotropy)

        label_tex = Gtk.Label(label="Texture quality", xalign = 0)

        list_tex = ['High', 'Low']
        combobox_tex = Gtk.ComboBoxText()
        for i in range(len(list_tex)):
            combobox_tex.append_text(list_tex[i])
        combobox_tex.set_active(self.tex)
        combobox_tex.connect('changed', self.cb_combobox_tex)

        button_save = Gtk.Button(label=_("Save and quit"))
        button_save.connect('clicked', self.cb_button_save)

        label_lightmap = Gtk.Label(label="Lightmap quality", xalign = 0)

        list_lightmap = ['High', 'Medium', 'Low']
        combobox_lightmap = Gtk.ComboBoxText()
        for i in range(len(list_lightmap)):
            combobox_lightmap.append_text(list_lightmap[i])
        combobox_lightmap.set_active(self.lightmap)
        combobox_lightmap.connect('changed', self.cb_combobox_lightmap)

        label_tex_comp = Gtk.Label(label="Texture compression", xalign = 0)
        switch_tex_comp = Gtk.Switch()
        if self.tex_comp == -1:
            tex_comp_bool = True
        else:
            tex_comp_bool = False
        switch_tex_comp.set_active(tex_comp_bool)
        switch_tex_comp.connect('state-set', self.cb_switch_tex_comp)

        label_decor = Gtk.Label(label="Decor", xalign = 0)
        switch_decor = Gtk.Switch()
        if self.decor == 1:
            decor_bool = True
        else:
            decor_bool = False
        switch_decor.set_active(decor_bool)
        switch_decor.connect('state-set', self.cb_switch_decor)

        label_nobumpmapping = Gtk.Label(label="Bump-mapping", xalign = 0)
        switch_nobumpmapping = Gtk.Switch()
        if self.nobumpmapping == 0:
            nobumpmapping_bool = True
        else:
            nobumpmapping_bool = False
        switch_nobumpmapping.set_active(nobumpmapping_bool)
        switch_nobumpmapping.connect('state-set', self.cb_switch_nobumpmapping)

        label_waterreflections = Gtk.Label(label="Water reflections", xalign = 0)
        switch_waterreflections = Gtk.Switch()
        if self.waterreflections == 1:
            waterreflections_bool = True
        else:
            waterreflections_bool = False
        switch_waterreflections.set_active(waterreflections_bool)
        switch_waterreflections.connect('state-set', self.cb_switch_waterreflections)

        label_enb = Gtk.Label(label="ENB Series mod", xalign = 0)
        switch_enb = Gtk.Switch()
        if self.enb == 1:
            enb_bool = True
        else:
            enb_bool = False
        switch_enb.set_active(enb_bool)
        switch_enb.connect('state-set', self.cb_switch_enb)

        button_save = Gtk.Button(label=_("Save and quit"))
        button_save.connect('clicked', self.cb_button_save)

        grid.attach(label_res, 0, 0, 1, 1)
        grid.attach(combobox_res, 1, 0, 1, 1)
        grid.attach(label_tex, 0, 1, 1, 1)
        grid.attach(combobox_tex, 1, 1, 1, 1)
        grid.attach(label_lightmap, 0, 2, 1, 1)
        grid.attach(combobox_lightmap, 1, 2, 1, 1)
        grid.attach(label_color, 0, 3, 1, 1)
        grid.attach(combobox_color, 1, 3, 1, 1)
        grid.attach(label_antialias, 0, 4, 1, 1)
        grid.attach(combobox_antialias, 1, 4, 1, 1)
        grid.attach(label_anisotropy, 0, 5, 1, 1)
        grid.attach(spinbutton_anisotropy, 1, 5, 1, 1)
        grid.attach(label_distance, 0, 6, 1, 1)
        grid.attach(spinbutton_distance, 1, 6, 1, 1)
        grid.attach(label_vsync, 0, 7, 1, 1)
        grid.attach(switch_vsync, 1, 7, 1, 1)
        grid.attach(label_tex_comp, 0, 8, 1, 1)
        grid.attach(switch_tex_comp, 1, 8, 1, 1)
        grid.attach(label_decor, 0, 9, 1, 1)
        grid.attach(switch_decor, 1, 9, 1, 1)
        grid.attach(label_nobumpmapping, 0, 10, 1, 1)
        grid.attach(switch_nobumpmapping, 1, 10, 1, 1)
        grid.attach(label_waterreflections, 0, 11, 1, 1)
        grid.attach(switch_waterreflections, 1, 11, 1, 1)
        grid.attach(label_enb, 0, 12, 1, 1)
        grid.attach(switch_enb, 1, 12, 1, 1)
        grid.attach(button_save, 0, 13, 2, 1)

        self.main_window.add(grid)
        self.main_window.show_all()

    def config_load(self):

        config_file_path = game_dir + '/data/config.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file_path)

        if not config_parser.has_section('Video'):
            config_parser.add_section('Video')

        if not config_parser.has_option('Video', 'XRes'):
            self.xres = '1366'
            config_parser.set('Video', 'XRes', self.xres)
        else:
            self.xres = config_parser.get('Video', 'XRes')
            if (self.xres == '800') or (self.xres == '1024'):
                self.xres = '1366'

        if not config_parser.has_option('Video', 'YRes'):
            self.yres = '768'
            config_parser.set('Video', 'YRes', self.yres)
        else:
            self.yres = config_parser.get('Video', 'YRes')
            if self.yres == '600':
                self.yres = '768'

        if not config_parser.has_option('Video', 'depth32'):
            self.depth32 = '0'
            config_parser.set('Video', 'depth32', self.depth32)
        else:
            self.depth32 = config_parser.get('Video', 'depth32')

        if not config_parser.has_option('Video', 'vsync'):
            self.vsync = False
            config_parser.set('Video', 'vsync', '0')
        else:
            vsync_value = config_parser.get('Video', 'vsync')
            if vsync_value == '1':
                self.vsync = True
            else:
                self.vsync = False

        if not config_parser.has_option('Video', 'antialias'):
            self.antialias = 0
            config_parser.set('Video', 'antialias', self.antialias)
        else:
            self.antialias = config_parser.getint('Video', 'antialias')

        if not config_parser.has_option('Video', 'distance'):
            self.distance = 0
            config_parser.set('Video', 'distance', self.distance)
        else:
            self.distance = config_parser.getint('Video', 'distance')

        if not config_parser.has_option('Video', 'texanisotropy'):
            self.anisotropy = 0
            config_parser.set('Video', 'texanisotropy', self.anisotropy)
        else:
            self.anisotropy = config_parser.getint('Video', 'texanisotropy')

        if not config_parser.has_option('Video', 'texturequality'):
            self.tex = 1
            config_parser.set('Video', 'texturequality', self.tex)
        else:
            self.tex = config_parser.getint('Video', 'texturequality')

        if not config_parser.has_option('Video', 'lightmapquality'):
            self.lightmap = 2
            config_parser.set('Video', 'lightmapquality', self.lightmap)
        else:
            self.lightmap = config_parser.getint('Video', 'lightmapquality')

        if not config_parser.has_option('Video', 'nocompressedtextures'):
            self.tex_comp = -1
            config_parser.set('Video', 'nocompressedtextures', self.tex_comp)
        else:
            self.tex_comp = config_parser.getint('Video', 'nocompressedtextures')

        if not config_parser.has_option('Video', 'eyecandy'):
            self.decor = 0
            config_parser.set('Video', 'eyecandy', self.decor)
        else:
            self.decor = config_parser.getint('Video', 'eyecandy')

        if not config_parser.has_option('Video', 'eyecandy'):
            self.decor = 0
            config_parser.set('Video', 'eyecandy', self.decor)
        else:
            self.decor = config_parser.getint('Video', 'eyecandy')

        if not config_parser.has_option('Video', 'nobumpmapping'):
            self.nobumpmapping = 1
            config_parser.set('Video', 'nobumpmapping', self.nobumpmapping)
        else:
            self.nobumpmapping = config_parser.getint('Video', 'nobumpmapping')

        if not config_parser.has_option('Video', 'waterreflections'):
            self.waterreflections = 0
            config_parser.set('Video', 'waterreflections', self.waterreflections)
        else:
            self.waterreflections = config_parser.getint('Video', 'waterreflections')

        if not config_parser.has_option('Video', 'enb'):
            self.enb = 0
            config_parser.set('Video', 'enb', self.enb)
        else:
            self.enb = config_parser.getint('Video', 'enb')

        config_file = open(config_file_path, 'w')
        config_parser.write(config_file)
        config_file.close()

        self.setup_enb()

    def config_save(self):

        config_file_path = game_dir + '/data/config.ini' # remove
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file_path) # remove

        config_parser.set('Video', 'XRes', self.xres)
        config_parser.set('Video', 'YRes', self.yres)
        config_parser.set('Video', 'depth32', self.depth32)

        if self.vsync == True:
            vsync_value = '1'
        else:
            vsync_value = '0'
        config_parser.set('Video', 'vsync', vsync_value)

        config_parser.set('Video', 'antialias', self.antialias)
        config_parser.set('Video', 'distance', self.distance)
        config_parser.set('Video', 'texanisotropy', self.anisotropy)
        config_parser.set('Video', 'texturequality', self.tex)
        config_parser.set('Video', 'lightmapquality', self.lightmap)
        config_parser.set('Video', 'nocompressedtextures', self.tex_comp)
        config_parser.set('Video', 'eyecandy', self.decor)
        config_parser.set('Video', 'nobumpmapping', self.nobumpmapping)
        config_parser.set('Video', 'waterreflections', self.waterreflections)
        config_parser.set('Video', 'enb', self.enb)

        self.setup_enb()

        config_file = open(config_file_path, 'w')
        config_parser.write(config_file)
        config_file.close()

    def cb_combobox_res(self, combobox):
        text = combobox.get_active_text()
        self.xres = text.split('x')[0]
        self.yres = text.split('x')[1]

    def cb_combobox_antialias(self, combobox):
        self.antialias = combobox.get_active()

    def cb_combobox_color(self, combobox):
        text = combobox.get_active_text()
        if text == '16':
            self.depth32 = '0'
        else:
            self.depth32 = '1'

    def cb_switch_vsync(self, switch, event):
        self.vsync = switch.get_active()

    def cb_spinbutton_distance(self, spinbutton):
        self.distance = spinbutton.get_value_as_int()

    def cb_spinbutton_anisotropy(self, spinbutton):
        self.anisotropy = spinbutton.get_value_as_int()

    def cb_combobox_tex(self, combobox):
        self.tex = combobox.get_active()

    def cb_combobox_lightmap(self, combobox):
        self.lightmap = combobox.get_active()

    def cb_switch_tex_comp(self, switch, event):
        value = switch.get_active()
        if value == True:
            self.tex_comp = -1
        else:
            self.tex_comp = 1

    def cb_switch_decor(self, switch, event):
        value = switch.get_active()
        if value == True:
            self.decor = 1
        else:
            self.decor = 0

    def cb_switch_nobumpmapping(self, switch, event):
        value = switch.get_active()
        if value == True:
            self.nobumpmapping = 0
        else:
            self.nobumpmapping = 1

    def cb_switch_waterreflections(self, switch, event):
        value = switch.get_active()
        if value == True:
            self.waterreflections = 1
        else:
            self.waterreflections = 0

    def cb_switch_enb(self, switch, event):
        value = switch.get_active()
        if value == True:
            self.enb = 1
        else:
            self.enb = 0

    def cb_button_patch(self, button):

        patch_path = download_dir + '/_distr/pathologic/Pathologic_Widescreen_Addon.exe'

        if not os.path.exists(patch_path):

            message_dialog = Gtk.MessageDialog(
                self.main_window,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK,
                _("Addon not found in download directory.")
                )
            content_area = message_dialog.get_content_area()
            content_area.set_property('margin-left', 10)
            content_area.set_property('margin-right', 10)
            content_area.set_property('margin-top', 10)
            content_area.set_property('margin-bottom', 10)

            self.main_window.hide()
            message_dialog.run()
            message_dialog.destroy()
            self.main_window.show()

        else:

            self.button_config.set_sensitive(False)
            self.button_patch.set_visible(False)
            self.progressbar.set_visible(True)

            while Gtk.events_pending():
                Gtk.main_iteration_do(False)

            command = ['innoextract', patch_path, '-d', game_dir + '/tmp']

            self.pid, stdin, stdout, stderr = GLib.spawn_async(command,
                                        flags=GLib.SpawnFlags.SEARCH_PATH|GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                                        standard_output=True,
                                        standard_error=True)

            io = GLib.IOChannel(stdout)

            self.source_id_out = io.add_watch(GLib.IO_IN|GLib.IO_HUP,
                                 self.watch_process,
                                 'extracting',
                                 priority=GLib.PRIORITY_HIGH)

    def cb_button_config(self, button):

        self.main_window.hide()

        while Gtk.events_pending():
            Gtk.main_iteration_do(False)

        os.system(wineloader + ' ' + game_dir + '/bin/Final/Config.exe')
        self.main_window.show()

    def cb_button_save(self, button):
        self.config_save()
        Gtk.main_quit()

    def quit_app(self, window, event):
        Gtk.main_quit()

    def watch_process(self, io, condition, process_name):

        if condition is GLib.IO_HUP:

            if process_name == 'extracting':

                os.system('touch ' + install_dir + '/pathologic/.ws_addon_installed')
                os.system('mv ' + game_dir + '/tmp/app/bin/Final/* ' + game_dir + '/bin/Final/')
                os.system('mkdir -p ' + game_dir + '/data/Scripts/')
                os.system('mv ' + game_dir + '/tmp/app/data/Scripts/* ' + game_dir + '/data/Scripts/')
                os.system('mkdir -p ' + game_dir + '/data/Textures/PL/')
                os.system('mv ' + game_dir + '/tmp/app/data/Textures/PL/* ' + game_dir + '/data/Textures/PL/')
                os.system('rm -r ' + game_dir + '/tmp/app/data/Textures/PL/')
                os.system('mkdir -p ' + game_dir + '/data/Textures/UI/')
                os.system('mv ' + game_dir + '/tmp/app/data/Textures/UI/* ' + game_dir + '/data/Textures/UI/')
                os.system('rm -r ' + game_dir + '/tmp/app/data/Textures/UI/')
                os.system('mv ' + game_dir + '/tmp/app/data/Textures/* ' + game_dir + '/data/Textures/')
                os.system('mkdir -p ' + game_dir + '/data/UI/')
                os.system('mv ' + game_dir + '/tmp/app/data/UI/* ' + game_dir + '/data/UI/')
                os.system('rm -r ' + game_dir + '/tmp/app/data/UI')
                os.system('mv ' + game_dir + '/tmp/app/data/Video/* ' + game_dir + '/data/Video/')
                os.system('rm -r ' + game_dir + '/tmp/app/data/Video')
                os.system('rm -r ' + game_dir + '/tmp/app/data')
                os.system('rm -r ' + game_dir + '/tmp/app/bin')
                os.system('mv ' + game_dir + '/tmp/app/* ' + game_dir)
                os.system('rm -r ' + game_dir + '/tmp')
                os.system('mv ' + game_dir + '/bin/Final/Config.exe ' + \
                        game_dir + '/bin/Final/Config.exe.bak ')
                os.execl(sys.executable, 'python2', __file__)

        print io.readline().strip('\n')

        if process_name == 'extracting':
            self.progressbar.pulse()

        return True

    def setup_enb(self):

        d3d9_path = game_dir + '/bin/Final/d3d9.dll'
        d3d9_enb_path = game_dir + '/bin/Final/d3d9.dll.enb'
        if self.enb == 1:
            if os.path.exists(d3d9_enb_path):
                os.system('mv ' + d3d9_enb_path + ' ' + d3d9_path)
        else:
            os.system('mv ' + d3d9_path + ' ' + d3d9_enb_path)

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
