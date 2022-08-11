import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView

from data_manager import Localization, Config


class UI_MainWindow(object):
    def setupUi(self, MainWindow):
        self.setWindowTitle(Localization.MAIN_WIN_TITLE) # заголовок окна
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.setMinimumWidth(300)
        self.setMinimumHeight(300)
        MainWindow.resize(1000, 600)

        self.widget = QWidget()
        self.grid = QGridLayout()

        self.lbl = QLabel(Localization.MAIN_HEADER, self)
        self.lbl.setFont(QFont('Arial', 20))

        self.btn_1 = QPushButton(Localization.BASE_BUTTON, self)
        self.btn_2 = QPushButton(Localization.VAR_BUTTON, self)
        self.btn_3 = QPushButton(Localization.EXIT_BUTTON, self)
        self.btn_3.clicked.connect(QApplication.instance().quit)

        self.exitAction = QAction(QIcon('icons/exit.png'), '&' + Localization.EXIT, self)
        self.exitAction.setShortcut(Localization.EXIT_SHORTCUT)
        self.exitAction.setStatusTip(Localization.EXIT_STATUS_TIP)
        self.exitAction.triggered.connect(qApp.quit)

        self.infoAction_var = QAction(QIcon('icons/info.png'), '&' + Localization.HELP, self)
        self.infoAction_var.setStatusTip(Localization.HELP_STATUS_TIP)
        self.infoAction_var.triggered.connect(self.infoAction)
        self.statusBar()

        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&' + Localization.FILE)
        self.fileMenu.addAction(self.infoAction_var)
        self.fileMenu.addAction(self.exitAction)

        self.grid.setSpacing(10)
        self.grid.addWidget(self.lbl, 1, 0, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.btn_1, 2, 0, 4, 0)
        self.grid.addWidget(self.btn_2, 3, 0, 5, 0)
        self.grid.addWidget(self.btn_3, 4, 0, 6, 0)

        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)

    def infoAction(self):
        self.box = QMessageBox()
        self.box.setIcon(QMessageBox.Question)
        self.box.setWindowIcon(QIcon('icons/icon.png'))
        self.box.setWindowTitle(Localization.HELP)
        self.box.setText(Localization.HELP_TEXT % Config.build)
        self.box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        self.buttonY = self.box.button(QMessageBox.Yes)
        self.buttonY.setText(Localization.HELP_BUTTON)
        self.buttonY.clicked.connect(lambda: webbrowser.open('https://forms.gle/GZUVBykDbkdH5gXp9'))
        self.buttonN = self.box.button(QMessageBox.No)
        self.buttonN.setVisible(False)
        self.box.exec_()