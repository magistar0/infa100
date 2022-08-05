from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QFont

from data_manager import Localization


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

        exitAction = QAction(QIcon('icons/exit.png'), '&' + Localization.EXIT, self)
        exitAction.setShortcut(Localization.EXIT_SHORTCUT)
        exitAction.setStatusTip(Localization.EXIT_STATUS_TIP)
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&' + Localization.FILE)
        fileMenu.addAction(exitAction)

        self.grid.setSpacing(10)
        self.grid.addWidget(self.lbl, 1, 0, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.btn_1, 2, 0, 4, 0)
        self.grid.addWidget(self.btn_2, 3, 0, 5, 0)
        self.grid.addWidget(self.btn_3, 4, 0, 6, 0)

        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)