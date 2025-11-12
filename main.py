import sys

from PyQt6.QtWidgets import *


class notepad(QWidget):
    def __init__(self, clr):
        super().__init__()
        #self.def_ext = ".txt"
        self.color = clr
        self.showversion = False #release consumer version - false, beta - true
        self.version = " 1.6" #js like cs 1.6
        self.initUI()

    def initUI(self):
        global lang_rus
        global lang_eng
        #window
        self.setFixedSize(300, 410)
        if self.showversion:
            self.setWindowTitle(cur_lang["nott"] + self.version)
        else:
            self.setWindowTitle(cur_lang["nott"])

        
        #text area
        self.label1 = QLabel("", self)
        self.label1.resize(self.label1.sizeHint())
        self.label1.move(19, 380)
        
        self.text = QPlainTextEdit(self)
        self.text.resize(260, 330)
        self.text.move(20, 50)
        
        #buttons and shi
        #saving
        self.save = QPushButton(cur_lang["svf"], self)
        self.save.resize(70, 30)
        self.save.move(19, 15)
        self.save.clicked.connect(self.save_file)

        #opening
        self.open = QPushButton(cur_lang["opf"], self)
        self.open.resize(70, 30)
        self.open.move(100, 15)
        self.open.clicked.connect(self.load_file)

        #settings
        self.setup = QPushButton(cur_lang["setn"], self)
        self.setup.resize(70, 30)
        self.setup.move(211, 15)
        self.setup.clicked.connect(self.open_settings)

        self.update_color()

    def load_file(self):
        global lang_rus
        global lang_eng
        file_name, _ = QFileDialog.getOpenFileName(self, cur_lang["opas"], "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                print(file_name)
                self.text.setPlainText(file.read())
                self.update_recents(file_name)

    def fast_load(self, file_name):
        with open(file_name, 'r+', encoding='utf-8') as file:
            self.text.setPlainText(file.read())
            self.update_recents(file_name)

    def update_color(self):
        self.save.setStyleSheet("color:" + colorf + ";")
        self.setup.setStyleSheet("color:" + colorf + ";")
        self.open.setStyleSheet("color:" + colorf + ";")
        self.text.setStyleSheet("color:" + colorf + ";")
        self.label1.setStyleSheet("color:" + colorf + ";")
        self.setStyleSheet("background-color:" + colort + ";")

    def update_lang(self):
        self.setWindowTitle(cur_lang["nott"])
        self.save.setText(cur_lang["svf"])
        self.setup.setText(cur_lang["setn"])
        self.open.setText(cur_lang["opf"])

    def save_file(self):
        global lang_rus
        global lang_eng
        file_name, _ = QFileDialog.getSaveFileName(self, cur_lang["svas"], "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                print(self.text.toPlainText(), file=f)
                self.label1.setText(f'{cur_lang["svdas"]} \n {file_name}!')
                self.label1.resize(self.label1.sizeHint())
                recentloc.update_list()
                self.update_recents(file_name)

    def open_settings(self):
        settingsloc.show()

    def update_recents(self, string):
        with open("recents.txt", 'r+', encoding='utf-8') as r:
            text = r.read().strip()
            if string not in text:
                if text != "":
                    textall = text + "\n" + string.strip()
                else:
                    textall = string.strip()
                print(textall, file=r)


class recentwindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # window
        self.setFixedSize(250, 300)
        self.setWindowTitle(cur_lang["rec"])

        # list init
        self.list = QListWidget(self)
        self.list.move(0, 0)
        self.list.resize(250, 300)

        self.update_color()
        self.update_list()

        self.list.itemClicked.connect(self.get_clicked)

    def get_clicked(self):
        global ex
        file = self.list.currentItem().text()
        print(file.strip())
        ex.fast_load(file.strip())


    def update_list(self):
        with open("recents.txt", 'r+', encoding='utf-8') as r:
            text = r.readlines()
            if text:
                for i in text:
                    self.list.insertItem(text.index(i), i)

    def update_color(self):
        global lang_rus
        global lang_eng
        self.list.setStyleSheet("color:" + colorf + ";" + "background-color:" + colort + ";")
        self.setStyleSheet("background-color:" + colort + ";")
        self.setWindowTitle(cur_lang["rec"])


class settings(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global lang_rus
        global lang_eng
        # window
        self.setFixedSize(250, 250)
        self.setWindowTitle(cur_lang["setnt"])

        # theme changer
        self.theme_btn = QPushButton(cur_lang["thm"], self)
        self.theme_btn.resize(85, 30)
        self.theme_btn.move(19, 15)
        self.theme_btn.clicked.connect(self.theme)

        # theme importer
        self.theme_import = QPushButton(cur_lang["thmi"], self)
        self.theme_import.resize(85, 30)
        self.theme_import.move(19, 56)
        self.theme_import.clicked.connect(self.import_theme)

        #lang swapper
        self.lang_ch = QPushButton(cur_lang["lngc"], self)
        self.lang_ch.resize(85, 30)
        self.lang_ch.move(19, 97)
        self.lang_ch.clicked.connect(self.change_lang)

        # recents button
        self.recent = QPushButton(cur_lang["recb"], self)
        self.recent.resize(85, 30)
        self.recent.move(19, 138)
        self.recent.clicked.connect(recentloc.show)

        #theme label
        self.labelt = QLabel("", self)
        self.labelt.move(108, 22)
        if colort == "#E0E0E0":
            self.labelt.setText(cur_lang["thmtl"])
            self.labelt.resize(self.labelt.sizeHint())
        elif colort == "#404040":
            self.labelt.setText(cur_lang["thmtd"])
            self.labelt.resize(self.labelt.sizeHint())
        else:
            self.labelt.setText(cur_lang["thmtc"])
            self.labelt.resize(self.labelt.sizeHint())

        # theme label
        self.labell = QLabel(cur_lang["lang"], self)
        self.labell.move(108, 104)
        if cur_lang == lang_rus:
            self.labell.setText(cur_lang["lang"])
        else:
            self.labell.setText(cur_lang["lang"])

        self.update_color()

    def theme(self):
        global lang_rus
        global lang_eng
        global colort
        global colorf
        global ex
        if colort == "#E0E0E0":
            colort = "#404040"
            colorf = "#FFFFFF"
            ex.update_color()
            recentloc.update_color()
            self.update_color()
            with open("settings.stp", 'w', encoding='utf-8') as f:
                print("theme "+ colort + "\nfontc " + colorf + "\nlang " + cur_lang["lang"], file=f)
            #notepad.update_color()
        elif colort == "#404040":
            colort = "#E0E0E0"
            colorf = "#000000"
            self.update_color()
            recentloc.update_color()
            ex.update_color()
            with open("settings.stp", 'w', encoding='utf-8') as f:
                print("theme "+ colort + "\nfontc " + colorf + "\nlang " + cur_lang["lang"], file=f)
        else:
            colort = "#404040"
            colorf = "#FFFFFF"
            ex.update_color()
            recentloc.update_color()
            self.update_color()
            with open("settings.stp", 'w', encoding='utf-8') as f:
                print("theme "+ colort + "\nfontc " + colorf + "\nlang " + cur_lang["lang"], file=f)

    def update_color(self):
        global lang_rus
        global lang_eng
        self.theme_btn.setStyleSheet("color:" + colorf + ";")
        self.recent.setStyleSheet("color:" + colorf + ";")
        self.lang_ch.setStyleSheet("color:" + colorf + ";")
        self.labell.setStyleSheet("color:" + colorf + ";")
        self.theme_import.setStyleSheet("color:" + colorf + ";")
        self.labelt.setStyleSheet("color:" + colorf + ";")
        self.setStyleSheet("background-color:" + colort + ";")
        if colort == "#E0E0E0":
            self.labelt.setText(cur_lang["thmtl"])
            self.labelt.resize(self.labelt.sizeHint())
        elif colort == "#404040":
            self.labelt.setText(cur_lang["thmtd"])
            self.labelt.resize(self.labelt.sizeHint())
        else:
            self.labelt.setText(cur_lang["thmtc"])
            self.labelt.resize(self.labelt.sizeHint())

    def import_theme(self):
        global colort
        global lang_rus
        global lang_eng
        global colorf
        global ex
        file_name, _ = QFileDialog.getOpenFileName(self, cur_lang["opthm"], "", "Theme Files (*.thm);;All Files (*)")
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                for line in file.readlines():
                    if line.strip()[0:5] == "theme":
                        colort = line[6:-1].strip()
                    if line.strip()[0:5] == "fontc":
                        colorf = line[6:-1].strip()
            with open("settings.stp", 'w', encoding='utf-8') as f:
                print("theme "+ colort + "\nfontc " + colorf + "\nlang " + cur_lang["lang"], file=f)
            self.update_color()
            ex.update_color()

    def change_lang(self):
        global lang_rus
        global ex
        global lang_eng
        global cur_lang
        if cur_lang["lang"] == "ru":
            cur_lang = lang_eng
        elif cur_lang["lang"] == "en":
            cur_lang = lang_rus
        with open("settings.stp", 'w', encoding='utf-8') as f:
            print("theme " + colort + "\nfontc " + colorf + "\nlang " + cur_lang["lang"], file=f)
        self.update_lang()
        recentloc.update_color()
        ex.update_lang()

    def update_lang(self):
        global lang_rus
        global lang_eng
        self.setWindowTitle(cur_lang["setnt"])
        self.theme_import.setText(cur_lang["thmi"])
        self.labell.setText(cur_lang["lang"])
        self.labell.resize(self.labell.sizeHint())
        self.lang_ch.setText(cur_lang["lngc"])
        self.theme_btn.setText(cur_lang["thm"])

        if colort == "#E0E0E0":
            self.labelt.setText(cur_lang["thmtl"])
            self.labelt.resize(self.labelt.sizeHint())
        elif colort == "#404040":
            self.labelt.setText(cur_lang["thmtd"])
            self.labelt.resize(self.labelt.sizeHint())
        else:
            self.labelt.setText(cur_lang["thmtc"])
            self.labelt.resize(self.labelt.sizeHint())


if __name__ == '__main__':
    lang_rus = {"lang":"ru",
                "opf":"Открыть",
                "opas": "Открыть Файл",
                "opthm": "Открыть Тему",
                "svf":"Сохранить",
                "svdas":"Сохранено как",
                "setn":"Настройки",
                "svas":"Сохранить файл",
                "thm":"Тема",
                "thmi":"Импорт Темы",
                "thmtl":": Светлая",
                "thmtd": ": Темная",
                "thmtc": ": Своя",
                "lngc": "Язык",
                "setnt":"Настройки",
                "nott":"Записная Книжка",
                "rec": "Недавние файлы",
                "recb": "Недавние",}
    lang_eng = {"lang":"en",
                "opf": "Open",
                "opas": "Open File",
                "opthm": "Open Theme",
                "svf": "Save",
                "svdas": "Saved As",
                "setn": "Settings",
                "svas": "Save file",
                "thm": "Theme",
                "thmi": "Import Theme",
                "thmtl": ": Light",
                "thmtd": ": Dark",
                "thmtc": ": Custom",
                "lngc": "Language",
                "setnt": "Settings",
                "nott": "Notepad--",
                "rec": "Recent files",
                "recb": "Recents",}

    colort = ""
    colorf = ""
    cur_lang = lang_eng
    for lines in open("settings.stp").readlines():
        if lines.strip()[0:5] == "theme":
            colort = lines[6:-1].strip()
        if lines.strip()[0:5] == "fontc":
            colorf = lines[6:-1].strip()
        if lines.strip()[0:4] == "lang":
            if lines[5:-1].strip() == "ru":
                cur_lang = lang_rus
            if lines[5:-1].strip() == "en":
                cur_lang = lang_eng
    app = QApplication(sys.argv)
    ex = notepad(colort)
    recentloc = recentwindow()
    settingsloc = settings()
    ex.show()
    sys.exit(app.exec())
