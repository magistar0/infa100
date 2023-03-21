import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QInputDialog, QStackedWidget
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
import webbrowser

from data_manager import Localization, Config, ID_Vars, Logger
from ui_base import UI_BaseWindow
from ui_exam import UI_VarWindow
from ui_main import UI_MainWindow, UI_StatsWindow, UI_Settings
import save_manager


class BaseWindow(QMainWindow, UI_BaseWindow):
    def __init__(self, parent=None):
        super(BaseWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(Localization.BASE_WIN_TITLE)

class StatsWindow(QMainWindow, UI_StatsWindow):
    def __init__(self, parent=None):
        super(StatsWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(Localization.STATS)

class SettingsWindow(QMainWindow, UI_Settings):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(Localization.SETTINGS)

class VarWindow(QMainWindow, UI_VarWindow):
    by_id = False
    var_id = None
    def __init__(self, parent=None):
        super(VarWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(Localization.VAR_WIN_TITLE)

    def setByIdClass(by_id: bool):
        VarWindow.by_id = by_id

    def setByIdSelf(self):
        self.by_id = VarWindow.by_id

    def setVarIdClass(id: str):
        VarWindow.var_id = id

    def setVarIdSelf(self):
        self.var_id = VarWindow.var_id


class Main(QMainWindow, UI_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.btn_1.clicked.connect(self.show_window_2)
        self.btn_2.clicked.connect(self.window_3_dialogAction)
        self.btn_4.clicked.connect(self.show_window_4)
        self.btn_5.clicked.connect(self.show_window_5)
        
    def show_window_2(self):
        win.translateToBase()

    def show_window_3(self):
        win.translateToVar()

    def show_window_4(self):
        win.translateToStats()

    def show_window_5(self):
        self.w5 = SettingsWindow()
        self.w5.show()

    def dialogAction_no_clicked(self):
        self.no_clicked = True

    def window_3_dialogAction(self):
        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setWindowIcon(QIcon('icons/icon.png'))
        box.setWindowTitle(Localization.VAR_WIN_TITLE)
        box.setText(Localization.BYID_DIALOG_QUESTION)
        box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText(Localization.BYID_DIALOG_OPTION_0)
        buttonN = box.button(QMessageBox.No)
        buttonN.setText(Localization.BYID_DIALOG_OPTION_1)
        self.no_clicked = False
        buttonN.clicked.connect(self.dialogAction_no_clicked)
        box.exec_()

        if box.clickedButton() == buttonY:
            VarWindow.setByIdClass(False)
            VarWindow.setVarIdClass(None)
            self.show_window_3()
        elif box.clickedButton() == buttonN and self.no_clicked:
            if not Config.checkInternetConnection():
                QMessageBox.critical(self, Localization.EMAIL_ERROR_HEADER, Localization.BYID_ERROR_1, QMessageBox.Ok)
            else:
                VarWindow.setByIdClass(True)
                self.to_pass_var_id, self.ok = QInputDialog.getText(self, Localization.BYID_ASK_HEADER,
                    Localization.BYID_ASK_TEXT, flags=Qt.WindowCloseButtonHint)
                VarWindow.setVarIdClass(self.to_pass_var_id)
                self.id_is_valid = ID_Vars.check_if_id_is_valid(VarWindow.var_id)
                if self.ok and self.id_is_valid:
                    self.show_window_3()
                elif not self.ok:
                    pass
                elif not self.id_is_valid:
                    QMessageBox.critical(self, Localization.EMAIL_ERROR_HEADER, Localization.BYID_ERROR_0, QMessageBox.Ok)
                else: 
                    pass


class CoreMain(QMainWindow):
    def __init__(self):
        super(CoreMain, self).__init__()
        self.basew = None
        self.statsw = None
        self.varw = None
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle(Localization.MAIN_WIN_TITLE)
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.setMinimumWidth(Config.multiplyNumberAccordingToSize(450, save_manager.getCurrentSettings()["size"]))
        self.setMinimumHeight(Config.multiplyNumberAccordingToSize(450, save_manager.getCurrentSettings()["size"]))
        self.showMaximized()

        self.w = QStackedWidget()
        self.mainw = Main()
        self.w.addWidget(self.mainw)

        self.setCentralWidget(self.w)

    def translateToBase(self):
        if self.basew is None:
            self.basew = BaseWindow()
            self.w.addWidget(self.basew)
        self.basew.win = win
        self.w.setCurrentWidget(self.basew)

    def translateToVar(self):
        if self.varw is None:
            self.varw = VarWindow()
            self.w.addWidget(self.varw)
        self.w.setCurrentWidget(self.varw)

    def translateToStats(self):
        if self.statsw is None:
            self.statsw = StatsWindow()
            self.w.addWidget(self.statsw)
        self.w.setCurrentWidget(self.statsw)

    def translateToMain(self):
        self.w.setCurrentWidget(self.mainw)


def load_fonts_from_dir(directory):
    families = set()
    for fi in QDir(directory).entryInfoList(["*.ttf", "*.otf"]):
        _id = QFontDatabase.addApplicationFont(fi.absoluteFilePath())
        families |= set(QFontDatabase.applicationFontFamilies(_id))
    return families


if __name__ == "__main__":
    if not os.path.exists(save_manager.dir_path):
        os.makedirs(save_manager.dir_path)
    if not os.path.exists(save_manager.dir_path + 'user_save.save'):
        save_manager.generate_empty_save()
    if not os.path.exists(Logger.log_path):
        Logger.generate_empty_log()
    if not "settings" in save_manager.read_save():
        save_manager.addSettingsParameter()
    if not "easteregg_unlocked" in save_manager.read_save():
        save_manager.addEasterEggParameter()
    if not "name" in save_manager.read_save()["settings"]:
        save_manager.addNameEmailParameters()
    if not "19-21" in save_manager.read_save()["save_data"]:
        save_manager.change19_21SaveFormat()

    
    currentExitCode = 1337
    while currentExitCode == 1337:
        app = QApplication(sys.argv)

        program_size = save_manager.getCurrentSettings()["size"]
        families = load_fonts_from_dir(os.fspath("fonts/"))
        db = QFontDatabase()
        font_style = Config.getFontStyleFromSize(program_size)
        font = db.font("SF Pro Display", font_style, 10)
        font_size = Config.getFontSize(program_size)
        font.setPointSize(font_size)
        app.setFont(font)

        win = CoreMain()
        win.show()

        if Config.checkInternetConnection():
            if not Config.checkIfBuildIsLatest():
                update_box = QMessageBox()
                update_box.setIcon(QMessageBox.Information)
                update_box.setWindowIcon(QIcon('icons/icon.png'))
                update_box.setWindowTitle(Localization.UPDATE_HEADER)
                update_box.setText(Localization.UPDATE_TEXT)
                update_box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                buttonY = update_box.button(QMessageBox.Yes)
                buttonY.setText(Localization.UPDATE_YES)
                buttonY.clicked.connect(lambda: webbrowser.open('https://sga235.ru/infa100'))
                buttonN = update_box.button(QMessageBox.No)
                buttonN.setText(Localization.UPDATE_NO)
                update_box.exec_()
        currentExitCode = app.exec_()
        app = None