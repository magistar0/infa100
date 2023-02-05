import webbrowser
import sys
from copy import deepcopy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QFont, QPixmap

from data_manager import Localization, Config
import save_manager


class UI_MainWindow(object):
    def setupUi(self, MainWindow):
        self.setWindowTitle(Localization.MAIN_WIN_TITLE)
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.setMinimumWidth(Config.multiplyNumberAccordingToSize(300, save_manager.getCurrentSettings()["size"]))
        self.setMinimumHeight(Config.multiplyNumberAccordingToSize(300, save_manager.getCurrentSettings()["size"]))
        MainWindow.resize(Config.multiplyNumberAccordingToSize(1000, save_manager.getCurrentSettings()["size"]),
                           Config.multiplyNumberAccordingToSize(600, save_manager.getCurrentSettings()["size"]))

        self.widget = QWidget()
        self.grid = QGridLayout()

        self.lbl = QLabel(Localization.MAIN_HEADER, self)
        self.lbl.setFont(QFont("SF Pro Display", Config.multiplyNumberAccordingToSize(45, save_manager.getCurrentSettings()["size"])))

        self.logo_path = 'icons/icon.png'
        self.logo = QPixmap(self.logo_path)
        self.logo_lbl = QLabel(self)
        self.logo_lbl.setPixmap(self.logo)

        self.btn_1 = QPushButton(Localization.BASE_BUTTON, self)
        self.btn_2 = QPushButton(Localization.VAR_BUTTON, self)
        self.btn_4 = QPushButton(Localization.STATS, self)
        self.btn_5 = QPushButton(Localization.SETTINGS, self)
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
        self.grid.addWidget(self.btn_5, 6, 0, 7, 0)
        self.grid.addWidget(self.btn_3, 7, 0, 8, 0)

        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)
        self.showMaximized()

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
        self.setMinimumWidth(Config.multiplyNumberAccordingToSize(300, save_manager.getCurrentSettings()["size"]))
        self.setMinimumHeight(Config.multiplyNumberAccordingToSize(300, save_manager.getCurrentSettings()["size"]))
        StatsWindow.resize(Config.multiplyNumberAccordingToSize(1000, save_manager.getCurrentSettings()["size"]),
                           Config.multiplyNumberAccordingToSize(600, save_manager.getCurrentSettings()["size"]))
        StatsWindow.move(150, 150)
        self.stats_already_generated = False

        self.stacked_widget = QStackedWidget()
        self.widget_1 = QWidget()
        self.grid = QGridLayout()

        self.lbl = QLabel(Localization.STATS_HEADER, self)
        self.lbl.setFont(QFont('Arial', Config.multiplyNumberAccordingToSize(15, save_manager.getCurrentSettings()["size"])))

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

        self.user_have_stats = bool(save_manager.getStats())
        if self.user_have_stats:
            self.vars_ever_solved, self.average_first, self.average_ege = save_manager.getStats()
            self.most_correct, self.most_incorrect = save_manager.getMostSolvedTasks()
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
        self.showMaximized()

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
            self.history = save_manager.getExamHistory()
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


class UI_Settings(object):
    check_box = None
 
    def setupUi(self, SettingsWindow):
        self.setMinimumSize(QSize(Config.multiplyNumberAccordingToSize(480, save_manager.getCurrentSettings()["size"]),
                                  Config.multiplyNumberAccordingToSize(240, save_manager.getCurrentSettings()["size"])))
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.setWindowIcon(QIcon('icons/icon.png'))
 
        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)
        grid_layout.addWidget(QLabel(Localization.SETTING_SIZE_TEXT, self), 0, 0)

        self.combo = QComboBox()
        self.list_of_items = [Localization.getPrintfText(key) for key in ["tiny", "default", "big", "large"]]
        self.combo.addItems(self.list_of_items)
        self.combo.setCurrentText(Localization.getPrintfText(save_manager.getCurrentSettings()["size"]))
 
        self.ok_btn = QPushButton(Localization.ACCEPT)
        self.cancel_btn = QPushButton(Localization.CANCEL)
        self.cancel_btn.clicked.connect(lambda: self.close())
        self.ok_btn.clicked.connect(self.ok_btn_clicked)

        grid_layout.addWidget(self.combo, 1, 0, 1, 2)
        grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding), 2, 0, 1, 2)
        grid_layout.addWidget(self.ok_btn, 3, 0)
        grid_layout.addWidget(self.cancel_btn, 3, 1)
 
    def ok_btn_clicked(self):
        sizes = {
            0: "tiny", 1: "default", 2: "big", 3: "large"
        }
        size_index = self.combo.currentIndex()
        current_settings = save_manager.getCurrentSettings()
        new_settings = deepcopy(current_settings)

        new_size = sizes[size_index]
        new_settings["size"] = new_size
        if not new_settings == current_settings:
            save_manager.updateSettings(new_settings)
            self.ask_for_reload()
        else:
            self.close()

    def ask_for_reload(self):
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setWindowIcon(QIcon('icons/icon.png'))
        box.setWindowTitle(Localization.RELOAD_TITLE)
        box.setText(Localization.RELOAD_REQUIRED_TEXT)
        box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText(Localization.RELOAD_NOW)
        buttonN = box.button(QMessageBox.No)
        buttonN.setText(Localization.RELOAD_LATER)
        box.exec_()

        if box.clickedButton() == buttonY:
            self.close()
            QCoreApplication.exit(1337)
        elif box.clickedButton() == buttonN:
            self.close()