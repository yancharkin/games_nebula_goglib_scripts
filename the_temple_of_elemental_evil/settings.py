import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import gettext
import imp

nebula_dir = os.getenv('NEBULA_DIR')

modules_dir = nebula_dir + '/modules'
set_visuals = imp.load_source('set_visuals', modules_dir + '/set_visuals.py')

gettext.bindtextdomain('games_nebula', nebula_dir + '/locale')
gettext.textdomain('games_nebula')
_ = gettext.gettext

link_co8_modpack_std = "http://www.moddb.com/downloads/start/73404?referer=http%3A%2F%2Fwww.moddb.com%2Fmods%2Fcircle-of-eight-modpack"
link_co8_modpack_nc = "http://www.moddb.com/downloads/start/73406?referer=http%3A%2F%2Fwww.moddb.com%2Fmods%2Fcircle-of-eight-modpack"
link_co8_kob = "http://www.moddb.com/downloads/start/73408?referer=http%3A%2F%2Fwww.moddb.com%2Fmods%2Fthe-keep-on-the-borderlands"
link_bg_portraits_std = "http://files.co8.org/mods/TFE-X%20Modules/Portrait%20Packs/Baldur's%20Gate%20Portrait%20Pack%208.1.0%20Standard%20Edition%20Setup.exe"
link_bg_portraits_nc = "http://files.co8.org/mods/TFE-X%20Modules/Portrait%20Packs/Baldur's%20Gate%20Portrait%20Pack%208.1.0%20New%20Content%20Edition%20Setup.exe"
link_bg_portraits_kob = "http://files.co8.org/mods/TFE-X%20Modules/Portrait%20Packs/Baldur's%20Gate%20Portrait%20Pack%201.0.1%20Keep%20on%20the%20Borderlands%20Setup.exe"
link_id_portraits_std = "http://files.co8.org/mods/TFE-X%20Modules/Portrait%20Packs/Icewind%20Dale%20Portrait%20Pack%208.1.0%20Standard%20Edition%20Setup.exe"
link_id_portraits_nc = "http://files.co8.org/mods/TFE-X%20Modules/Portrait%20Packs/Icewind%20Dale%20Portrait%20Pack%208.1.0%20New%20Content%20Edition%20Setup.exe"
link_id_portraits_kob = "http://files.co8.org/mods/TFE-X%20Modules/Portrait%20Packs/Icewind%20Dale%20Portrait%20Pack%201.0.1%20Keep%20on%20the%20Borderlands%20Setup.exe"
link_ja2_portraits_std = "http://files.co8.org/mods/TFE-X%20Modules/Portrait%20Packs/Jagged%20Alliance%202%20Portrait%20Pack%208.1.0%20Standard%20Edition%20Setup.exe"
link_ja2_portraits_nc = "http://files.co8.org/mods/TFE-X%20Modules/Portrait%20Packs/Jagged%20Alliance%202%20Portrait%20Pack%208.1.0%20New%20Content%20Edition%20Setup.exe"
link_ja2_portraits_kob = "http://files.co8.org/mods/TFE-X%20Modules/Portrait%20Packs/Jagged%20Alliance%202%20Portrait%20Pack%201.0.1%20Keep%20on%20the%20Borderlands%20Setup.exe"
link_lr_portraits_std = "http://files.co8.org/mods/TFE-X%20Modules/Portrait%20Packs/Luis%20Royo%20Portrait%20Pack%208.1.0%20Standard%20Edition%20Setup.exe"
link_lr_portraits_nc = "http://files.co8.org/mods/TFE-X%20Modules/Portrait%20Packs/Luis%20Royo%20Portrait%20Pack%208.1.0%20New%20Content%20Edition%20Setup.exe"
link_lr_portraits_kob = "http://files.co8.org/mods/TFE-X%20Modules/Portrait%20Packs/Luis%20Royo%20Portrait%20Pack%201.0.1%20Keep%20on%20the%20Borderlands%20Setup.exe"

exe_co8_modpack_std = "Circle_of_Eight_Modpack_8.1.0_Standard_Edition_Setup.exe"
exe_co8_modpack_nc = "Circle_of_Eight_Modpack_8.1.0_New_Content_Edition_Setup.exe"
exe_co8_kob = "Keep_on_the_Borderlands_1.0.1_Setup.exe"
exe_bg_portraits_std = "Baldur's Gate Portrait Pack 8.1.0 Standard Edition Setup.exe"
exe_bg_portraits_nc = "Baldur's Gate Portrait Pack 8.1.0 New Content Edition Setup.exe"
exe_bg_portraits_kob = "Baldur's Gate Portrait Pack 1.0.1 Keep on the Borderlands Setup.exe"
exe_id_portraits_std = "Icewind Dale Portrait Pack 8.1.0 Standard Edition Setup.exe"
exe_id_portraits_nc = "Icewind Dale Portrait Pack 8.1.0 New Content Edition Setup.exe"
exe_id_portraits_kob = "Icewind Dale Portrait Pack 1.0.1 Keep on the Borderlands Setup.exe"
exe_ja2_portraits_std = "Jagged Alliance 2 Portrait Pack 8.1.0 Standard Edition Setup.exe"
exe_ja2_portraits_nc = "Jagged Alliance 2 Portrait Pack 8.1.0 New Content Edition Setup.exe"
exe_ja2_portraits_kob = "Jagged Alliance 2 Portrait Pack 1.0.1 Keep on the Borderlands Setup.exe"
exe_lr_portraits_std = "Luis Royo Portrait Pack 8.1.0 Standard Edition Setup.exe"
exe_lr_portraits_nc = "Luis Royo Portrait Pack 8.1.0 New Content Edition Setup.exe"
exe_lr_portraits_kob = "Luis Royo Portrait Pack 1.0.1 Keep on the Borderlands Setup.exe"

tfm_co8_modpack_std = ' '.join(exe_co8_modpack_std.split('_')[:-2]) + '.tfm'
tfm_co8_modpack_nc = ' '.join(exe_co8_modpack_nc.split('_')[:-2]) + '.tfm'
tfm_co8_kob = ' '.join(exe_co8_kob.split('_')[:-1]) + '.tfm'

tpp_bg_portraits_std = ' '.join(exe_bg_portraits_std.split(' ')[:-1]) + '.tpp'
tpp_id_portraits_std = ' '.join(exe_id_portraits_std.split(' ')[:-1]) + '.tpp'
tpp_ja2_portraits_std = ' '.join(exe_ja2_portraits_std.split(' ')[:-1]) + '.tpp'
tpp_lr_portraits_std = ' '.join(exe_lr_portraits_std.split(' ')[:-1]) + '.tpp'

current_dir = sys.path[0]
download_dir = os.getenv('DOWNLOAD_DIR')
install_dir = os.getenv('INSTALL_DIR')
game_dir = install_dir + '/the_temple_of_elemental_evil/game'
os.system('mkdir -p ' + download_dir + '/_distr/the_temple_of_elemental_evil')

std_addons_dir = current_dir + '/game/addons/Circle of Eight Modpack 8.1.0 Standard'
bg_portraits_installed = os.path.exists(std_addons_dir + '/' + tpp_bg_portraits_std)
id_portraits_installed = os.path.exists(std_addons_dir + '/' + tpp_id_portraits_std)
ja2_portraits_installed = os.path.exists(std_addons_dir + '/' + tpp_ja2_portraits_std)
lr_portraits_installed = os.path.exists(std_addons_dir + '/' + tpp_lr_portraits_std)

config_file_path = current_dir + '/game/toee.cfg'
if not os.path.exists(config_file_path):
    config_file_path = current_dir + '/game/ToEE.cfg'

class GUI:

    def __init__(self):
        self.config_load()
        self.create_main_window()
        self.create_co8_std_window()
        self.create_co8_nc_window()
        self.create_co8_kob_window()
        self.create_portraits_window()

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("The Temple of Elemental Evil"),
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

        self.button_co8_tfe_x = Gtk.Button(
            label = _("TFE-X"),
            no_show_all = True
            )
        self.button_co8_tfe_x.connect('clicked', self.cb_button_co8_tfe_x)
        if os.path.exists(current_dir + '/game/TFE-X.jar'):
            self.button_co8_tfe_x.set_visible(True)

        self.button_co8_std = Gtk.Button(
            label = _("Install 'Co8 Mopdack Standard Edition'"),
            no_show_all = True
            )
        self.button_co8_std.connect('clicked', self.cb_button_co8_std)
        if not os.path.exists(current_dir + '/game/' + tfm_co8_modpack_std):
            self.button_co8_std.set_visible(True)

        self.button_co8_nc = Gtk.Button(
            label = _("Install 'Co8 Mopdack New Content Edition'"),
            no_show_all = True
            )
        self.button_co8_nc.connect('clicked', self.cb_button_co8_nc)
        if not os.path.exists(current_dir + '/game/' + tfm_co8_modpack_nc):
            self.button_co8_nc.set_visible(True)

        self.button_co8_kob = Gtk.Button(
            label = _("Install 'The Keep on the Borderlands'"),
            no_show_all = True
            )
        self.button_co8_kob.connect('clicked', self.cb_button_co8_kob)
        if not os.path.exists(current_dir + '/game/' + tfm_co8_kob):
            self.button_co8_kob.set_visible(True)

        self.button_portraits = Gtk.Button(
            label = _("Install Portrait Packs"),
            no_show_all = True
            )
        self.button_portraits.connect('clicked', self.cb_button_portraits)

        if (not bg_portraits_installed) or \
                (not id_portraits_installed) or \
                (not ja2_portraits_installed) or \
                (not lr_portraits_installed):

            self.button_portraits.set_visible(True)

        button_save = Gtk.Button(
            label = _("Save and quit"),
            )
        button_save.connect('clicked', self.cb_button_save)

        grid.attach(label_custom_res, 0, 0, 2, 1)
        grid.attach(entry_custom_width, 0, 1, 1, 1)
        grid.attach(entry_custom_height, 1, 1, 1, 1)
        grid.attach(self.button_co8_tfe_x, 0, 2, 2, 1)
        grid.attach(self.button_co8_std, 0, 3, 2, 1)
        grid.attach(self.button_co8_nc, 0, 4, 2, 1)
        grid.attach(self.button_co8_kob, 0, 5, 2, 1)
        grid.attach(self.button_portraits, 0, 6, 2, 1)
        grid.attach(button_save, 0, 7, 2, 1)

        self.main_window.add(grid)
        self.main_window.show_all()

    def create_co8_std_window(self):

        self.co8_std_window = Gtk.Window(
            title = _("The Temple of Elemental Evil"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 480
            )
        self.co8_std_window.connect('delete-event', self.hide_co8_std_window)

        box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            spacing = 10
            )

        linkbutton_download = Gtk.LinkButton(
            label = _("Download 'Circle of Eight Mopdack Standard Edition'"),
            uri = link_co8_modpack_std,
            )

        linkbutton_put = Gtk.LinkButton(
            label = _("Put it here"),
            uri = 'file://' + download_dir + '/_distr/the_temple_of_elemental_evil',
            )

        button_install = Gtk.Button(label=_("Install"))
        button_install.connect('clicked', self.cb_button_install_std)

        self.box_std = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            spacing = 10
            )

        self.box_std.pack_start(linkbutton_download, True, True, 0)
        self.box_std.pack_start(linkbutton_put, True, True, 0)
        self.box_std.pack_start(button_install, True, True, 0)

        self.progressbar_std = Gtk.ProgressBar(
            hexpand = True,
            show_text = True,
            text = _("Processing..."),
            pulse_step = 0.1,
            no_show_all = True
            )

        box.pack_start(self.box_std, True, True, 0)
        box.pack_start(self.progressbar_std, True, True, 0)

        self.co8_std_window.add(box)

    def create_co8_nc_window(self):

        self.co8_nc_window = Gtk.Window(
            title = _("The Temple of Elemental Evil"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 480
            )
        self.co8_nc_window.connect('delete-event', self.hide_co8_nc_window)

        box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            spacing = 10
            )

        linkbutton_download = Gtk.LinkButton(
            label = _("Download 'Circle of Eight Mopdack New Content Edition'"),
            uri = link_co8_modpack_nc,
            )

        linkbutton_put = Gtk.LinkButton(
            label = _("Put it here"),
            uri = 'file://' + download_dir + '/_distr/the_temple_of_elemental_evil',
            )

        button_install = Gtk.Button(label=_("Install"))
        button_install.connect('clicked', self.cb_button_install_nc)

        self.box_nc = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            spacing = 10
            )

        self.box_nc.pack_start(linkbutton_download, True, True, 0)
        self.box_nc.pack_start(linkbutton_put, True, True, 0)
        self.box_nc.pack_start(button_install, True, True, 0)

        self.progressbar_nc = Gtk.ProgressBar(
            hexpand = True,
            show_text = True,
            text = _("Processing..."),
            pulse_step = 0.1,
            no_show_all = True
            )

        box.pack_start(self.box_nc, True, True, 0)
        box.pack_start(self.progressbar_nc, True, True, 0)

        self.co8_nc_window.add(box)

    def create_co8_kob_window(self):

        self.co8_kob_window = Gtk.Window(
            title = _("The Temple of Elemental Evil"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 480
            )
        self.co8_kob_window.connect('delete-event', self.hide_co8_kob_window)

        box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            spacing = 10
            )

        linkbutton_download = Gtk.LinkButton(
            label = _("Download 'The Keep on the Borderlands'"),
            uri = link_co8_kob,
            )

        linkbutton_put = Gtk.LinkButton(
            label = _("Put it here"),
            uri = 'file://' + download_dir + '/_distr/the_temple_of_elemental_evil',
            )

        button_install = Gtk.Button(label=_("Install"))
        button_install.connect('clicked', self.cb_button_install_kob)

        self.box_kob = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            spacing = 10
            )

        self.box_kob.pack_start(linkbutton_download, True, True, 0)
        self.box_kob.pack_start(linkbutton_put, True, True, 0)
        self.box_kob.pack_start(button_install, True, True, 0)

        self.progressbar_kob = Gtk.ProgressBar(
            hexpand = True,
            show_text = True,
            text = _("Processing..."),
            pulse_step = 0.1,
            no_show_all = True
            )

        box.pack_start(self.box_kob, True, True, 0)
        box.pack_start(self.progressbar_kob, True, True, 0)

        self.co8_kob_window.add(box)

    def create_portraits_window(self):

        self.portraits_window = Gtk.Window(
            title = _("The Temple of Elemental Evil"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 480
            )
        self.portraits_window.connect('delete-event', self.hide_portraits_window)

        self.checkbutton_bg = Gtk.CheckButton(
            label = _("Baldur's Gate Portrait Pack"),
            no_show_all = True,
            visible = not bg_portraits_installed
            )

        self.checkbutton_id = Gtk.CheckButton(
            label = _("Icewind Dale Portrait Pack"),
            no_show_all = True,
            visible = not id_portraits_installed
            )

        self.checkbutton_ja2 = Gtk.CheckButton(
            label = _("Jagged Alliance 2 Portrait Pack"),
            no_show_all = True,
            visible = not ja2_portraits_installed
            )

        self.checkbutton_lr = Gtk.CheckButton(
            label = _("Luis Royo Portrait Pack"),
            no_show_all = True,
            visible = not lr_portraits_installed
            )

        self.box_portraits = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            spacing = 10
            )

        button_install = Gtk.Button(label=_("Install"))
        button_install.connect('clicked', self.cb_button_install_portraits)

        self.box_portraits.pack_start(self.checkbutton_bg, True, True, 0)
        self.box_portraits.pack_start(self.checkbutton_id, True, True, 0)
        self.box_portraits.pack_start(self.checkbutton_ja2, True, True, 0)
        self.box_portraits.pack_start(self.checkbutton_lr, True, True, 0)
        self.box_portraits.pack_start(button_install, True, True, 0)

        self.progressbar_portraits = Gtk.ProgressBar(
            hexpand = True,
            show_text = True,
            text = _("Processing..."),
            pulse_step = 0.1,
            no_show_all = True
            )

        box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            spacing = 10
            )

        box.pack_start(self.box_portraits, True, True, 0)
        box.pack_start(self.progressbar_portraits, True, True, 0)

        self.portraits_window.add(box)

    def config_load(self):
        config_file = open(config_file_path, 'r')
        config_content = config_file.readlines()
        config_file.close()

        for line in config_content:
            if 'video_width' in line:
                self.custom_width = line.split('=')[1].strip('\r\n')
            if 'video_height' in line:
                self.custom_height = line.split('=')[1].strip('\r\n')

    def config_save(self):

        config_file_path = current_dir + '/game/toee.cfg'
        if not os.path.exists(config_file_path):
            config_file_path = current_dir + '/game/ToEE.cfg'

        config_file = open(config_file_path, 'r')
        config_content = config_file.readlines()
        config_file.close()

        config_file = open(config_file_path, 'w')

        for line in config_content:
            if 'video_height' in line:
                config_file.write('video_height=' + self.custom_height + '\r\n')
            elif 'video_width' in line:
                config_file.write('video_width=' + self.custom_width + '\r\n')
            else:
                config_file.write(line)

        config_file.close()

    def cb_button_co8_tfe_x(self, button):

        self.main_window.hide()

        while Gtk.events_pending():
            Gtk.main_iteration()

        os.system('cd ' + current_dir + '/game && ' +
        current_dir + '/jre/bin/java -jar ./TFE-X.jar' )

        self.main_window.show()

    def cb_button_co8_std(self, button):
        self.main_window.hide()
        self.co8_std_window.show_all()

    def cb_button_co8_nc(self, button):
        self.main_window.hide()
        self.co8_nc_window.show_all()

    def cb_button_co8_kob(self, button):
        self.main_window.hide()
        self.co8_kob_window.show_all()

    def cb_button_portraits(self, button):
        self.main_window.hide()
        self.portraits_window.show_all()

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

    def cb_button_install_std(self, button):

        modpacks_path = download_dir + '/_distr/the_temple_of_elemental_evil/' + exe_co8_modpack_std

        if not os.path.exists(modpacks_path):

            message_dialog = Gtk.MessageDialog(
                self.co8_std_window,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK,
                _("Modpack not found in download directory")
                )
            content_area = message_dialog.get_content_area()
            content_area.set_property('margin-left', 10)
            content_area.set_property('margin-right', 10)
            content_area.set_property('margin-top', 10)
            content_area.set_property('margin-bottom', 10)

            self.co8_std_window.hide()
            message_dialog.run()
            message_dialog.destroy()
            self.co8_std_window.show()

        else:

            self.box_std.set_visible(False)
            self.progressbar_std.set_visible(True)

            command = ['innoextract', modpacks_path, '-d', game_dir + '/tmp']

            self.pid_std, stdin, stdout, stderr = GLib.spawn_async(command,
                                        flags=GLib.SpawnFlags.SEARCH_PATH|GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                                        standard_output=True,
                                        standard_error=True)

            io = GLib.IOChannel(stdout)

            self.source_id_out = io.add_watch(GLib.IO_IN|GLib.IO_HUP,
                                 self.watch_process,
                                 'extracting std',
                                 priority=GLib.PRIORITY_HIGH)

    def cb_button_install_nc(self, button):

        modpacks_path = download_dir + '/_distr/the_temple_of_elemental_evil/' + exe_co8_modpack_nc

        if not os.path.exists(modpacks_path):

            message_dialog = Gtk.MessageDialog(
                self.co8_nc_window,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK,
                _("Modpack not found in download directory")
                )
            content_area = message_dialog.get_content_area()
            content_area.set_property('margin-left', 10)
            content_area.set_property('margin-right', 10)
            content_area.set_property('margin-top', 10)
            content_area.set_property('margin-bottom', 10)

            self.co8_nc_window.hide()
            message_dialog.run()
            message_dialog.destroy()
            self.co8_nc_window.show()

        else:

            self.box_nc.set_visible(False)
            self.progressbar_nc.set_visible(True)

            command = ['innoextract', modpacks_path, '-d', game_dir + '/tmp']

            self.pid_nc, stdin, stdout, stderr = GLib.spawn_async(command,
                                        flags=GLib.SpawnFlags.SEARCH_PATH|GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                                        standard_output=True,
                                        standard_error=True)

            io = GLib.IOChannel(stdout)

            self.source_id_out = io.add_watch(GLib.IO_IN|GLib.IO_HUP,
                                 self.watch_process,
                                 'extracting nc',
                                 priority=GLib.PRIORITY_HIGH)

    def cb_button_install_kob(self, button):

        modpacks_path = download_dir + '/_distr/the_temple_of_elemental_evil/' + exe_co8_kob

        if not os.path.exists(modpacks_path):

            message_dialog = Gtk.MessageDialog(
                self.co8_kob_window,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK,
                _("Mod not found in download directory")
                )
            content_area = message_dialog.get_content_area()
            content_area.set_property('margin-left', 10)
            content_area.set_property('margin-right', 10)
            content_area.set_property('margin-top', 10)
            content_area.set_property('margin-bottom', 10)

            self.co8_kob_window.hide()
            message_dialog.run()
            message_dialog.destroy()
            self.co8_kob_window.show()

        else:

            self.box_kob.set_visible(False)
            self.progressbar_kob.set_visible(True)

            command = ['innoextract', modpacks_path, '-d', game_dir + '/tmp']

            self.pid_kob, stdin, stdout, stderr = GLib.spawn_async(command,
                                        flags=GLib.SpawnFlags.SEARCH_PATH|GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                                        standard_output=True,
                                        standard_error=True)

            io = GLib.IOChannel(stdout)

            self.source_id_out = io.add_watch(GLib.IO_IN|GLib.IO_HUP,
                                 self.watch_process,
                                 'extracting kob',
                                 priority=GLib.PRIORITY_HIGH)

    def cb_button_install_portraits(self, button):

        if (not self.checkbutton_bg.get_active()) and \
                (not self.checkbutton_id.get_active()) and \
                (not self.checkbutton_ja2.get_active()) and \
                (not self.checkbutton_lr.get_active()):

            self.portraits_window.hide()

            message_dialog = Gtk.MessageDialog(
                self.main_window,
                0,
                Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK,
                _("Error")
                )
            message_dialog.format_secondary_text(_("You have to select at least one portrait pack."))
            content_area = message_dialog.get_content_area()
            content_area.set_property('margin-left', 10)
            content_area.set_property('margin-right', 10)
            content_area.set_property('margin-top', 10)
            content_area.set_property('margin-bottom', 10)
            message_dialog.run()
            message_dialog.destroy()

            self.portraits_window.show()

        else:

            self.box_portraits.set_visible(False)
            self.progressbar_portraits.set_visible(True)

            distr_dir = download_dir + '/_distr/the_temple_of_elemental_evil/'

            self.bg_download_portraits_commands = []

            if not os.path.exists(distr_dir + exe_bg_portraits_std):
                self.bg_download_portraits_commands.append(['curl', '-L', '-o', distr_dir + exe_bg_portraits_std, link_bg_portraits_std])
            if not os.path.exists(distr_dir + exe_bg_portraits_nc):
                self.bg_download_portraits_commands.append(['curl', '-L', '-o', distr_dir + exe_bg_portraits_nc, link_bg_portraits_nc])
            if not os.path.exists(distr_dir + exe_bg_portraits_kob):
                self.bg_download_portraits_commands.append(['curl', '-L', '-o', distr_dir + exe_bg_portraits_kob, link_bg_portraits_kob])

            self.bg_extract_portraits_commands = [
                ['innoextract', distr_dir + exe_bg_portraits_std, '-d', game_dir + '/tmp'],
                ['innoextract', distr_dir + exe_bg_portraits_nc, '-d', game_dir + '/tmp'],
                ['innoextract', distr_dir + exe_bg_portraits_kob, '-d', game_dir + '/tmp']
            ]

            self.id_download_portraits_commands = []

            if not os.path.exists(distr_dir + exe_id_portraits_std):
                self.id_download_portraits_commands.append(['curl', '-L', '-o', distr_dir + exe_id_portraits_std, link_id_portraits_std])
            if not os.path.exists(distr_dir + exe_id_portraits_nc):
                self.id_download_portraits_commands.append(['curl', '-L', '-o', distr_dir + exe_id_portraits_nc, link_id_portraits_nc])
            if not os.path.exists(distr_dir + exe_id_portraits_kob):
                self.id_download_portraits_commands.append(['curl', '-L', '-o', distr_dir + exe_id_portraits_kob, link_id_portraits_kob])

            self.id_extract_portraits_commands = [
                ['innoextract', distr_dir + exe_id_portraits_std, '-d', game_dir + '/tmp'],
                ['innoextract', distr_dir + exe_id_portraits_nc, '-d', game_dir + '/tmp'],
                ['innoextract', distr_dir + exe_id_portraits_kob, '-d', game_dir + '/tmp']
            ]

            self.ja2_download_portraits_commands = []

            if not os.path.exists(distr_dir + exe_ja2_portraits_std):
                self.ja2_download_portraits_commands.append(['curl', '-L', '-o', distr_dir + exe_ja2_portraits_std, link_ja2_portraits_std])
            if not os.path.exists(distr_dir + exe_ja2_portraits_nc):
                self.ja2_download_portraits_commands.append(['curl', '-L', '-o', distr_dir + exe_ja2_portraits_nc, link_ja2_portraits_nc])
            if not os.path.exists(distr_dir + exe_ja2_portraits_kob):
                self.ja2_download_portraits_commands.append(['curl', '-L', '-o', distr_dir + exe_ja2_portraits_kob, link_ja2_portraits_kob])

            self.ja2_extract_portraits_commands = [
                ['innoextract', distr_dir + exe_ja2_portraits_std, '-d', game_dir + '/tmp'],
                ['innoextract', distr_dir + exe_ja2_portraits_nc, '-d', game_dir + '/tmp'],
                ['innoextract', distr_dir + exe_ja2_portraits_kob, '-d', game_dir + '/tmp']
            ]

            self.lr_download_portraits_commands = []

            if not os.path.exists(distr_dir + exe_lr_portraits_std):
                self.lr_download_portraits_commands.append(['curl', '-L', '-o', distr_dir + exe_lr_portraits_std, link_lr_portraits_std])
            if not os.path.exists(distr_dir + exe_lr_portraits_nc):
                self.lr_download_portraits_commands.append(['curl', '-L', '-o', distr_dir + exe_lr_portraits_nc, link_lr_portraits_nc])
            if not os.path.exists(distr_dir + exe_lr_portraits_kob):
                self.lr_download_portraits_commands.append(['curl', '-L', '-o', distr_dir + exe_lr_portraits_kob, link_lr_portraits_kob])

            self.lr_extract_portraits_commands = [
                ['innoextract', distr_dir + exe_lr_portraits_std, '-d', game_dir + '/tmp'],
                ['innoextract', distr_dir + exe_lr_portraits_nc, '-d', game_dir + '/tmp'],
                ['innoextract', distr_dir + exe_lr_portraits_kob, '-d', game_dir + '/tmp']
            ]

            self.download_portraits_commands = []
            self.extract_portraits_commands = []

            if self.checkbutton_bg.get_active():
                self.checkbutton_bg.set_visible(False)
                self.download_portraits_commands.extend(self.bg_download_portraits_commands)
                self.extract_portraits_commands.extend(self.bg_extract_portraits_commands)
            if self.checkbutton_id.get_active():
                self.checkbutton_id.set_visible(False)
                self.download_portraits_commands.extend(self.id_download_portraits_commands)
                self.extract_portraits_commands.extend(self.id_extract_portraits_commands)
            if self.checkbutton_ja2.get_active():
                self.checkbutton_ja2.set_visible(False)
                self.download_portraits_commands.extend(self.ja2_download_portraits_commands)
                self.extract_portraits_commands.extend(self.ja2_extract_portraits_commands)
            if self.checkbutton_lr.get_active():
                self.checkbutton_lr.set_visible(False)
                self.download_portraits_commands.extend(self.lr_download_portraits_commands)
                self.extract_portraits_commands.extend(self.lr_extract_portraits_commands)

            if (self.checkbutton_bg.get_visible() == False) and \
                    (self.checkbutton_id.get_visible() == False) and \
                    (self.checkbutton_ja2.get_visible() == False) and \
                    (self.checkbutton_lr.get_visible() == False):

                self.button_portraits.set_visible(False)

            self.n_download_commands = len(self.download_portraits_commands)
            self.n_extract_commands = len(self.extract_portraits_commands)

            if self.n_download_commands != 0:
                for command in self.download_portraits_commands:
                    self.execute_command(command, 'downloading portraits')
            else:
                command = ['echo', '"Already downloaded"']
                self.execute_command(command, 'downloading portraits')

    def execute_command(self, command, process_name):

        pid, stdin, stdout, stderr = GLib.spawn_async(command,
                                    flags=GLib.SpawnFlags.SEARCH_PATH|GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                                    standard_output=True,
                                    standard_error=True)

        io = GLib.IOChannel(stdout)

        self.source_id_out = io.add_watch(GLib.IO_IN|GLib.IO_HUP,
                             self.watch_process,
                             process_name,
                             priority=GLib.PRIORITY_HIGH)

    def watch_process(self, io, condition, process_name):

        if condition is GLib.IO_HUP:

            if process_name == 'extracting std':

                os.system('mv ' + game_dir + '/tmp/app/* ' + game_dir)
                os.system('rm -R ' + game_dir + '/tmp')

                self.co8_std_window.hide()
                self.main_window.show()
                self.button_co8_tfe_x.set_visible(True)
                self.button_co8_std.set_visible(False)

                return False

            if process_name == 'extracting nc':

                os.system('mv ' + game_dir + '/tmp/app/* ' + game_dir)
                os.system('rm -R ' + game_dir + '/tmp')

                self.co8_nc_window.hide()
                self.main_window.show()
                self.button_co8_tfe_x.set_visible(True)
                self.button_co8_nc.set_visible(False)

                return False

            if process_name == 'extracting kob':

                os.system('mv ' + game_dir + '/tmp/app/* ' + game_dir)
                os.system('rm -R ' + game_dir + '/tmp')

                self.co8_kob_window.hide()
                self.main_window.show()
                self.button_co8_tfe_x.set_visible(True)
                self.button_co8_kob.set_visible(False)

                return False

            if process_name == 'downloading portraits':

                self.progressbar_portraits.pulse()
                self.n_download_commands -= 1

                if self.n_download_commands <= 0:
                    for command in self.extract_portraits_commands:
                        self.execute_command(command, 'extracting portraits')

                return False

            if process_name == 'extracting portraits':

                self.progressbar_portraits.pulse()
                self.n_extract_commands -= 1

                if self.n_extract_commands == 0:

                    os.system('cp -r ' + game_dir + '/tmp/app/* ' + game_dir)
                    os.system('rm -R ' + game_dir + '/tmp')

                    self.progressbar_portraits.set_visible(False)
                    self.portraits_window.hide()
                    self.main_window.show()

                return False

        print(io.readline().strip('\n'))

        if process_name == 'extracting std':
            self.progressbar_std.pulse()
        if process_name == 'extracting nc':
            self.progressbar_nc.pulse()
        if process_name == 'extracting kob':
            self.progressbar_kob.pulse()
        if process_name == 'downloading portraits':
            self.progressbar_portraits.pulse()
        if process_name == 'extracting portraits':
            self.progressbar_portraits.pulse()

        return True

    def hide_co8_std_window(self, window, event):
        window.hide()
        self.main_window.show()
        return True

    def hide_co8_nc_window(self, window, event):
        window.hide()
        self.main_window.show()
        return True

    def hide_co8_kob_window(self, window, event):
        window.hide()
        self.main_window.show()
        return True

    def hide_portraits_window(self, window, event):
        window.hide()
        self.main_window.show()
        return True

    def quit_app(self, window, event):
        Gtk.main_quit()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
