#!/usr/bin/env python2
# -*- Mode: Python; coding: utf-8; -*-

import sys, os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
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
        self.create_progressbar_window()

    def config_load(self):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        if not config_parser.has_section('Settings'):
            config_parser.add_section('Settings')

        if not config_parser.has_option('Settings', 'widescreen_applied'):
            self.widescreen_applied = False
            config_parser.set('Settings', 'widescreen_applied', self.widescreen_applied)
        else:
            self.widescreen_applied = config_parser.getboolean('Settings', 'widescreen_applied')

        if not config_parser.has_option('Settings', 'width'):
            self.width = 640
            config_parser.set('Settings', 'width', self.width)
        else:
            self.width = config_parser.get('Settings', 'width')

        if not config_parser.has_option('Settings', 'height'):
            self.height = 480
            config_parser.set('Settings', 'height', self.height)
        else:
            self.height = config_parser.get('Settings', 'height')

        if not config_parser.has_option('Settings', 'guifix_applied'):
            self.guifix_applied = False
            config_parser.set('Settings', 'guifix_applied', self.guifix_applied)
        else:
            self.guifix_applied = config_parser.getboolean('Settings', 'guifix_applied')

        if not config_parser.has_option('Settings', 'font_size'):
            self.font_size = 0
            config_parser.set('Settings', 'font_size', self.font_size)
        else:
            self.font_size = config_parser.getint('Settings', 'font_size')

        if not config_parser.has_option('Settings', 'fixpack_installed'):
            self.fixpack_installed = False
            config_parser.set('Settings', 'fixpack_installed', self.fixpack_installed)
        else:
            self.fixpack_installed = config_parser.getboolean('Settings', 'fixpack_installed')

        if not config_parser.has_option('Settings', 'grammar'):
            self.grammar = False
            config_parser.set('Settings', 'grammar', self.grammar)
        else:
            self.grammar = config_parser.getboolean('Settings', 'grammar')

        if not config_parser.has_option('Settings', 'subtitles'):
            self.subtitles = False
            config_parser.set('Settings', 'subtitles', self.subtitles)
        else:
            self.subtitles = config_parser.getboolean('Settings', 'subtitles')

        if not config_parser.has_option('Settings', 'ub_installed'):
            self.ub_installed = False
            config_parser.set('Settings', 'ub_installed', self.ub_installed)
        else:
            self.ub_installed = config_parser.getboolean('Settings', 'ub_installed')

        if not config_parser.has_option('Settings', 'ub_recommended'):
            self.ub_recommended = False
            config_parser.set('Settings', 'ub_recommended', self.ub_recommended)
        else:
            self.ub_recommended = config_parser.getboolean('Settings', 'ub_recommended')

        if not config_parser.has_option('Settings', 'ub_deionarra'):
            self.ub_deionarra = False
            config_parser.set('Settings', 'ub_deionarra', self.ub_deionarra)
        else:
            self.ub_deionarra = config_parser.getboolean('Settings', 'ub_deionarra')

        if not config_parser.has_option('Settings', 'ub_cheat'):
            self.ub_cheat = False
            config_parser.set('Settings', 'ub_cheat', self.ub_cheat)
        else:
            self.ub_cheat = config_parser.getboolean('Settings', 'ub_cheat')

        if not config_parser.has_option('Settings', 'tp_installed'):
            self.tp_installed = False
            config_parser.set('Settings', 'tp_installed', self.tp_installed)
        else:
            self.tp_installed = config_parser.getboolean('Settings', 'tp_installed')

        if not config_parser.has_option('Settings', 'banter'):
            self.banter = 0
            config_parser.set('Settings', 'banter', self.banter)
        else:
            self.banter = config_parser.getint('Settings', 'banter')

        if not config_parser.has_option('Settings', 'robes'):
            self.robes = False
            config_parser.set('Settings', 'robes', self.robes)
        else:
            self.robes = config_parser.getboolean('Settings', 'robes')

        if not config_parser.has_option('Settings', 'bg2thac0'):
            self.bg2thac0 = False
            config_parser.set('Settings', 'bg2thac0', self.bg2thac0)
        else:
            self.bg2thac0 = config_parser.getboolean('Settings', 'bg2thac0')

        if not config_parser.has_option('Settings', 'stackable'):
            self.stackable = False
            config_parser.set('Settings', 'stackable', self.stackable)
        else:
            self.stackable = config_parser.getboolean('Settings', 'stackable')

        if not config_parser.has_option('Settings', 'city_areas'):
            self.city_areas = False
            config_parser.set('Settings', 'city_areas', self.city_areas)
        else:
            self.city_areas = config_parser.getboolean('Settings', 'city_areas')

        if not config_parser.has_option('Settings', 'souls'):
            self.souls = False
            config_parser.set('Settings', 'souls', self.souls)
        else:
            self.souls = config_parser.getboolean('Settings', 'souls')

        if not config_parser.has_option('Settings', 'nordom'):
            self.nordom = False
            config_parser.set('Settings', 'nordom', self.nordom)
        else:
            self.nordom = config_parser.getboolean('Settings', 'nordom')

        if not config_parser.has_option('Settings', 'stat_min'):
            self.stat_min = False
            config_parser.set('Settings', 'stat_min', self.stat_min)
        else:
            self.stat_min = config_parser.getboolean('Settings', 'stat_min')

        if not config_parser.has_option('Settings', 'max_hp'):
            self.max_hp = False
            config_parser.set('Settings', 'max_hp', self.max_hp)
        else:
            self.max_hp = config_parser.getboolean('Settings', 'max_hp')

        if not config_parser.has_option('Settings', 'max_spell'):
            self.max_spell = False
            config_parser.set('Settings', 'max_spell', self.max_spell)
        else:
            self.max_spell = config_parser.getboolean('Settings', 'max_spell')

        if not config_parser.has_option('Settings', 'no_music'):
            self.no_music = False
            config_parser.set('Settings', 'no_music', self.no_music)
        else:
            self.no_music = config_parser.getboolean('Settings', 'no_music')

        if not config_parser.has_option('Settings', 'floating_text'):
            self.floating_text = False
            config_parser.set('Settings', 'floating_text', self.floating_text)
        else:
            self.floating_text = config_parser.getboolean('Settings', 'floating_text')

        if not config_parser.has_option('Settings', 'all_items'):
            self.all_items = False
            config_parser.set('Settings', 'all_items', self.all_items)
        else:
            self.all_items = config_parser.getboolean('Settings', 'all_items')

        if not config_parser.has_option('Settings', 'glabrezus'):
            self.glabrezus = False
            config_parser.set('Settings', 'glabrezus', self.glabrezus)
        else:
            self.glabrezus = config_parser.getboolean('Settings', 'glabrezus')

        if not config_parser.has_option('Settings', 'annah'):
            self.annah = False
            config_parser.set('Settings', 'annah', self.annah)
        else:
            self.annah = config_parser.getboolean('Settings', 'annah')

        if not config_parser.has_option('Settings', 'morte'):
            self.morte = False
            config_parser.set('Settings', 'morte', self.morte)
        else:
            self.morte = config_parser.getboolean('Settings', 'morte')

        if not config_parser.has_option('Settings', 'quickload'):
            self.quickload = 0
            config_parser.set('Settings', 'quickload', self.quickload)
        else:
            self.quickload = config_parser.getint('Settings', 'quickload')

        if not config_parser.has_option('Settings', 'rest'):
            self.rest = False
            config_parser.set('Settings', 'rest', self.rest)
        else:
            self.rest = config_parser.getboolean('Settings', 'rest')

        if not config_parser.has_option('Settings', 'cheats_tom'):
            self.cheats_tom = False
            config_parser.set('Settings', 'cheats_tom', self.cheats_tom)
        else:
            self.cheats_tom = config_parser.getboolean('Settings', 'cheats_tom')

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

        self.old_font_size = self.font_size
        self.old_width = self.width
        self.old_height = self.height
        self.old_grammar = self.grammar
        self.old_subtitles = self.subtitles
        self.old_ub_recommended = self.ub_recommended
        self.old_ub_deionarra = self.ub_deionarra
        self.old_ub_cheat = self.ub_cheat
        self.old_banter = self.banter
        self.old_robes = self.robes
        self.old_bg2thac0 = self.bg2thac0
        self.old_stackable = self.stackable
        self.old_city_areas = self.city_areas
        self.old_souls = self.souls
        self.old_nordom = self.nordom
        self.old_stat_min = self.stat_min
        self.old_max_hp = self.max_hp
        self.old_max_spell = self.max_spell
        self.old_no_music = self.no_music
        self.old_floating_text = self.floating_text
        self.old_all_items = self.all_items
        self.old_glabrezus = self.glabrezus
        self.old_annah = self.annah
        self.old_morte = self.morte
        self.old_quickload = self.quickload
        self.old_rest = self.rest
        self.old_cheats_tom = self.cheats_tom

    def config_save(self):

        config_file = current_dir + '/settings.ini'
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)

        config_parser.set('Settings', 'widescreen_applied', self.widescreen_applied)
        config_parser.set('Settings', 'width', self.width)
        config_parser.set('Settings', 'height', self.height)
        config_parser.set('Settings', 'guifix_applied', self.guifix_applied)
        config_parser.set('Settings', 'font_size', self.font_size)
        config_parser.set('Settings', 'fixpack_installed', self.fixpack_installed)
        config_parser.set('Settings', 'grammar', self.grammar)
        config_parser.set('Settings', 'subtitles', self.subtitles)
        config_parser.set('Settings', 'ub_recommended', self.ub_recommended)
        config_parser.set('Settings', 'ub_deionarra', self.ub_deionarra)
        config_parser.set('Settings', 'ub_cheat', self.ub_cheat)
        config_parser.set('Settings', 'ub_installed', self.ub_installed)
        config_parser.set('Settings', 'tp_installed', self.tp_installed)
        config_parser.set('Settings', 'banter', self.banter)
        config_parser.set('Settings', 'robes', self.robes)
        config_parser.set('Settings', 'bg2thac0', self.bg2thac0)
        config_parser.set('Settings', 'stackable', self.stackable)
        config_parser.set('Settings', 'city_areas', self.city_areas)
        config_parser.set('Settings', 'souls', self.souls)
        config_parser.set('Settings', 'nordom', self.nordom)
        config_parser.set('Settings', 'stat_min', self.stat_min)
        config_parser.set('Settings', 'max_hp', self.max_hp)
        config_parser.set('Settings', 'max_spell', self.max_spell)
        config_parser.set('Settings', 'no_music', self.no_music)
        config_parser.set('Settings', 'floating_text', self.floating_text)
        config_parser.set('Settings', 'all_items', self.all_items)
        config_parser.set('Settings', 'glabrezus', self.glabrezus)
        config_parser.set('Settings', 'annah', self.annah)
        config_parser.set('Settings', 'morte', self.morte)
        config_parser.set('Settings', 'quickload', self.quickload)
        config_parser.set('Settings', 'rest', self.rest)
        config_parser.set('Settings', 'cheats_tom', self.cheats_tom)

        new_config_file = open(config_file, 'w')
        config_parser.write(new_config_file)
        new_config_file.close()

    def create_progressbar_window(self):

        self.progressbar_window = Gtk.Window(
            title = "Planescape: Torment",
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 360
            )

        self.progressbar = Gtk.ProgressBar(
            hexpand = True,
            show_text = True,
            text = _("Patching..."),
            pulse_step = 0.1,
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10
            )

        self.progressbar_window.add(self.progressbar)

    def create_main_window(self):

        self.main_window = Gtk.Window(
            title = _("Planescape: Torment"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            )
        self.main_window.connect('delete-event', self.quit_app)

        self.checkbutton_widescreen = Gtk.CheckButton(
            label = _("Widescreen mod and GhostDog's PS:T UI mod"),
            active = self.widescreen_applied
            )
        self.checkbutton_widescreen.connect('clicked', self.cb_checkbutton_widescreen)

        self.frame_widescreen = Gtk.Frame()

        grid_widescreen = Gtk.Grid(
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

        label_bigger_fonts = Gtk.Label(
            label = _("Fonts size: ")
            )

        combobox_bigger_fonts = Gtk.ComboBoxText()

        sizes = [_("default"),
        _("20% bigger for English, French, German, Spanish and Italian"),
        _("40% bigger for English, French, German, Spanish and Italian"),
        _("80% bigger for English, French, German, Spanish and Italian"),
        _("120% bigger for English, French, German, Spanish and Italian"),
        _("20% bigger for Hungarian"),
        _("40% bigger for Hungarian"),
        _("80% bigger for Hungarian"),
        _("120% bigger for Hungarian"),
        _("20% bigger for the Polish and Czech"),
        _("40% bigger for the Polish and Czech"),
        _("80% bigger for the Polish and Czech"),
        _("120% bigger for the Polish and Czech"),
        _("20% bigger for Russian"),
        _("40% bigger for Russian"),
        _("80% bigger for Russian"),
        _("120% bigger for Russian")
        ]

        for font in sizes:
            combobox_bigger_fonts.append_text(font)
        combobox_bigger_fonts.set_active(self.font_size)

        combobox_bigger_fonts.connect('changed', self.cb_combobox_bigger_fonts)

        grid_widescreen.attach(label_res, 0, 0, 1, 1)
        grid_widescreen.attach(entry_width, 1, 0, 1, 1)
        grid_widescreen.attach(entry_height, 2, 0, 1, 1)
        grid_widescreen.attach(label_bigger_fonts, 0, 1, 1, 1)
        grid_widescreen.attach(combobox_bigger_fonts, 1, 1, 2, 1)

        self.frame_widescreen.add(grid_widescreen)

        self.checkbutton_fixpack = Gtk.CheckButton(
            label = _("PS:T Ultimate WeiDU Fixpack"),
            active = self.fixpack_installed,
            margin_top = 10
            )
        self.checkbutton_fixpack.connect('clicked', self.cb_checkbutton_fixpack)

        self.frame_fixpack = Gtk.Frame()

        box_fixpack = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            spacing = 10,
            )

        checkbutton_grammar = Gtk.CheckButton(
            label = _("Dialogue Spelling/Grammar Corrections (English Only)"),
            active = self.grammar
            )
        checkbutton_grammar.connect('clicked', self.cb_checkbutton_grammar)

        checkbutton_subtitles = Gtk.CheckButton(
            label = _("Subtitled Cutscenes"),
            active = self.subtitles
            )
        checkbutton_subtitles.connect('clicked', self.cb_checkbutton_subtitles)

        box_fixpack.pack_start(checkbutton_grammar, True, True, 0)
        box_fixpack.pack_start(checkbutton_subtitles, True, True, 0)

        self.frame_fixpack.add(box_fixpack)

        box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            spacing = 10
            )

        self.checkbutton_ub = Gtk.CheckButton(
            label = _("PS:T Unfinished Business"),
            active = self.ub_installed,
            margin_top = 10
            )
        self.checkbutton_ub.connect('clicked', self.cb_checkbutton_ub)

        self.frame_ub = Gtk.Frame()

        box_ub = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            spacing = 10,
            )

        checkbutton_ub_recommended = Gtk.CheckButton(
            label = _("All Recommended PS:T Unfinished Business Components"),
            active = self.ub_recommended
            )
        checkbutton_ub_recommended.connect('clicked', self.cb_checkbutton_ub_recommended)

        checkbutton_ub_deionarra = Gtk.CheckButton(
            label = _("Expanded Deionarra's Truth Mod"),
            active = self.ub_deionarra
            )
        checkbutton_ub_deionarra.connect('clicked', self.cb_checkbutton_ub_deionarra)


        checkbutton_ub_cheat = Gtk.CheckButton(
            label = _("Restored Cheat Items (Not Recommended)"),
            active = self.ub_cheat
            )
        checkbutton_ub_cheat.connect('clicked', self.cb_checkbutton_ub_cheat)

        box_ub.pack_start(checkbutton_ub_recommended, True, True, 0)
        box_ub.pack_start(checkbutton_ub_deionarra, True, True, 0)
        box_ub.pack_start(checkbutton_ub_cheat, True, True, 0)

        self.frame_ub.add(box_ub)

        self.checkbutton_tp = Gtk.CheckButton(
            label = _("Qwinn's PS:T Tweak Pack"),
            active = self.tp_installed,
            margin_top = 10
            )
        self.checkbutton_tp.connect('clicked', self.cb_checkbutton_tp)

        self.frame_tp = Gtk.Frame()

        grid_tp = Gtk.Grid(
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            row_spacing = 10,
            column_spacing = 10
            )

        label_banter = Gtk.Label(
            label = _("Interparty Banter:"),
            halign = Gtk.Align.START
            )

        combobox_banter = Gtk.ComboBoxText()

        intervals = [_("default"),
        _("Interparty Banter Every 4 game hours (20 minutes)"),
        _("Interparty Banter Every 6 game hours (30 minutes)"),
        _("Interparty Banter Every 10 game hours (50 minutes)"),
        _("Interparty Banter Every 15 game hours (75 minutes)"),
        _("Interparty Banter Every 20 game hours (100 minutes)")
        ]

        for interval in intervals:
            combobox_banter.append_text(interval)
        combobox_banter.set_active(self.banter)

        combobox_banter.connect('changed', self.cb_combobox_banter)

        checkbutton_robes = Gtk.CheckButton(
            label = _("Dustman Robes Area Restriction Removal"),
            active = self.robes
            )
        checkbutton_robes.connect('clicked', self.cb_checkbutton_robes)

        checkbutton_bg2thac0 = Gtk.CheckButton(
            label = _("BG2-Style THAC0 Display"),
            active = self.bg2thac0
            )
        checkbutton_bg2thac0.connect('clicked', self.cb_checkbutton_bg2thac0)

        checkbutton_stackable = Gtk.CheckButton(
            label = _("Stackable Rings, Charms, Bracelets, Scrolls"),
            active = self.stackable
            )
        checkbutton_stackable.connect('clicked', self.cb_checkbutton_stackable)

        checkbutton_city_areas = Gtk.CheckButton(
            label = _("Explore City Areas"),
            active = self.city_areas
            )
        checkbutton_city_areas.connect('clicked', self.cb_checkbutton_city_areas)

        checkbutton_souls = Gtk.CheckButton(
            label = _("Scale of Souls"),
            active = self.souls
            )
        checkbutton_souls.connect('clicked', self.cb_checkbutton_souls)

        checkbutton_nordom = Gtk.CheckButton(
            label = _("Save Nordom! Tweak"),
            active = self.nordom
            )
        checkbutton_nordom.connect('clicked', self.cb_checkbutton_nordom)

        checkbutton_stat_min = Gtk.CheckButton(
            label = _("Disabled Stat Minimums"),
            active = self.stat_min
            )
        checkbutton_stat_min.connect('clicked', self.cb_checkbutton_stat_min)

        checkbutton_max_hp = Gtk.CheckButton(
            label = _("Maximized HP Per Level for TNO and Party"),
            active = self.max_hp
            )
        checkbutton_max_hp.connect('clicked', self.cb_checkbutton_max_hp)

        checkbutton_max_spell = Gtk.CheckButton(
            label = _("Maximized Friends Spell"),
            active = self.max_spell
            )
        checkbutton_max_spell.connect('clicked', self.cb_checkbutton_max_spell)

        checkbutton_no_music = Gtk.CheckButton(
            label = _("No Battle Music"),
            active = self.no_music
            )
        checkbutton_no_music.connect('clicked', self.cb_checkbutton_no_music)

        checkbutton_floating_text = Gtk.CheckButton(
            label = _("Use Floating Text Font Globally"),
            active = self.floating_text
            )
        checkbutton_floating_text.connect('clicked', self.cb_checkbutton_floating_text)

        checkbutton_all_items = Gtk.CheckButton(
            label = _("Identify All Items"),
            active = self.all_items
            )
        checkbutton_all_items.connect('clicked', self.cb_checkbutton_all_items)

        checkbutton_glabrezus = Gtk.CheckButton(
            label = _("Early Glabrezus Tweak"),
            active = self.glabrezus
            )
        checkbutton_glabrezus.connect('clicked', self.cb_checkbutton_glabrezus)

        checkbutton_annah = Gtk.CheckButton(
            label = _("Power Action Leprechaun Annah, by Black Isle"),
            active = self.annah
            )
        checkbutton_annah.connect('clicked', self.cb_checkbutton_annah)

        checkbutton_morte = Gtk.CheckButton(
            label = _("Easter Egg Morte, by Black Isle"),
            active = self.morte
            )
        checkbutton_morte.connect('clicked', self.cb_checkbutton_morte)

        label_quickload = Gtk.Label(
            label = _("Quick Load:"),
            halign = Gtk.Align.START
            )

        combobox_quickload = Gtk.ComboBoxText()

        options = [_("disabled"),
        _("F5 QuickSave, F9 QuickLoad"),
        _("F5 QuickSave, F10 QuickLoad")
        ]

        for option in options:
            combobox_quickload.append_text(option)
        combobox_quickload.set_active(self.quickload)

        combobox_quickload.connect('changed', self.cb_combobox_quickload)

        checkbutton_rest = Gtk.CheckButton(
            label = _("Rest Anywhere (Not Recommended)"),
            active = self.rest
            )
        checkbutton_rest.connect('clicked', self.cb_checkbutton_rest)

        checkbutton_cheats_tom = Gtk.CheckButton(
            label = _("Tome Of Cheats (Not Recommended)"),
            active = self.cheats_tom
            )
        checkbutton_cheats_tom.connect('clicked', self.cb_checkbutton_cheats_tom)

        grid_tp.attach(label_banter, 0, 0, 1, 1)
        grid_tp.attach(combobox_banter, 1, 0, 1, 1)
        grid_tp.attach(label_quickload, 0, 1, 1, 1)
        grid_tp.attach(combobox_quickload, 1, 1, 1, 1)
        grid_tp.attach(checkbutton_robes, 0, 2, 3, 1)
        grid_tp.attach(checkbutton_bg2thac0, 0, 3, 2, 1)
        grid_tp.attach(checkbutton_stackable, 0, 4, 2, 1)
        grid_tp.attach(checkbutton_city_areas, 0, 5, 2, 1)
        grid_tp.attach(checkbutton_souls, 0, 6, 2, 1)
        grid_tp.attach(checkbutton_nordom, 0, 7, 2, 1)
        grid_tp.attach(checkbutton_stat_min, 0, 8, 2, 1)
        grid_tp.attach(checkbutton_max_hp, 0, 9, 2, 1)
        grid_tp.attach(checkbutton_max_spell, 0, 10, 2, 1)
        grid_tp.attach(checkbutton_no_music, 0, 11, 2, 1)
        grid_tp.attach(checkbutton_floating_text, 0, 12, 2, 1)
        grid_tp.attach(checkbutton_all_items, 0, 13, 2, 1)
        grid_tp.attach(checkbutton_glabrezus, 0, 14, 2, 1)
        grid_tp.attach(checkbutton_annah, 0, 15, 2, 1)
        grid_tp.attach(checkbutton_morte, 0, 16, 2, 1)
        grid_tp.attach(checkbutton_rest, 0, 17, 2, 1)
        grid_tp.attach(checkbutton_cheats_tom, 0, 18, 2, 1)

        self.frame_tp.add(grid_tp)

        button_patch = Gtk.Button(
            label = _("Patch and quit")
            )
        button_patch.connect('clicked', self.cb_button_patch)

        box_scrolled = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        scrolled_windwow = Gtk.ScrolledWindow(height_request=240)
        scrolled_windwow.add(box_scrolled)

        box_scrolled.pack_start(self.checkbutton_fixpack, False, False, 0)
        box_scrolled.pack_start(self.frame_fixpack, False, False, 0)
        box_scrolled.pack_start(self.checkbutton_ub, False, False, 0)
        box_scrolled.pack_start(self.frame_ub, False, False, 0)
        box_scrolled.pack_start(self.checkbutton_tp, False, False, 0)
        box_scrolled.pack_start(self.frame_tp, False, False, 0)

        box = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            spacing = 10
            )

        box.pack_start(self.checkbutton_widescreen, True, True, 0)
        box.pack_start(self.frame_widescreen, True, True, 0)
        box.pack_start(scrolled_windwow, True, True, 0)
        box.pack_start(button_patch, True, True, 0)

        self.main_window.add(box)
        self.main_window.show_all()

        self.frame_widescreen.set_visible(self.widescreen_applied)
        self.frame_fixpack.set_visible(self.fixpack_installed)
        self.frame_ub.set_visible(self.ub_installed)
        self.frame_tp.set_visible(self.tp_installed)

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

    def cb_combobox_bigger_fonts(self, combobox):
        self.font_size = combobox.get_active()

    def cb_checkbutton_widescreen(self, checkbutton):
        self.frame_widescreen.set_visible(checkbutton.get_active())

    def cb_checkbutton_fixpack(self, checkbutton):
        self.frame_fixpack.set_visible(checkbutton.get_active())

    def cb_checkbutton_grammar(self, checkbutton):
        self.grammar = checkbutton.get_active()

    def cb_checkbutton_subtitles(self, checkbutton):
        self.subtitles = checkbutton.get_active()

    def cb_checkbutton_ub(self, checkbutton):
        self.frame_ub.set_visible(checkbutton.get_active())

    def cb_checkbutton_ub_recommended(self, checkbutton):
        self.ub_recommended = checkbutton.get_active()

    def cb_checkbutton_ub_deionarra(self, checkbutton):
        self.ub_deionarra = checkbutton.get_active()

    def cb_checkbutton_ub_cheat(self, checkbutton):
        self.ub_cheat = checkbutton.get_active()

    def cb_checkbutton_tp(self, checkbutton):
        self.frame_tp.set_visible(checkbutton.get_active())

    def cb_combobox_banter(self, combobox):
        self.banter = combobox.get_active()

    def cb_checkbutton_robes(self, checkbutton):
        self.robes = checkbutton.get_active()

    def cb_checkbutton_bg2thac0(self, checkbutton):
        self.bg2thac0 = checkbutton.get_active()

    def cb_checkbutton_stackable(self, checkbutton):
        self.stackable = checkbutton.get_active()

    def cb_checkbutton_city_areas(self, checkbutton):
        self.city_areas = checkbutton.get_active()

    def cb_checkbutton_souls(self, checkbutton):
        self.souls = checkbutton.get_active()

    def cb_checkbutton_nordom(self, checkbutton):
        self.nordom = checkbutton.get_active()

    def cb_checkbutton_stat_min(self, checkbutton):
        self.stat_min = checkbutton.get_active()

    def cb_checkbutton_max_hp(self, checkbutton):
        self.max_hp = checkbutton.get_active()

    def cb_checkbutton_max_spell(self, checkbutton):
        self.max_spell = checkbutton.get_active()

    def cb_checkbutton_no_music(self, checkbutton):
        self.no_music = checkbutton.get_active()

    def cb_checkbutton_floating_text(self, checkbutton):
        self.floating_text = checkbutton.get_active()

    def cb_checkbutton_all_items(self, checkbutton):
        self.all_items = checkbutton.get_active()

    def cb_checkbutton_glabrezus(self, checkbutton):
        self.glabrezus = checkbutton.get_active()

    def cb_checkbutton_annah(self, checkbutton):
        self.annah = checkbutton.get_active()

    def cb_checkbutton_morte(self, checkbutton):
        self.morte = checkbutton.get_active()

    def cb_combobox_quickload(self, combobox):
        self.quickload = combobox.get_active()

    def cb_checkbutton_rest(self, checkbutton):
        self.rest = checkbutton.get_active()

    def cb_checkbutton_cheats_tom(self, checkbutton):
        self.cheats_tom = checkbutton.get_active()

    def cb_button_patch(self, button):

        commands = []
        cd_command = 'cd ' + current_dir + '/game'

        # Widescreen

        if self.checkbutton_widescreen.get_active():

            if (self.width != self.old_width) or (self.height != self.old_height):

                os.system('rm -R ' + current_dir + '/game/cache')
                os.system('ln -s ' + current_dir + '/game/data ' + current_dir + '/game/cache')

                if not self.widescreen_applied:
                    command = "printf '0\nn\n1\n" + self.width + "\n" + self.height + \
                    "\ny\nn\ny\n'" + ' | ./weidu ./widescreen/widescreen.tp2'
                    self.widescreen_applied = True
                else:
                    command = "printf '1\n" + self.width + "\n" + self.height + \
                    "\ny\nn\ny\n'" + ' | ./weidu ./widescreen/widescreen.tp2'

                commands.append(command)

        # Gui fix

            if not self.guifix_applied:
                if self.font_size == 0:
                    command = "printf 'n\ni\nn\n' | ./weidu ./setup-ghostdog\\'s-pst-ui.tp2"
                else:
                    command = "printf 'n\ni\n" + str(self.font_size) + "\n'" \
                    " | ./weidu ./setup-ghostdog\\'s-pst-ui.tp2"
                self.guifix_applied = True
                commands.append(command)
            else:
                if (self.font_size != self.old_font_size) or \
                        (self.width != self.old_width) or \
                        (self.height != self.old_height):

                    if self.font_size == 0:
                        command = "printf 'i\nu\n' | ./weidu ./setup-ghostdog\\'s-pst-ui.tp2"
                    else:
                        if (self.width != self.old_width) or \
                                (self.height != self.old_height):

                            if self.font_size != self.old_font_size:
                                command = "printf 'i\n" + str(self.font_size) + "\n'" \
                                " | ./weidu ./setup-ghostdog\\'s-pst-ui.tp2"
                            else:
                                command = "printf 'i\nn\n'" \
                                " | ./weidu ./setup-ghostdog\\'s-pst-ui.tp2"
                        else:

                            if self.font_size != self.old_font_size:
                                command = "printf 'n\n" + str(self.font_size) + "\n'" \
                                " | ./weidu ./setup-ghostdog\\'s-pst-ui.tp2"

                    commands.append(command)

        # Fix pack

        if self.checkbutton_fixpack.get_active():

            if self.grammar == self.old_grammar:
                grammar = 'n'
            else:
                if self.grammar:
                    grammar = 'i'
                else:
                    grammar = 'u'

            if self.subtitles == self.old_subtitles:
                subtitles = 'n'
            else:
                if self.subtitles:
                    subtitles = 'i'
                else:
                    subtitles = 'u'

            if not self.fixpack_installed:
                command = "printf '0\nn\ni\n" + grammar + "\n" + subtitles + \
                "\n'" + ' | ./weidu ./setup-pst-fix.tp2'
                self.fixpack_installed = True
            else:
                command = "printf 'n\ni\n" + grammar + "\n" + subtitles + \
                "\n'" + ' | ./weidu ./setup-pst-fix.tp2'

            commands.append(command)

        # Unfinished Business

        if self.checkbutton_ub.get_active():

            if self.ub_recommended == self.old_ub_recommended:
                ub_recommended = 'n'
            else:
                if self.ub_recommended:
                    ub_recommended = 'i'
                else:
                    ub_recommended = 'u'

            if self.ub_deionarra == self.old_ub_deionarra:
                ub_deionarra = 'n'
            else:
                if self.ub_deionarra:
                    ub_deionarra = 'i'
                else:
                    ub_deionarra = 'u'

            if self.ub_cheat == self.old_ub_cheat:
                ub_cheat = 'n'
            else:
                if self.ub_cheat:
                    ub_cheat = 'i'
                else:
                    ub_cheat = 'u'

            if not self.ub_installed:
                command = "printf '0\nn\n" + ub_recommended + "\n" + \
                ub_deionarra + "\n" + ub_cheat + "\n'" + \
                ' | ./weidu ./setup-pst-ub.tp2'
                self.ub_installed = True
            else:
                command = "printf 'n\n" + ub_recommended + "\n" + \
                ub_deionarra + "\n" + ub_cheat + "\n'" + \
                ' | ./weidu ./setup-pst-ub.tp2'

            commands.append(command)

        # Tweak Pack

        if self.checkbutton_tp.get_active():

            if self.banter == self.old_banter:
                banter = 'n'
            else:
                if self.banter == 0:
                    banter = 'u'
                else:
                    banter = str(self.banter)

            if self.robes == self.old_robes:
                robes = 'n'
            else:
                if self.robes:
                    robes = 'i'
                else:
                    robes = 'u'

            if self.bg2thac0 == self.old_bg2thac0:
                bg2thac0 = 'n'
            else:
                if self.bg2thac0:
                    bg2thac0 = 'i'
                else:
                    bg2thac0 = 'u'

            if self.stackable == self.old_stackable:
                stackable = 'n'
            else:
                if self.stackable:
                    stackable = 'i'
                else:
                    stackable = 'u'

            if self.city_areas == self.old_city_areas:
                city_areas = 'n'
            else:
                if self.city_areas:
                    city_areas = 'i'
                else:
                    city_areas = 'u'

            if self.souls == self.old_souls:
                souls = 'n'
            else:
                if self.souls:
                    souls = 'i'
                else:
                    souls = 'u'

            if self.nordom == self.old_nordom:
                nordom = 'n'
            else:
                if self.nordom:
                    nordom = 'i'
                else:
                    nordom = 'u'

            if self.stat_min == self.old_stat_min:
                stat_min = 'n'
            else:
                if self.stat_min:
                    stat_min = 'i'
                else:
                    stat_min = 'u'

            if self.max_hp == self.old_max_hp:
                max_hp = 'n'
            else:
                if self.max_hp:
                    max_hp = 'i'
                else:
                    max_hp = 'u'

            if self.max_spell == self.old_max_spell:
                max_spell = 'n'
            else:
                if self.max_spell:
                    max_spell = 'i'
                else:
                    max_spell = 'u'

            if self.no_music == self.old_no_music:
                no_music = 'n'
            else:
                if self.no_music:
                    no_music = 'i'
                else:
                    no_music = 'u'

            if self.floating_text == self.old_floating_text:
                floating_text = 'n'
            else:
                if self.floating_text:
                    floating_text = 'i'
                else:
                    floating_text = 'u'

            if self.all_items == self.old_all_items:
                all_items = 'n'
            else:
                if self.all_items:
                    all_items = 'i'
                else:
                    all_items = 'u'

            if self.glabrezus == self.old_glabrezus:
                glabrezus = 'n'
            else:
                if self.glabrezus:
                    glabrezus = 'i'
                else:
                    glabrezus = 'u'

            if self.annah == self.old_annah:
                annah = 'n'
            else:
                if self.annah:
                    annah = 'i'
                else:
                    annah = 'u'

            if self.morte == self.old_morte:
                morte = 'n'
            else:
                if self.morte:
                    morte = 'i'
                else:
                    morte = 'u'

            if self.quickload == self.old_quickload:
                quickload = 'n'
            else:
                if self.quickload == 0:
                    quickload = 'u'
                else:
                    quickload = str(self.quickload)

            if self.rest == self.old_rest:
                rest = 'n'
            else:
                if self.rest:
                    rest = 'i'
                else:
                    rest = 'u'

            if self.cheats_tom == self.old_cheats_tom:
                cheats_tom = 'n'
            else:
                if self.cheats_tom:
                    cheats_tom = 'i'
                else:
                    cheats_tom = 'u'

            if not self.tp_installed:
                command = "printf '0\nn\n" \
                 + banter + "\n" \
                 + robes + "\n" \
                 + bg2thac0 + "\n" \
                 + stackable + "\n" \
                 + city_areas + "\n" \
                 + souls + "\n" \
                 + nordom + "\n" \
                 + stat_min + "\n" \
                 + max_hp + "\n" \
                 + max_spell + "\n" \
                 + no_music + "\n" \
                 + floating_text + "\n" \
                 + all_items + "\n" \
                 + glabrezus + "\n" \
                 + annah + "\n" \
                 + morte + "\n" \
                 + quickload + "\n" \
                 + rest + "\n" \
                 + cheats_tom + "\n'" \
                 + ' | ./weidu ./setup-pst-tweak.tp2'
                self.tp_installed = True
            else:
                command = "printf 'n\n" \
                 + banter + "\n" \
                 + robes + "\n" \
                 + bg2thac0 + "\n" \
                 + stackable + "\n" \
                 + city_areas + "\n" \
                 + souls + "\n" \
                 + nordom + "\n" \
                 + stat_min + "\n" \
                 + max_hp + "\n" \
                 + max_spell + "\n" \
                 + no_music + "\n" \
                 + floating_text + "\n" \
                 + all_items + "\n" \
                 + glabrezus + "\n" \
                 + annah + "\n" \
                 + morte + "\n" \
                 + quickload + "\n" \
                 + rest + "\n" \
                 + cheats_tom + "\n'" \
                 + ' | ./weidu ./setup-pst-tweak.tp2'

            commands.append(command)

        tmp_file_path = current_dir + '/game/tmp_file'
        tmp_file = open(tmp_file_path, 'w')
        tmp_file.write('#!/bin/bash\n')
        tmp_file.write(cd_command + '\n')
        for command in commands:
            tmp_file.write(command + '\n')
        tmp_file.close()
        os.system('chmod +x ' + tmp_file_path)

        self.progressbar_window.show_all()
        self.main_window.hide()

        while Gtk.events_pending():
            Gtk.main_iteration()

        command = ['sh', tmp_file_path]

        pid, stdin, stdout, stderr = GLib.spawn_async(command,
                                    flags=GLib.SpawnFlags.SEARCH_PATH|GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                                    standard_output=True,
                                    standard_error=True)

        io = GLib.IOChannel(stdout)

        self.source_id_out = io.add_watch(GLib.IO_IN|GLib.IO_HUP,
                             self.watch_process,
                             'patching',
                             priority=GLib.PRIORITY_HIGH)

    def watch_process(self, io, condition, process_name):

        if condition is GLib.IO_HUP:

            os.system('rm ' + current_dir + '/game/cache')
            os.system('mkdir -p ' + current_dir + '/game/cache')

            self.config_save()
            Gtk.main_quit()

            return False

        print io.readline().strip('\n')

        self.progressbar.pulse()

        return True

    def quit_app(self, window, event):
        Gtk.main_quit()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
