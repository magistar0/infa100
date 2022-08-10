import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication

from data_manager import Localization
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
    def __init__(self, parent=None):
        super(VarWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(Localization.VAR_WIN_TITLE)


class Main(QMainWindow, UI_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.btn_1.clicked.connect(self.show_window_2)
        self.btn_2.clicked.connect(self.show_window_3)

    def show_window_2(self):
        self.w2 = BaseWindow()
        self.w2.show()

    def show_window_3(self):
        self.w3 = VarWindow()
        self.w3.show()


if __name__ == "__main__":
    if not os.path.exists(save_manager.dir_path):
        os.makedirs(save_manager.dir_path)
    if not os.path.exists(save_manager.dir_path + 'user_save.save'):
        save_manager.generate_empty_save()
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec_())