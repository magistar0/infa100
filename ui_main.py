import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QFont, QPixmap

from data_manager import Localization, Config
import save_manager


class UI_MainWindow(object):
    def setupUi(self, MainWindow):
        self.setWindowTitle(Localization.MAIN_WIN_TITLE)
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.setMinimumWidth(300)
        self.setMinimumHeight(300)
        MainWindow.resize(1000, 600)

        self.widget = QWidget()
        self.grid = QGridLayout()

        self.lbl = QLabel(Localization.MAIN_HEADER, self)
        self.lbl.setFont(QFont('Arial', 20))

        self.logo_path = 'icons/icon.png'
        self.logo = QPixmap(self.logo_path)
        self.logo_lbl = QLabel(self)
        self.logo_lbl.setPixmap(self.logo)

        self.btn_1 = QPushButton(Localization.BASE_BUTTON, self)
        self.btn_2 = QPushButton(Localization.VAR_BUTTON, self)
        self.btn_4 = QPushButton(Localization.STATS, self)
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
        self.grid.addWidget(self.lbl, 0, 0, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.logo_lbl, 2, 0, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.btn_1, 3, 0, 4, 0)
        self.grid.addWidget(self.btn_2, 4, 0, 5, 0)
        self.grid.addWidget(self.btn_4, 5, 0, 6, 0)
        self.grid.addWidget(self.btn_3, 6, 0, 7, 0)

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

class UI_StatsWindow(object):
    def setupUi(self, StatsWindow):
        self.setWindowTitle(Localization.STATS)
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.setMinimumWidth(300)
        self.setMinimumHeight(300)
        StatsWindow.resize(1000, 600)
        StatsWindow.move(150, 150)
        self.stats_already_generated = False

        self.stacked_widget = QStackedWidget()
        self.widget_1 = QWidget()
        self.grid = QGridLayout()

        self.lbl = QLabel(Localization.STATS_HEADER, self)
        self.lbl.setFont(QFont('Arial', 15))

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

        self.grid.addWidget(self.lbl, 0, 0, alignment=Qt.AlignCenter)

        self.user_have_stats = bool(Config.getStats())
        if self.user_have_stats:
            self.vars_ever_solved, self.average_first, self.average_ege = Config.getStats()
            self.most_correct, self.most_incorrect = Config.getMostSolvedTasks()
            self.stats_1 = Localization.STATS_VARS_COUNT_TEXT % (self.vars_ever_solved,
                Localization.__dict__["STATS_VARS_COUNT_" + Config.getCountEnding(self.vars_ever_solved).upper()])
            self.stats_2 = Localization.STATS_AVERAGE_RESULT_TEXT % (self.average_first, Localization.__dict__["POINTS_" + Config.getCountEnding(self.average_first).upper()],
                self.average_ege, Localization.__dict__["STATS_AVERAGE_POINTS_" + Config.getCountEnding(self.average_ege).upper()])
            self.stats_3 = Localization.STATS_MOST_TIMES_CORRECT_TEXT % (self.most_correct[0], 
                self.most_correct[1], Localization.__dict__["STATS_TIMES_" + Config.getCountEnding(self.most_correct[1]).upper()])
            self.stats_4 = Localization.STATS_MOST_TIMES_INCORRECT_TEXT % (self.most_incorrect[0], 
                self.most_incorrect[1], Localization.__dict__["STATS_TIMES_" + Config.getCountEnding(self.most_incorrect[1]).upper()])
            self.stats_text = self.stats_1 + "\n" + self.stats_2 + "\n" + self.stats_3 + "\n" + self.stats_4
        else:
            self.stats_text = Localization.STATS_TEXT_EMPTY_HISTORY
        self.stats_lbl = QLabel(self.stats_text)
        self.stats_lbl.setWordWrap(True)
        self.stats_lbl.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.stats_lbl, 1, 0, 2, 0)

        if self.user_have_stats:
            self.more_btn = QPushButton(Localization.HISTORY_BUTTON, self)
            self.more_btn.clicked.connect(self.more_clicked)
            self.reset_btn = QPushButton(Localization.RESET_STATS, self)
            self.reset_btn.clicked.connect(self.reset_clicked)
            self.grid.addWidget(self.more_btn, 2, 0, 2, 0)
            self.grid.addWidget(self.reset_btn, 3, 0, 2, 0)

        self.widget_1.setLayout(self.grid)
        self.stacked_widget.addWidget(self.widget_1)
        self.stacked_widget.setCurrentIndex(0)
        self.setCentralWidget(self.stacked_widget)

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

    def more_clicked(self):
        if not self.stats_already_generated:
            self.history = Config.getExamHistory()
            self.history_text = ""
            k = 1
            for exam in self.history:
                self.points_form = Config.getCountEnding(exam[1])
                self.points_form_text = Localization.__dict__["POINTS_" + self.points_form.upper()]
                self.history_text += Localization.HISTORY_DATE_AND_TIME % (k, exam[0]) + "\n" + Localization.HISTORY_RESULT % (exam[1], self.points_form_text)
                self.history_text += "\n\n"
                k += 1

            self.stats_already_generated = True
            self.widget_2 = QWidget()
            self.grid_2 = QGridLayout()

            self.history_lbl = QLabel(self.history_text)
            self.history_lbl.setWordWrap(True)
            self.history_lbl.setAlignment(Qt.AlignCenter)
            self.history_btn = QPushButton(Localization.BACK, self)
            self.history_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

            self.grid_2.addWidget(self.history_lbl, 1, 0, 2, 0)
            self.grid_2.addWidget(self.history_btn, 0, 0, 2, 0)
            self.widget_2.setLayout(self.grid_2)
            self.stacked_widget.addWidget(self.widget_2)

        self.stacked_widget.setCurrentIndex(1)

    def reset_clicked(self):
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setWindowIcon(QIcon('icons/icon.png'))
        box.setWindowTitle(Localization.RESET_STATS_TITLE)
        box.setText(Localization.RESET_STATS_CONFIRM)
        box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText(Localization.YES)
        buttonN = box.button(QMessageBox.No)
        buttonN.setText(Localization.NO)
        buttonY.clicked.connect(self.clear_confirmed)
        box.exec_()
    
    def clear_confirmed(self):
        save_manager.clear_exam_history()
        self.close()
        QMessageBox.information(self, Localization.RESET_STATS_TITLE, Localization.STATS_RESET_SUCCESS, QMessageBox.Ok)