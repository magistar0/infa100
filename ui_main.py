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
        self.setMinimumWidth(Config.multiplyNumberAccordingToSize(450, save_manager.getCurrentSettings()["size"]))
        self.setMinimumHeight(Config.multiplyNumberAccordingToSize(450, save_manager.getCurrentSettings()["size"]))
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

        self.grid.addWidget(self.lbl, 0, 0, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.logo_lbl, 1, 0, alignment=Qt.AlignCenter)
        self.grid.addItem(QSpacerItem(150, 150, QSizePolicy.Expanding, QSizePolicy.Expanding), 2, 0)
        self.grid.addWidget(self.btn_1, 3, 0)
        self.grid.addWidget(self.btn_2, 4, 0)
        self.grid.addWidget(self.btn_4, 5, 0)
        self.grid.addWidget(self.btn_5, 6, 0)
        self.grid.addWidget(self.btn_3, 7, 0)
        self.grid.setRowStretch(8, 1) 

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
        self.buttonN.setText(Localization.SITE_BUTTON)
        self.buttonN.clicked.connect(lambda: webbrowser.open('https://sga235.ru/infa100'))
        self.box.exec_()

class UI_StatsWindow(object):
    def setupUi(self, StatsWindow):
        self.setWindowTitle(Localization.STATS)
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.setMinimumWidth(Config.multiplyNumberAccordingToSize(450, save_manager.getCurrentSettings()["size"]))
        self.setMinimumHeight(Config.multiplyNumberAccordingToSize(450, save_manager.getCurrentSettings()["size"]))
        StatsWindow.resize(Config.multiplyNumberAccordingToSize(1000, save_manager.getCurrentSettings()["size"]),
                           Config.multiplyNumberAccordingToSize(600, save_manager.getCurrentSettings()["size"]))
        StatsWindow.move(150, 150)
        self.stats_already_generated = False

        self.stacked_widget = QStackedWidget()
        self.widget_1 = QWidget()
        self.grid = QGridLayout()

        self.lbl = QLabel(Localization.STATS_HEADER, self)
        self.lbl.setFont(QFont("SF Pro Display", Config.multiplyNumberAccordingToSize(30, save_manager.getCurrentSettings()["size"])))

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
        self.grid.addItem(QSpacerItem(250, 250, QSizePolicy.Expanding, QSizePolicy.Expanding), 1, 0)

        self.user_have_stats = save_manager.checkIfStatsIsAvailable()
        if self.user_have_stats:
            self.vars_ever_solved, self.average_first, self.average_ege = save_manager.getStats()
            self.most_correct, self.most_incorrect = save_manager.getMostSolvedTasks()
            self.stats_1 = Localization.STATS_VARS_COUNT_TEXT % (self.vars_ever_solved,
                Localization.__dict__["STATS_VARS_COUNT_" + Config.getCountEnding(self.vars_ever_solved).upper()])
            self.stats_2 = Localization.STATS_AVERAGE_RESULT_TEXT % (self.average_first, Localization.__dict__["POINTS_" + Config.getCountEnding(self.average_first).upper()],
                self.average_ege, Localization.__dict__["STATS_AVERAGE_POINTS_" + Config.getCountEnding(self.average_ege).upper()])
            if len(self.most_correct) == 1:
                self.stats_3 = Localization.STATS_MOST_TIMES_CORRECT_TEXT % (self.most_correct[0][0], 
                    self.most_correct[0][1], Localization.__dict__["STATS_TIMES_" + Config.getCountEnding(self.most_correct[0][1]).upper()])
            elif self.average_first == 0:
                self.stats_3 = ""
            else:
                self.correct_list_as_str = ", ".join(list(map(str, [tpl[0] for tpl in self.most_correct])))
                self.stats_3 = Localization.STATS_MOST_TIMES_CORRECT_TEXT_PLURAL % (self.correct_list_as_str, 
                    self.most_correct[0][1], Localization.__dict__["STATS_TIMES_" + Config.getCountEnding(self.most_correct[0][1]).upper()])
            if len(self.most_incorrect) == 1:
                self.stats_4 = Localization.STATS_MOST_TIMES_INCORRECT_TEXT % (self.most_incorrect[0][0], 
                    self.vars_ever_solved - self.most_incorrect[0][1], Localization.__dict__["STATS_TIMES_" + Config.getCountEnding(self.vars_ever_solved - self.most_incorrect[0][1]).upper()])
            else:
                self.incorrect_list_as_str = ", ".join(list(map(str, [tpl[0] for tpl in self.most_incorrect])))
                self.stats_4 = Localization.STATS_MOST_TIMES_INCORRECT_TEXT_PLURAL % (self.incorrect_list_as_str, 
                    self.vars_ever_solved - self.most_incorrect[0][1], Localization.__dict__["STATS_TIMES_" + Config.getCountEnding(self.vars_ever_solved - self.most_incorrect[0][1]).upper()])
            if self.stats_3:
                self.stats_text = self.stats_1 + "\n" + self.stats_2 + "\n" + self.stats_3 + "\n" + self.stats_4
            else:
                self.stats_text = self.stats_1 + "\n" + self.stats_2 + "\n" + self.stats_4
        else:
            self.why_unavailable = Localization.getPrintfText(save_manager.getUnavailableStatsDescriptionKey())
            self.stats_text = Localization.STATS_TEXT_EMPTY_HISTORY + "\n" + self.why_unavailable
        self.stats_lbl = QLabel(self.stats_text)
        self.stats_lbl.setWordWrap(True)
        self.stats_lbl.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.stats_lbl, 2, 0)
        self.grid.addItem(QSpacerItem(250, 250, QSizePolicy.Expanding, QSizePolicy.Expanding), 3, 0)

        self.stats = save_manager.getStats()
        if self.stats:
            if self.stats[0] >= 1:
                self.more_btn = QPushButton(Localization.HISTORY_BUTTON, self)
                self.more_btn.clicked.connect(self.more_clicked)
                self.reset_btn = QPushButton(Localization.RESET_STATS, self)
                self.reset_btn.clicked.connect(self.reset_clicked)
                self.grid.addWidget(self.more_btn, 4, 0)
                self.grid.addWidget(self.reset_btn, 5, 0)

        self.back_to_menu_btn = QPushButton(Localization.BACK_TO_MENU, self)
        self.back_to_menu_btn.clicked.connect(self.back_to_menu_btn_clicked)
        self.grid.addWidget(self.back_to_menu_btn, 6, 0)
        self.grid.setRowStretch(7, 1)

        self.widget_1.setLayout(self.grid)
        self.stacked_widget.addWidget(self.widget_1)
        self.stacked_widget.setCurrentIndex(0)
        self.setCentralWidget(self.stacked_widget)
        self.showMaximized()

    def back_to_menu_btn_clicked(self):
        self.win.translateToMain()

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
        self.buttonN.setText(Localization.SITE_BUTTON)
        self.buttonN.clicked.connect(lambda: webbrowser.open('https://sga235.ru/infa100'))
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

            self.scrollArea = QScrollArea()
            self.scrollArea.setWidgetResizable(True)

            self.history_lbl = QLabel(self.history_text)
            self.history_lbl.setWordWrap(True)
            self.history_lbl.setAlignment(Qt.AlignCenter)
            self.history_btn = QPushButton(Localization.BACK, self)
            self.history_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

            self.grid_2.addWidget(self.history_btn, 0, 0, 2, 0)
            self.grid_2.addWidget(self.history_lbl, 2, 0, 2, 0)
            self.widget_2.setLayout(self.grid_2)
            self.scrollArea.setWidget(self.widget_2)
            self.stacked_widget.addWidget(self.scrollArea)

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
        self.win.translateToMain()
        QMessageBox.information(self, Localization.RESET_STATS_TITLE, Localization.STATS_RESET_SUCCESS, QMessageBox.Ok)


class UI_Settings(object):
    def setupUi(self, SettingsWindow):
        current_settings = save_manager.getCurrentSettings()
        self.setMinimumSize(QSize(Config.multiplyNumberAccordingToSize(480, current_settings["size"]),
                                  Config.multiplyNumberAccordingToSize(240, current_settings["size"])))
        self.setMaximumHeight(Config.multiplyNumberAccordingToSize(400, current_settings["size"]))
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setWindowIcon(QIcon('icons/icon.png'))
 
        self.grid_layout = QGridLayout()
        self.central_widget.setLayout(self.grid_layout)

        self.available_sizes = ["tiny", "default", "big", "large"]
        if save_manager.checkIfEasterEggIsUnlocked():
            self.available_sizes.append("secret")
        self.combo = QComboBox()
        self.list_of_items = [Localization.getPrintfText(key) for key in self.available_sizes]
        self.combo.addItems(self.list_of_items)
        self.combo.setCurrentText(Localization.getPrintfText(current_settings["size"]))

        self.current_name, self.current_email = current_settings["name"], current_settings["email"]
        self.name_blank = QLineEdit()
        self.name_blank.setPlaceholderText(Localization.ENTER_NAME)
        self.email_blank = QLineEdit()
        self.email_blank.setPlaceholderText(Localization.ENTER_EMAIL)
        if self.current_name:
            self.name_blank.setText(self.current_name)
        if self.current_email:
            self.email_blank.setText(self.current_email)
 
        self.ok_btn = QPushButton(Localization.ACCEPT)
        self.cancel_btn = QPushButton(Localization.CANCEL)
        self.cancel_btn.clicked.connect(lambda: self.close())
        self.ok_btn.clicked.connect(self.ok_btn_clicked)

        self.grid_layout.addWidget(QLabel(Localization.SETTING_SIZE_TEXT, self), 0, 0, 1, 2)
        self.grid_layout.addWidget(self.combo, 1, 0, 1, 2)
        self.grid_layout.addWidget(QLabel(Localization.SETTINGS_NAME_TEXT, self), 2, 0, 1, 2)
        self.grid_layout.addWidget(self.name_blank, 3, 0, 1, 2)
        self.grid_layout.addWidget(QLabel(Localization.SETTINGS_EMAIL_TEXT, self), 4, 0, 1, 2)
        self.grid_layout.addWidget(self.email_blank, 5, 0, 1, 2)
        self.grid_layout.addWidget(self.ok_btn, 6, 0)
        self.grid_layout.addWidget(self.cancel_btn, 6, 1)
 
    def ok_btn_clicked(self):
        current_settings = save_manager.getCurrentSettings()
        new_settings = deepcopy(current_settings)

        sizes = {
            0: "tiny", 1: "default", 2: "big", 3: "large", 4: "secret"
        }
        size_index = self.combo.currentIndex()
        new_size = sizes[size_index]
        new_settings["size"] = new_size

        name = self.name_blank.text()
        email = self.email_blank.text()
        new_settings["name"] = name if name else None
        new_settings["email"] = email if email else None

        if (not save_manager.checkIfEasterEggIsUnlocked()) and Config.checkIfNameNeedsToBeTriggered(new_settings["name"]):
            QMessageBox.information(self, Localization.EMAIL_EASTEREGG_HEADER, Localization.EMAIL_EASTEREGG_TEXT, QMessageBox.Ok)
            save_manager.setEasterEggUnlocked()
        settings_was_changed = new_settings != current_settings
        reload_required = Config.checkIfSizeWasChanged(current_settings, new_settings)
        email_was_changed = new_settings["email"] != current_settings["email"]
        email_is_valid = True
        if email_was_changed:
            email_is_valid = Config.emailIsValid(new_settings["email"])
        if settings_was_changed and reload_required:
            if not email_is_valid:
                QMessageBox.information(self, Localization.WARNING_HEADER, Localization.EMAIL_WARNING_TEXT, QMessageBox.Ok)
            save_manager.updateSettings(new_settings)
            self.ask_for_reload()
        elif settings_was_changed:
            save_manager.updateSettings(new_settings)
        if not email_is_valid:
            QMessageBox.information(self, Localization.WARNING_HEADER, Localization.EMAIL_WARNING_TEXT, QMessageBox.Ok)
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