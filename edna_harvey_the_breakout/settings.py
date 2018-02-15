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

current_dir = sys.path[0]

class GUI:

    def __init__(self):
        self.config_load()
        self.create_main_window()

    def config_load(self):

        conf_file_path = current_dir + '/game/ednaPreferen.ces'
        conf_file = open(conf_file_path, 'r')
        file_content = conf_file.readlines()
        conf_file.close()

        for line in file_content:
            if '"language"' in line:
                language = line.split('value=')[1].strip('"/>\r\n')
                if language == 'de':
                    self.language = 'Deutsch'
                else:
                    self.language = 'English'
            if '"fullscreen"' in line:
                fullscreen = line.split('value=')[1].strip('"/>\r\n')
                self.fullscreen = self.text_to_bool(fullscreen)
            if '"music"' in line:
                music = line.split('value=')[1].strip('"/>\r\n')
                self.music = self.text_to_bool(music)
            if '"sound"' in line:
                speech = line.split('value=')[1].strip('"/>\r\n')
                self.speech = self.text_to_bool(speech)
            if '"text"' in line:
                subtitles = line.split('value=')[1].strip('"/>\r\n')
                self.subtitles = self.text_to_bool(subtitles)
            if '"comment"' in line:
                comments = line.split('value=')[1].strip('"/>\r\n')
                self.comments = self.text_to_bool(comments)

    def text_to_bool(self, text):
        if text == 'true':
            return True
        else:
            return False

    def config_save(self):

        language = self.combobox_language.get_active_text()[:2].lower()
        fullscreen = str(self.switch_fullscreen.get_active()).lower()
        music = str(self.switch_music.get_active()).lower()
        speech = str(self.switch_speech.get_active()).lower()
        subtitles = str(self.switch_subtitles.get_active()).lower()
        comments = str(self.switch_comments.get_active()).lower()

        conf_file_path = current_dir + '/game/ednaPreferen.ces'
        conf_file = open(conf_file_path, 'r')
        file_content = conf_file.readlines()
        conf_file.close()
        conf_file = open(conf_file_path, 'w')

        for line in file_content:
            if '"language"' in line:
                conf_file.write(line.split('value=')[0] + 'value="' + language + '"/>\r\n')
            elif '"fullscreen"' in line:
                conf_file.write(line.split('value=')[0] + 'value="' + fullscreen + '"/>\r\n')
            elif '"music"' in line:
                conf_file.write(line.split('value=')[0] + 'value="' + music + '"/>\r\n')
            elif '"sound"' in line:
                conf_file.write(line.split('value=')[0]  + 'value="' + speech + '"/>\r\n')
            elif '"text"' in line:
                conf_file.write(line.split('value=')[0] + 'value="' + subtitles + '"/>\r\n')
            elif '"comment"' in line:
                conf_file.write(line.split('value=')[0] + 'value="' + comments + '"/>\r\n')
            else:
                conf_file.write(line)

        conf_file.close()

    def create_main_window(self):

        main_window = Gtk.Window(
            title = _("Edna & Harvey: The Breakout"),
            type = Gtk.WindowType.TOPLEVEL,
            window_position = Gtk.WindowPosition.CENTER_ALWAYS,
            resizable = False,
            default_width = 360,
            )
        main_window.connect('delete-event', Gtk.main_quit)

        label_language = Gtk.Label(
            halign = Gtk.Align.START,
            label = _("Language:"),
            )

        self.combobox_language = Gtk.ComboBoxText(
            hexpand = True
            )
        self.combobox_language.append_text('English')
        self.combobox_language.append_text('Deutsch')

        if self.language == 'Deutsch':
            self.combobox_language.set_active(1)
        else:
            self.combobox_language.set_active(0)

        label_fullscreen = Gtk.Label(
            halign = Gtk.Align.START,
            label = _("Fullscreen:"),
            )

        self.switch_fullscreen = Gtk.Switch(
            halign = Gtk.Align.END,
            active = self.fullscreen
            )

        label_music = Gtk.Label(
            halign = Gtk.Align.START,
            label = _("Music:"),
            )

        self.switch_music = Gtk.Switch(
            halign = Gtk.Align.END,
            active = self.music
            )

        label_speech = Gtk.Label(
            halign = Gtk.Align.START,
            label = _("Speech:"),
            )

        self.switch_speech = Gtk.Switch(
            halign = Gtk.Align.END,
            active = self.speech
            )

        label_subtitles = Gtk.Label(
            halign = Gtk.Align.START,
            label = _("Subtitles:"),
            )

        self.switch_subtitles = Gtk.Switch(
            halign = Gtk.Align.END,
            active = self.subtitles
            )

        label_comments = Gtk.Label(
            halign = Gtk.Align.START,
            label = _("Comments:"),
            )

        self.switch_comments = Gtk.Switch(
            halign = Gtk.Align.END,
            active = self.comments
            )

        grid = Gtk.Grid(
            margin_top = 10,
            margin_bottom = 10,
            margin_left = 10,
            margin_right = 10,
            row_spacing = 10,
            column_spacing = 10
            )

        button_save = Gtk.Button(
            label = _("Save and quit"),
            margin_top = 10,
            hexpand = True
            )
        button_save.connect('clicked', self.cb_button_save)

        grid.attach(label_language, 0, 0, 1, 1)
        grid.attach(self.combobox_language, 1, 0, 1, 1)
        grid.attach(label_fullscreen, 0, 1, 1, 1)
        grid.attach(self.switch_fullscreen, 1, 1, 1, 1)
        grid.attach(label_music, 0, 2, 1, 1)
        grid.attach(self.switch_music, 1, 2, 1, 1)
        grid.attach(label_speech, 0, 3, 1, 1)
        grid.attach(self.switch_speech, 1, 3, 1, 1)
        grid.attach(label_subtitles, 0, 4, 1, 1)
        grid.attach(self.switch_subtitles, 1, 4, 1, 1)
        grid.attach(label_comments, 0, 5, 1, 1)
        grid.attach(self.switch_comments, 1, 5, 1, 1)
        grid.attach(button_save, 0, 6, 2, 1)

        main_window.add(grid)
        main_window.show_all()

    def cb_button_save(self, button):
        self.config_save()
        Gtk.main_quit()

def main():
    import sys
    app = GUI()
    Gtk.main()

if __name__ == '__main__':
    sys.exit(main())
