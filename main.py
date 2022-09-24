import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from data_manager import Localization, Config, ID_Vars, Logger
from ui_base import UI_BaseWindow
from ui_exam import UI_VarWindow
from ui_main import UI_MainWindow
import save_manager


class BaseWindow(QMainWindow, UI_BaseWindow):
    def __init__(self, parent=None):
        super(BaseWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(Localization.BASE_WIN_TITLE)


class VarWindow(QMainWindow, UI_VarWindow):
    by_id = False
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

    def show_window_2(self):
        self.w2 = BaseWindow()
        self.w2.show()

    def show_window_3(self):
        self.w3 = VarWindow()
        self.w3.show()

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


if __name__ == "__main__":
    if not os.path.exists(save_manager.dir_path):
        os.makedirs(save_manager.dir_path)
    if not os.path.exists(save_manager.dir_path + 'user_save.save'):
        save_manager.generate_empty_save()
    if not os.path.exists(Logger.log_path):
        Logger.generate_empty_log()
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    if Config.checkInternetConnection():
        if not Config.checkIfBuildIsLatest():
            update_box = QMessageBox()
            update_box.setIcon(QMessageBox.Information)
            update_box.setWindowIcon(QIcon('icons/icon.png'))
            update_box.setWindowTitle(Localization.UPDATE_HEADER)
            update_box.setText(Localization.UPDATE_TEXT)
            update_box.exec_()
    sys.exit(app.exec_())