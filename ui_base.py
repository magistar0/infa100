import os
import shutil
import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap, QFont

from task_manager import Task_Chooser
from data_manager import Localization, Config, Logger
import save_manager


class UI_BaseWindow(object):
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

    def back_btn_clicked(self):
        self.menubar_var.clear()
        self.setupUi_continue()

    def setupUi_continue(self):
        self.setWindowTitle(Localization.BASE_WIN_TITLE)
        self.setWindowIcon(QIcon('icons/icon.png'))

        self.exitAction_var = QAction(QIcon('icons/exit.png'), '&' + Localization.EXIT, self)
        self.exitAction_var.setShortcut(Localization.EXIT_SHORTCUT)
        self.exitAction_var.setStatusTip(Localization.EXIT_STATUS_TIP)
        self.exitAction_var.triggered.connect(qApp.quit)

        self.infoAction_var = QAction(QIcon('icons/info.png'), '&' + Localization.HELP, self)
        self.infoAction_var.setStatusTip(Localization.HELP_STATUS_TIP)
        self.infoAction_var.triggered.connect(self.infoAction)
        self.statusBar()

        self.menubar_var = self.menuBar()
        self.fileMenu_var = self.menubar_var.addMenu('&' + Localization.FILE)
        self.fileMenu_var.addAction(self.infoAction_var)
        self.fileMenu_var.addAction(self.exitAction_var)

        self.lbl = QLabel(Localization.CHOOSE_TASK, self)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.show_btn = QPushButton(Localization.SHOW, self)
        self.show_btn.clicked.connect(self.show_btn_clicked)

        self.back_to_menu_btn = QPushButton(Localization.BACK_TO_MENU, self)
        self.back_to_menu_btn.clicked.connect(self.back_to_menu_btn_clicked)

        self.centralWidget = QWidget()
        self.combo = QComboBox()
        self.list_of_items = [Localization.TASK + str(num) for num in range(1, 19)] + [Localization.TASKS + "19-21"] + [Localization.TASK + str(num) for num in range(22, 28)]
        self.combo.addItems(self.list_of_items)
        if self.combo_last_picked_index is not None:
            self.combo.setCurrentIndex(self.combo_last_picked_index)

        self.grid = QGridLayout()
        self.grid.addWidget(self.lbl, 0, 0)
        self.grid.addItem(QSpacerItem(250, 250, QSizePolicy.Expanding, QSizePolicy.Expanding), 1, 0)
        self.grid.addWidget(self.combo, 2, 0)
        self.grid.addWidget(self.show_btn, 3, 0)
        self.grid.addItem(QSpacerItem(250, 250, QSizePolicy.Expanding, QSizePolicy.Expanding), 4, 0)
        self.grid.addWidget(self.back_to_menu_btn, 5, 0)
        self.grid.setRowStretch(6, 1) 
        
        self.centralWidget.setLayout(self.grid)
        self.setCentralWidget(self.centralWidget)
        self.showMaximized()

    def back_to_menu_btn_clicked(self):
        self.win.translateToMain()

    def show_btn_clicked(self):
        task_num = self.combo.currentText().replace(Localization.TASK, '').replace(Localization.TASKS, '')
        self.combo_last_picked_index = self.combo.currentIndex()

        self.lbl2_text = Localization.TASK_HEADER if task_num != "19-21" else Localization.TASKS_HEADER
        self.lbl2 = QLabel(self.lbl2_text % task_num, self)
        self.lbl2.setFont(QFont("SF Pro Display", Config.multiplyNumberAccordingToSize(22, save_manager.getCurrentSettings()["size"])))
        self.back_btn = QPushButton(Localization.BACK, self)
        self.back_btn.clicked.connect(self.back_btn_clicked)

        # 1111111111
        self.task_1_widget = QWidget()
        self.task_1_data = Task_Chooser.choose_task(1)
        self.task_1_text = QLabel(self.task_1_data['text'])
        self.task_1_text.setWordWrap(True)
        self.task_1_text.setAlignment(Qt.AlignCenter)
        self.task_1_answer = QLabel(Localization.ANSWER + self.task_1_data['answer'])
        self.task_1_answer.setWordWrap(True)
        self.task_1_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_1_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_1_description = self.task_1_data['description']
        self.task_1_description_widget = QLabel(self.task_1_description)
        self.task_1_description_widget.setWordWrap(True)
        self.task_1_widget_clicked_grid = QGridLayout()

        self.task_1_picture_path = 'data/tasks_data/1/' + self.task_1_data['id'] + '.png'
        self.task_1_picture_exists = True if os.path.exists(self.task_1_picture_path) else False
        if self.task_1_picture_exists:
            self.task_1_picture = QPixmap(self.task_1_picture_path)
            self.task_1_picture_lbl = QLabel(self)
            self.task_1_picture_lbl.setPixmap(self.task_1_picture)
        
        self.task_1_widget_clicked_grid.addWidget(self.task_1_text, 0, 0)
        self.t1k = 0
        if self.task_1_picture_exists:
            self.t1k = 1
            self.task_1_widget_clicked_grid.addWidget(self.task_1_picture_lbl, 1, 0, alignment=Qt.AlignCenter)
        self.task_1_widget_clicked_grid.addWidget(self.task_1_show_ans_btn, 1 + self.t1k, 0)
        self.task_1_widget_clicked_grid.addWidget(self.task_1_show_descr_btn, 2 + self.t1k, 0)
        self.task_1_widget_clicked_grid.setRowStretch(4, 1) 
        self.task_1_widget.setLayout(self.task_1_widget_clicked_grid)

        def task_1_ans_button_clicked():
            self.task_1_show_ans_btn.setParent(None)
            self.task_1_widget_clicked_grid.addWidget(self.task_1_answer, 1 + self.t1k, 0)
        def task_1_descr_button_clicked():
            self.task_1_show_descr_btn.setParent(None)
            self.task_1_widget_clicked_grid.addWidget(self.task_1_description_widget, 2 + self.t1k, 0)

        self.task_1_show_ans_btn.clicked.connect(task_1_ans_button_clicked)
        self.task_1_show_descr_btn.clicked.connect(task_1_descr_button_clicked)


        # 222222222
        self.task_2_widget = QWidget()
        self.task_2_data = Task_Chooser.choose_task(2)
        self.task_2_text = QLabel(self.task_2_data['text'])
        self.task_2_text.setWordWrap(True)
        self.task_2_text.setAlignment(Qt.AlignCenter)
        self.task_2_answer = QLabel(Localization.BASE_ANSWER + self.task_2_data['answer'])
        self.task_2_answer.setWordWrap(True)
        self.task_2_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_2_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_2_description = self.task_2_data['description']
        self.task_2_description_widget = QLabel(self.task_2_description)
        self.task_2_description_widget.setWordWrap(True)
        self.task_2_widget_clicked_grid = QGridLayout()

        self.task_2_picture_path = 'data/tasks_data/2/' + self.task_2_data['id'] + '.png'
        self.task_2_picture_exists = True if os.path.exists(self.task_2_picture_path) else False
        if self.task_2_picture_exists:
            self.task_2_picture = QPixmap(self.task_2_picture_path)
            self.task_2_picture_lbl = QLabel(self)
            self.task_2_picture_lbl.setPixmap(self.task_2_picture)
        
        self.task_2_widget_clicked_grid.addWidget(self.task_2_text, 0, 0)
        self.t2k = 0
        if self.task_2_picture_exists:
            self.t2k = 1
            self.task_2_widget_clicked_grid.addWidget(self.task_2_picture_lbl, 1, 0, alignment=Qt.AlignCenter)
        self.task_2_widget_clicked_grid.addWidget(self.task_2_show_ans_btn, 1 + self.t2k, 0)
        self.task_2_widget_clicked_grid.addWidget(self.task_2_show_descr_btn, 2 + self.t2k, 0)
        self.task_2_widget_clicked_grid.setRowStretch(4, 1) 
        self.task_2_widget.setLayout(self.task_2_widget_clicked_grid)

        def task_2_ans_button_clicked():
            self.task_2_show_ans_btn.setParent(None)
            self.task_2_widget_clicked_grid.addWidget(self.task_2_answer, 1 + self.t2k, 0)
        def task_2_descr_button_clicked():
            self.task_2_show_descr_btn.setParent(None)
            self.task_2_widget_clicked_grid.addWidget(self.task_2_description_widget, 2 + self.t2k, 0)

        self.task_2_show_ans_btn.clicked.connect(task_2_ans_button_clicked)
        self.task_2_show_descr_btn.clicked.connect(task_2_descr_button_clicked)


        # 3333333333333333
        self.task_3_widget = QWidget()
        self.task_3_data = Task_Chooser.choose_task(3)

        self.task_3_text1 = QLabel(self.task_3_data['text1'])
        self.task_3_text1.setWordWrap(True)
        self.task_3_text1.setAlignment(Qt.AlignCenter)
        self.task_3_text2 = QLabel(self.task_3_data['text2'])
        self.task_3_text2.setWordWrap(True)
        self.task_3_text2.setAlignment(Qt.AlignCenter)
        self.task_3_text3 = QLabel(self.task_3_data['text3'])
        self.task_3_text3.setAlignment(Qt.AlignCenter)
        self.task_3_text4 = QLabel(self.task_3_data['text4'])
        self.task_3_text3.setWordWrap(True)
        self.task_3_text4.setWordWrap(True)
        self.task_3_text4.setAlignment(Qt.AlignCenter)
        self.task_3_text5 = QLabel(self.task_3_data['text5'])
        self.task_3_text5.setWordWrap(True)
        self.task_3_text5.setAlignment(Qt.AlignCenter)
        self.task_3_text6 = QLabel(self.task_3_data['text6'])
        self.task_3_text6.setWordWrap(True)
        self.task_3_text6.setAlignment(Qt.AlignCenter)

        self.task_3_answer = QLabel(Localization.BASE_ANSWER + self.task_3_data['answer'])
        self.task_3_answer.setWordWrap(True)
        self.task_3_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_3_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_3_description = self.task_3_data['description']
        self.task_3_description_widget = QLabel(self.task_3_description)
        self.task_3_description_widget.setWordWrap(True)
        self.task_3_widget_clicked_grid = QGridLayout()

        self.task_3_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_3_file_path = 'data/tasks_data/3/' + self.task_3_data['id'] + '.xlsx'

        self.task_3_picture_2to3_path = 'data/tasks_data/3/' + self.task_3_data['id'] + '_2to3.png'
        self.task_3_picture_2to3 = QPixmap(self.task_3_picture_2to3_path)
        self.task_3_picture_2to3_lbl = QLabel(self)
        self.task_3_picture_2to3_lbl.setPixmap(self.task_3_picture_2to3)
        self.task_3_picture_3to4_path = 'data/tasks_data/3/' + self.task_3_data['id'] + '_3to4.png'
        self.task_3_picture_3to4 = QPixmap(self.task_3_picture_3to4_path)
        self.task_3_picture_3to4_lbl = QLabel(self)
        self.task_3_picture_3to4_lbl.setPixmap(self.task_3_picture_3to4)
        self.task_3_picture_4to5_path = 'data/tasks_data/3/' + self.task_3_data['id'] + '_4to5.png'
        self.task_3_picture_4to5 = QPixmap(self.task_3_picture_4to5_path)
        self.task_3_picture_4to5_lbl = QLabel(self)
        self.task_3_picture_4to5_lbl.setPixmap(self.task_3_picture_4to5)
        self.task_3_picture_5to6_path = 'data/tasks_data/3/' + self.task_3_data['id'] + '_5to6.png'
        self.task_3_picture_5to6 = QPixmap(self.task_3_picture_5to6_path)
        self.task_3_picture_5to6_lbl = QLabel(self)
        self.task_3_picture_5to6_lbl.setPixmap(self.task_3_picture_5to6)
        
        self.task_3_widget_clicked_grid.addWidget(self.task_3_text1, 0, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_get_file_btn, 1, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_text2, 2, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_picture_2to3_lbl, 3, 0, alignment=Qt.AlignCenter)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_text3, 4, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_picture_3to4_lbl, 5, 0, alignment=Qt.AlignCenter)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_text4, 6, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_picture_4to5_lbl, 7, 0, alignment=Qt.AlignCenter)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_text5, 8, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_picture_5to6_lbl, 9, 0, alignment=Qt.AlignCenter)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_text6, 10, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_show_ans_btn, 11, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_show_descr_btn, 12, 0)
        self.task_3_widget_clicked_grid.setRowStretch(13, 1) 
        self.task_3_widget.setLayout(self.task_3_widget_clicked_grid)

        def task_3_ans_button_clicked():
            self.task_3_show_ans_btn.setParent(None)
            self.task_3_widget_clicked_grid.addWidget(self.task_3_answer, 11, 0)
        def task_3_descr_button_clicked():
            self.task_3_show_descr_btn.setParent(None)
            self.task_3_widget_clicked_grid.addWidget(self.task_3_description_widget, 12, 0)

        def show_permission_error(self):
            QMessageBox.critical(self, Localization.EMAIL_ERROR_HEADER, Localization.EXAM_GET_DESTINATION_ERROR, QMessageBox.Ok)

        def show_unknown_file_getting_error(self):
            QMessageBox.critical(self, Localization.EMAIL_ERROR_HEADER, Localization.EXAM_GET_FILE_ERROR, QMessageBox.Ok)

        def task_get_file_button_clicked(t: int):
            r = {
                3: ".xlsx", 9: ".xlsx", 10: ".docx", 17: ".txt",
                18: ".xlsx", 22: ".xlsx", 24: ".txt", 26: ".txt"
            }
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                self.task_file_path = self.__dict__["task_%d_file_path" % t]
                iddata = self.__dict__["task_%d_data" % t]
                task_id = iddata["id"]
                shutil.copy(self.task_file_path, destination_path + f"/{t}_{task_id}")
                repl = f"{t}_{task_id}" + r[t]
                QMessageBox.information(self, Localization.EMAIL_SUCCESS_HEADER, Localization.EXAM_SUCCESS % (repl), QMessageBox.Ok)
            except PermissionError:
                show_permission_error(self)
            except FileNotFoundError:
                pass
            except Exception as E:
                Logger.add_line_to_log("Error getting file for task %d. More: %s" % (t, E))
                show_unknown_file_getting_error(self)

        self.task_3_show_ans_btn.clicked.connect(task_3_ans_button_clicked)
        self.task_3_show_descr_btn.clicked.connect(task_3_descr_button_clicked)
        self.task_3_get_file_btn.clicked.connect(lambda: task_get_file_button_clicked(3))


        # 4444444444
        self.task_4_widget = QWidget()
        self.task_4_data = Task_Chooser.choose_task(4)
        self.task_4_text = QLabel(self.task_4_data['text'])
        self.task_4_text.setWordWrap(True)
        self.task_4_text.setAlignment(Qt.AlignCenter)
        self.task_4_answer = QLabel(Localization.BASE_ANSWER + self.task_4_data['answer'])
        self.task_4_answer.setWordWrap(True)
        self.task_4_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_4_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_4_description = self.task_4_data['description']
        self.task_4_description_widget = QLabel(self.task_4_description)
        self.task_4_description_widget.setWordWrap(True)
        self.task_4_widget_clicked_grid = QGridLayout()
        
        self.task_4_widget_clicked_grid.addWidget(self.task_4_text, 0, 0)
        self.task_4_widget_clicked_grid.addWidget(self.task_4_show_ans_btn, 1, 0)
        self.task_4_widget_clicked_grid.addWidget(self.task_4_show_descr_btn, 2, 0)
        self.task_4_widget_clicked_grid.setRowStretch(3, 1) 
        self.task_4_widget.setLayout(self.task_4_widget_clicked_grid)

        def task_4_ans_button_clicked():
            self.task_4_show_ans_btn.setParent(None)
            self.task_4_widget_clicked_grid.addWidget(self.task_4_answer, 1, 0)
        def task_4_descr_button_clicked():
            self.task_4_show_descr_btn.setParent(None)
            self.task_4_widget_clicked_grid.addWidget(self.task_4_description_widget, 2, 0)

        self.task_4_show_ans_btn.clicked.connect(task_4_ans_button_clicked)
        self.task_4_show_descr_btn.clicked.connect(task_4_descr_button_clicked)


        # 5555555555
        self.task_5_widget = QWidget()
        self.task_5_data = Task_Chooser.choose_task(5)
        self.task_5_text = QLabel(self.task_5_data['text'])
        self.task_5_text.setWordWrap(True)
        self.task_5_text.setAlignment(Qt.AlignCenter)
        self.task_5_answer = QLabel(Localization.BASE_ANSWER + self.task_5_data['answer'])
        self.task_5_answer.setWordWrap(True)
        self.task_5_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_5_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_5_description = self.task_5_data['description']
        self.task_5_description_widget = QLabel(self.task_5_description)
        self.task_5_description_widget.setWordWrap(True)
        self.task_5_widget_clicked_grid = QGridLayout()
        
        self.task_5_widget_clicked_grid.addWidget(self.task_5_text, 0, 0)
        self.task_5_widget_clicked_grid.addWidget(self.task_5_show_ans_btn, 1, 0)
        self.task_5_widget_clicked_grid.addWidget(self.task_5_show_descr_btn, 2, 0)
        self.task_5_widget_clicked_grid.setRowStretch(4, 1) 
        self.task_5_widget.setLayout(self.task_5_widget_clicked_grid)

        def task_5_ans_button_clicked():
            self.task_5_show_ans_btn.setParent(None)
            self.task_5_widget_clicked_grid.addWidget(self.task_5_answer, 1, 0)
        def task_5_descr_button_clicked():
            self.task_5_show_descr_btn.setParent(None)
            self.task_5_widget_clicked_grid.addWidget(self.task_5_description_widget, 2, 0)

        self.task_5_show_ans_btn.clicked.connect(task_5_ans_button_clicked)
        self.task_5_show_descr_btn.clicked.connect(task_5_descr_button_clicked)


        # 66666666
        self.task_6_widget = QWidget()
        self.task_6_data = Task_Chooser.choose_task(6)
        self.task_6_text = QLabel(self.task_6_data['text'])
        self.task_6_text.setWordWrap(True)
        self.task_6_answer = QLabel(Localization.BASE_ANSWER + self.task_6_data['answer'])
        self.task_6_answer.setWordWrap(True)
        self.task_6_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_6_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_6_description = self.task_6_data['description']
        if self.task_6_data['python'].strip() != 'нет':
            self.task_6_description = self.task_6_description + '\n\n' + self.task_6_data['python']
        self.task_6_description_widget = QLabel(self.task_6_description)
        self.task_6_description_widget.setWordWrap(True)
        self.task_6_widget_clicked_grid = QGridLayout()
        
        self.task_6_widget_clicked_grid.addWidget(self.task_6_text, 0, 0, alignment=Qt.AlignCenter)
        self.task_6_widget_clicked_grid.addWidget(self.task_6_show_ans_btn, 1, 0)
        self.task_6_widget_clicked_grid.addWidget(self.task_6_show_descr_btn, 2, 0)
        self.task_6_widget_clicked_grid.setRowStretch(3, 1) 
        self.task_6_widget.setLayout(self.task_6_widget_clicked_grid)

        def task_6_ans_button_clicked():
            self.task_6_show_ans_btn.setParent(None)
            self.task_6_widget_clicked_grid.addWidget(self.task_6_answer, 1, 0)
        def task_6_descr_button_clicked():
            self.task_6_show_descr_btn.setParent(None)
            self.task_6_widget_clicked_grid.addWidget(self.task_6_description_widget, 2, 0)

        self.task_6_show_ans_btn.clicked.connect(task_6_ans_button_clicked)
        self.task_6_show_descr_btn.clicked.connect(task_6_descr_button_clicked)


        # 7777777777
        self.task_7_widget = QWidget()
        self.task_7_data = Task_Chooser.choose_task(7)
        self.task_7_text = QLabel(self.task_7_data['text'])
        self.task_7_text.setWordWrap(True)
        self.task_7_text.setAlignment(Qt.AlignCenter)
        self.task_7_answer = QLabel(Localization.BASE_ANSWER + self.task_7_data['answer'])
        self.task_7_answer.setWordWrap(True)
        self.task_7_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_7_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_7_description = self.task_7_data['description']
        self.task_7_description_widget = QLabel(self.task_7_description)
        self.task_7_description_widget.setWordWrap(True)
        self.task_7_widget_clicked_grid = QGridLayout()
        
        self.task_7_widget_clicked_grid.addWidget(self.task_7_text, 0, 0)
        self.task_7_widget_clicked_grid.addWidget(self.task_7_show_ans_btn, 1, 0)
        self.task_7_widget_clicked_grid.addWidget(self.task_7_show_descr_btn, 2, 0)
        self.task_7_widget_clicked_grid.setRowStretch(3, 1) 
        self.task_7_widget.setLayout(self.task_7_widget_clicked_grid)

        def task_7_ans_button_clicked():
            self.task_7_show_ans_btn.setParent(None)
            self.task_7_widget_clicked_grid.addWidget(self.task_7_answer, 1, 0)
        def task_7_descr_button_clicked():
            self.task_7_show_descr_btn.setParent(None)
            self.task_7_widget_clicked_grid.addWidget(self.task_7_description_widget, 2, 0)

        self.task_7_show_ans_btn.clicked.connect(task_7_ans_button_clicked)
        self.task_7_show_descr_btn.clicked.connect(task_7_descr_button_clicked)


        # 88888888888888
        self.task_8_widget = QWidget()
        self.task_8_data = Task_Chooser.choose_task(8)
        self.task_8_text = QLabel(self.task_8_data['text'])
        self.task_8_text.setWordWrap(True)
        self.task_8_text.setAlignment(Qt.AlignCenter)
        self.task_8_answer = QLabel(Localization.BASE_ANSWER + self.task_8_data['answer'])
        self.task_8_answer.setWordWrap(True)
        self.task_8_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_8_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_8_description = self.task_8_data['description']
        if self.task_8_data['python'].strip() != 'нет':
            self.task_8_description = self.task_8_description + '\n\n' + self.task_8_data['python']
        self.task_8_description_widget = QLabel(self.task_8_description)
        self.task_8_description_widget.setWordWrap(True)
        self.task_8_widget_clicked_grid = QGridLayout()
        
        self.task_8_widget_clicked_grid.addWidget(self.task_8_text, 0, 0)
        self.task_8_widget_clicked_grid.addWidget(self.task_8_show_ans_btn, 1, 0)
        self.task_8_widget_clicked_grid.addWidget(self.task_8_show_descr_btn, 2, 0)
        self.task_8_widget_clicked_grid.setRowStretch(3, 1) 
        self.task_8_widget.setLayout(self.task_8_widget_clicked_grid)

        def task_8_ans_button_clicked():
            self.task_8_show_ans_btn.setParent(None)
            self.task_8_widget_clicked_grid.addWidget(self.task_8_answer, 1, 0)
        def task_8_descr_button_clicked():
            self.task_8_show_descr_btn.setParent(None)
            self.task_8_widget_clicked_grid.addWidget(self.task_8_description_widget, 2, 0)

        self.task_8_show_ans_btn.clicked.connect(task_8_ans_button_clicked)
        self.task_8_show_descr_btn.clicked.connect(task_8_descr_button_clicked)


        # 9999999999
        self.task_9_widget = QWidget()
        self.task_9_data = Task_Chooser.choose_task(9)
        self.task_9_text = QLabel(self.task_9_data['text'])
        self.task_9_text.setWordWrap(True)
        self.task_9_text.setAlignment(Qt.AlignCenter)
        self.task_9_answer = QLabel(Localization.BASE_ANSWER + self.task_9_data['answer'])
        self.task_9_answer.setWordWrap(True)
        self.task_9_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_9_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_9_description = self.task_9_data['description']
        self.task_9_description_widget = QLabel(self.task_9_description)
        self.task_9_description_widget.setWordWrap(True)
        self.task_9_widget_clicked_grid = QGridLayout()

        self.task_9_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_9_file_path = 'data/tasks_data/9/' + self.task_9_data['id'] + '.xlsx'
        
        self.task_9_widget_clicked_grid.addWidget(self.task_9_text, 0, 0)
        self.task_9_widget_clicked_grid.addWidget(self.task_9_get_file_btn, 1, 0)
        self.task_9_widget_clicked_grid.addWidget(self.task_9_show_ans_btn, 2, 0)
        self.task_9_widget_clicked_grid.addWidget(self.task_9_show_descr_btn, 3, 0)
        self.task_9_widget_clicked_grid.setRowStretch(4, 1) 
        self.task_9_widget.setLayout(self.task_9_widget_clicked_grid)

        def task_9_ans_button_clicked():
            self.task_9_show_ans_btn.setParent(None)
            self.task_9_widget_clicked_grid.addWidget(self.task_9_answer, 2, 0)
        def task_9_descr_button_clicked():
            self.task_9_show_descr_btn.setParent(None)
            self.task_9_widget_clicked_grid.addWidget(self.task_9_description_widget, 3, 0)

        self.task_9_show_ans_btn.clicked.connect(task_9_ans_button_clicked)
        self.task_9_show_descr_btn.clicked.connect(task_9_descr_button_clicked)
        self.task_9_get_file_btn.clicked.connect(lambda: task_get_file_button_clicked(9))


        # 10101010101010101010
        self.task_10_widget = QWidget()
        self.task_10_data = Task_Chooser.choose_task(10)
        self.task_10_text = QLabel(self.task_10_data['text'])
        self.task_10_text.setWordWrap(True)
        self.task_10_text.setAlignment(Qt.AlignCenter)
        self.task_10_answer = QLabel(Localization.BASE_ANSWER + self.task_10_data['answer'])
        self.task_10_answer.setWordWrap(True)
        self.task_10_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_10_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_10_description = self.task_10_data['description']
        self.task_10_description_widget = QLabel(self.task_10_description)
        self.task_10_description_widget.setWordWrap(True)
        self.task_10_widget_clicked_grid = QGridLayout()

        self.task_10_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_10_file_path = 'data/tasks_data/10/' + self.task_10_data['id'] + '.docx'
        
        self.task_10_widget_clicked_grid.addWidget(self.task_10_text, 0, 0)
        self.task_10_widget_clicked_grid.addWidget(self.task_10_get_file_btn, 1, 0)
        self.task_10_widget_clicked_grid.addWidget(self.task_10_show_ans_btn, 2, 0)
        self.task_10_widget_clicked_grid.addWidget(self.task_10_show_descr_btn, 3, 0)
        self.task_10_widget_clicked_grid.setRowStretch(4, 1) 
        self.task_10_widget.setLayout(self.task_10_widget_clicked_grid)

        def task_10_ans_button_clicked():
            self.task_10_show_ans_btn.setParent(None)
            self.task_10_widget_clicked_grid.addWidget(self.task_10_answer, 2, 0)
        def task_10_descr_button_clicked():
            self.task_10_show_descr_btn.setParent(None)
            self.task_10_widget_clicked_grid.addWidget(self.task_10_description_widget, 3, 0)

        self.task_10_show_ans_btn.clicked.connect(task_10_ans_button_clicked)
        self.task_10_show_descr_btn.clicked.connect(task_10_descr_button_clicked)
        self.task_10_get_file_btn.clicked.connect(lambda: task_get_file_button_clicked(10))


        # 11111111111111111111
        self.task_11_widget = QWidget()
        self.task_11_data = Task_Chooser.choose_task(11)
        self.task_11_text = QLabel(self.task_11_data['text'])
        self.task_11_text.setWordWrap(True)
        self.task_11_text.setAlignment(Qt.AlignCenter)
        self.task_11_answer = QLabel(Localization.BASE_ANSWER + self.task_11_data['answer'])
        self.task_11_answer.setWordWrap(True)
        self.task_11_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_11_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_11_description = self.task_11_data['description']
        self.task_11_description_widget = QLabel(self.task_11_description)
        self.task_11_description_widget.setWordWrap(True)
        self.task_11_widget_clicked_grid = QGridLayout()
        
        self.task_11_widget_clicked_grid.addWidget(self.task_11_text, 0, 0)
        self.task_11_widget_clicked_grid.addWidget(self.task_11_show_ans_btn, 1, 0)
        self.task_11_widget_clicked_grid.addWidget(self.task_11_show_descr_btn, 2, 0)
        self.task_11_widget_clicked_grid.setRowStretch(3, 1) 
        self.task_11_widget.setLayout(self.task_11_widget_clicked_grid)

        def task_11_ans_button_clicked():
            self.task_11_show_ans_btn.setParent(None)
            self.task_11_widget_clicked_grid.addWidget(self.task_11_answer, 1, 0)
        def task_11_descr_button_clicked():
            self.task_11_show_descr_btn.setParent(None)
            self.task_11_widget_clicked_grid.addWidget(self.task_11_description_widget, 2, 0)

        self.task_11_show_ans_btn.clicked.connect(task_11_ans_button_clicked)
        self.task_11_show_descr_btn.clicked.connect(task_11_descr_button_clicked)


        # 12121212121212121212
        self.task_12_widget = QWidget()
        self.task_12_data = Task_Chooser.choose_task(12)
        self.task_12_text = QLabel(self.task_12_data['text'])
        self.task_12_text.setWordWrap(True)
        self.task_12_answer = QLabel(Localization.BASE_ANSWER + self.task_12_data['answer'])
        self.task_12_answer.setWordWrap(True)
        self.task_12_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_12_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_12_description = self.task_12_data['description']
        if self.task_12_data['python'].strip() != 'нет':
            self.task_12_description = self.task_12_description + '\n\n' + self.task_12_data['python']
        self.task_12_description_widget = QLabel(self.task_12_description)
        self.task_12_description_widget.setWordWrap(True)
        self.task_12_widget_clicked_grid = QGridLayout()

        def task_12_ans_button_clicked():
            self.task_12_show_ans_btn.setParent(None)
            self.task_12_widget_clicked_grid.addWidget(self.task_12_answer, 1, 0)
        def task_12_descr_button_clicked():
            self.task_12_show_descr_btn.setParent(None)
            self.task_12_widget_clicked_grid.addWidget(self.task_12_description_widget, 2, 0)

        if self.task_12_data['hasPictures'] == False:
            self.task_12_widget_clicked_grid.addWidget(self.task_12_text, 0, 0)
            self.task_12_widget_clicked_grid.addWidget(self.task_12_show_ans_btn, 1, 0)
            self.task_12_widget_clicked_grid.addWidget(self.task_12_show_descr_btn, 2, 0)
            self.task_12_widget_clicked_grid.setRowStretch(3, 1) 
            self.task_12_widget.setLayout(self.task_12_widget_clicked_grid)
            self.task_12_show_ans_btn.clicked.connect(task_12_ans_button_clicked)
            self.task_12_show_descr_btn.clicked.connect(task_12_descr_button_clicked)


        # 13131313131313131313
        self.task_13_widget = QWidget()
        self.task_13_data = Task_Chooser.choose_task(13)
        self.task_13_text = QLabel(self.task_13_data['text'])
        self.task_13_text.setWordWrap(True)
        self.task_13_text.setAlignment(Qt.AlignCenter)
        self.task_13_answer = QLabel(Localization.BASE_ANSWER + self.task_13_data['answer'])
        self.task_13_answer.setWordWrap(True)
        self.task_13_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_13_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_13_description = self.task_13_data['description']
        self.task_13_description_widget = QLabel(self.task_13_description)
        self.task_13_description_widget.setWordWrap(True)
        self.task_13_widget_clicked_grid = QGridLayout()

        self.task_13_text_widgth = self.task_13_text.frameGeometry().width()
        self.task_13_text_height = self.task_13_text.frameGeometry().height()

        self.task_13_picture_path = 'data/tasks_data/13/' + self.task_13_data['id'] + '.png'
        self.task_13_picture_exists = True if os.path.exists(self.task_13_picture_path) else False
        if self.task_13_picture_exists:
            self.task_13_picture = QPixmap(self.task_13_picture_path)
            self.task_13_picture = self.task_13_picture.scaled(self.task_13_text_widgth, self.task_13_text_height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.task_13_picture_lbl = QLabel(self)
            self.task_13_picture_lbl.setPixmap(self.task_13_picture)
        
        self.task_13_widget_clicked_grid.addWidget(self.task_13_text, 0, 0)
        self.t13k = 0
        if self.task_13_picture_exists:
            self.t13k = 1
            self.task_13_widget_clicked_grid.addWidget(self.task_13_picture_lbl, 1, 0, alignment=Qt.AlignCenter)
        self.task_13_widget_clicked_grid.addWidget(self.task_13_show_ans_btn, 1 + self.t13k, 0)
        self.task_13_widget_clicked_grid.addWidget(self.task_13_show_descr_btn, 2 + self.t13k, 0)
        self.task_13_widget_clicked_grid.setRowStretch(4, 1) 
        self.task_13_widget.setLayout(self.task_13_widget_clicked_grid)

        def task_13_ans_button_clicked():
            self.task_13_show_ans_btn.setParent(None)
            self.task_13_widget_clicked_grid.addWidget(self.task_13_answer, 1 + self.t13k, 0)
        def task_13_descr_button_clicked():
            self.task_13_show_descr_btn.setParent(None)
            self.task_13_widget_clicked_grid.addWidget(self.task_13_description_widget, 2 + self.t13k, 0)

        self.task_13_show_ans_btn.clicked.connect(task_13_ans_button_clicked)
        self.task_13_show_descr_btn.clicked.connect(task_13_descr_button_clicked)


        # 1414141414141414141414141414
        self.task_14_widget = QWidget()
        self.task_14_data = Task_Chooser.choose_task(14)
        self.task_14_text = QLabel(self.task_14_data['text'])
        self.task_14_text.setWordWrap(True)
        self.task_14_text.setAlignment(Qt.AlignCenter)
        self.task_14_answer = QLabel(Localization.BASE_ANSWER + self.task_14_data['answer'])
        self.task_14_answer.setWordWrap(True)
        self.task_14_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_14_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_14_description = self.task_14_data['description']
        if self.task_14_data['python'].strip() != 'нет':
            self.task_14_description = self.task_14_description + '\n\n' + self.task_14_data['python']
        self.task_14_description_widget = QLabel(self.task_14_description)
        self.task_14_description_widget.setWordWrap(True)
        self.task_14_widget_clicked_grid = QGridLayout()
        
        self.task_14_widget_clicked_grid.addWidget(self.task_14_text, 0, 0)
        self.task_14_widget_clicked_grid.addWidget(self.task_14_show_ans_btn, 1, 0)
        self.task_14_widget_clicked_grid.addWidget(self.task_14_show_descr_btn, 2, 0)
        self.task_14_widget_clicked_grid.setRowStretch(3, 1) 
        self.task_14_widget.setLayout(self.task_14_widget_clicked_grid)

        def task_14_ans_button_clicked():
            self.task_14_show_ans_btn.setParent(None)
            self.task_14_widget_clicked_grid.addWidget(self.task_14_answer, 1, 0)
        def task_14_descr_button_clicked():
            self.task_14_show_descr_btn.setParent(None)
            self.task_14_widget_clicked_grid.addWidget(self.task_14_description_widget, 2, 0)

        self.task_14_show_ans_btn.clicked.connect(task_14_ans_button_clicked)
        self.task_14_show_descr_btn.clicked.connect(task_14_descr_button_clicked)


        # 1515151515151515151515151515
        self.task_15_widget = QWidget()
        self.task_15_data = Task_Chooser.choose_task(15)
        self.task_15_text = QLabel(self.task_15_data['text'])
        self.task_15_text.setWordWrap(True)
        self.task_15_text.setAlignment(Qt.AlignCenter)
        self.task_15_answer = QLabel(Localization.BASE_ANSWER + self.task_15_data['answer'])
        self.task_15_answer.setWordWrap(True)
        self.task_15_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_15_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_15_description = self.task_15_data['description']
        if self.task_15_data['python'].strip() != 'нет':
            self.task_15_description = self.task_15_description + '\n\n' + self.task_15_data['python']
        self.task_15_description_widget = QLabel(self.task_15_description)
        self.task_15_description_widget.setWordWrap(True)
        self.task_15_widget_clicked_grid = QGridLayout()
        
        self.task_15_widget_clicked_grid.addWidget(self.task_15_text, 0, 0)
        self.task_15_widget_clicked_grid.addWidget(self.task_15_show_ans_btn, 1, 0)
        self.task_15_widget_clicked_grid.addWidget(self.task_15_show_descr_btn, 2, 0)
        self.task_15_widget_clicked_grid.setRowStretch(3, 1) 
        self.task_15_widget.setLayout(self.task_15_widget_clicked_grid)

        def task_15_ans_button_clicked():
            self.task_15_show_ans_btn.setParent(None)
            self.task_15_widget_clicked_grid.addWidget(self.task_15_answer, 1, 0)
        def task_15_descr_button_clicked():
            self.task_15_show_descr_btn.setParent(None)
            self.task_15_widget_clicked_grid.addWidget(self.task_15_description_widget, 2, 0)

        self.task_15_show_ans_btn.clicked.connect(task_15_ans_button_clicked)
        self.task_15_show_descr_btn.clicked.connect(task_15_descr_button_clicked)


        # 1616161616161616
        self.task_16_widget = QWidget()
        self.task_16_data = Task_Chooser.choose_task(16)
        self.task_16_text_for_lbl = self.task_16_data['text']
        self.task_16_text = QLabel(self.task_16_text_for_lbl)
        self.task_16_text.setWordWrap(True)
        self.task_16_answer = QLabel(Localization.BASE_ANSWER + self.task_16_data['answer'])
        self.task_16_answer.setWordWrap(True)
        self.task_16_description = ""
        if self.task_16_data['description'].strip() != 'нет':
            self.task_16_description += self.task_16_data['description'] + "\n"
        if self.task_16_data['python'].strip() != 'нет':
            self.task_16_description += self.task_16_data['python']
        self.task_16_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_16_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_16_description_widget = QLabel(self.task_16_description)
        self.task_16_description_widget.setWordWrap(True)
        self.task_16_widget_clicked_grid = QGridLayout()
        
        self.task_16_widget_clicked_grid.addWidget(self.task_16_text, 0, 0, alignment=Qt.AlignCenter)
        self.task_16_widget_clicked_grid.addWidget(self.task_16_show_ans_btn, 1, 0)
        self.task_16_widget_clicked_grid.addWidget(self.task_16_show_descr_btn, 2, 0)
        self.task_16_widget_clicked_grid.setRowStretch(3, 1) 
        self.task_16_widget.setLayout(self.task_16_widget_clicked_grid)

        def task_16_ans_button_clicked():
            self.task_16_show_ans_btn.setParent(None)
            self.task_16_widget_clicked_grid.addWidget(self.task_16_answer, 1, 0)
        def task_16_descr_button_clicked():
            self.task_16_show_descr_btn.setParent(None)
            self.task_16_widget_clicked_grid.addWidget(self.task_16_description_widget, 2, 0)

        self.task_16_show_ans_btn.clicked.connect(task_16_ans_button_clicked)
        self.task_16_show_descr_btn.clicked.connect(task_16_descr_button_clicked)


        # 1717171717171717171717171717
        self.task_17_widget = QWidget()
        self.task_17_data = Task_Chooser.choose_task(17)
        self.task_17_text = QLabel(self.task_17_data['text'].replace("17.txt", ""))
        self.task_17_text.setWordWrap(True)
        self.task_17_text.setAlignment(Qt.AlignCenter)
        self.task_17_answer = QLabel(Localization.BASE_ANSWER + self.task_17_data['answer'])
        self.task_17_answer.setWordWrap(True)
        self.task_17_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_17_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_17_description = self.task_17_data['description']
        if self.task_17_data['python'].strip() != 'нет':
            self.task_17_description = self.task_17_description + '\n\n' + self.task_17_data['python']
        self.task_17_description_widget = QLabel(self.task_17_description)
        self.task_17_description_widget.setWordWrap(True)
        self.task_17_widget_clicked_grid = QGridLayout()

        self.task_17_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_17_file_path = 'data/tasks_data/17/' + self.task_17_data['fileName']
        
        self.task_17_widget_clicked_grid.addWidget(self.task_17_text, 0, 0)
        self.task_17_widget_clicked_grid.addWidget(self.task_17_get_file_btn, 1, 0)
        self.task_17_widget_clicked_grid.addWidget(self.task_17_show_ans_btn, 2, 0)
        self.task_17_widget_clicked_grid.addWidget(self.task_17_show_descr_btn, 3, 0)
        self.task_17_widget_clicked_grid.setRowStretch(4, 1) 
        self.task_17_widget.setLayout(self.task_17_widget_clicked_grid)

        def task_17_ans_button_clicked():
            self.task_17_show_ans_btn.setParent(None)
            self.task_17_widget_clicked_grid.addWidget(self.task_17_answer, 2, 0)
        def task_17_descr_button_clicked():
            self.task_17_show_descr_btn.setParent(None)
            self.task_17_widget_clicked_grid.addWidget(self.task_17_description_widget, 3, 0)

        self.task_17_show_ans_btn.clicked.connect(task_17_ans_button_clicked)
        self.task_17_show_descr_btn.clicked.connect(task_17_descr_button_clicked)

        self.task_17_get_file_btn.clicked.connect(lambda: task_get_file_button_clicked(17))


        # 1818181818181818181818181818
        self.task_18_widget = QWidget()
        self.task_18_data = Task_Chooser.choose_task(18)
        self.task_18_text = QLabel(self.task_18_data['text'].replace("18.xlsx", ""))
        self.task_18_text.setWordWrap(True)
        self.task_18_text.setAlignment(Qt.AlignCenter)
        self.task_18_answer = QLabel(Localization.BASE_ANSWER + self.task_18_data['answer'])
        self.task_18_answer.setWordWrap(True)
        self.task_18_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_18_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_18_description = self.task_18_data['description']
        self.task_18_description_widget = QLabel(self.task_18_description)
        self.task_18_description_widget.setWordWrap(True)
        self.task_18_widget_clicked_grid = QGridLayout()

        self.task_18_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_18_file_path = 'data/tasks_data/18/' + self.task_18_data['id'] + '.xlsx'
        
        self.task_18_widget_clicked_grid.addWidget(self.task_18_text, 0, 0)
        self.task_18_widget_clicked_grid.addWidget(self.task_18_get_file_btn, 1, 0)
        self.task_18_widget_clicked_grid.addWidget(self.task_18_show_ans_btn, 2, 0)
        self.task_18_widget_clicked_grid.addWidget(self.task_18_show_descr_btn, 3, 0)
        self.task_18_widget_clicked_grid.setRowStretch(4, 1) 
        self.task_18_widget.setLayout(self.task_18_widget_clicked_grid)

        def task_18_ans_button_clicked():
            self.task_18_show_ans_btn.setParent(None)
            self.task_18_widget_clicked_grid.addWidget(self.task_18_answer, 2, 0)
        def task_18_descr_button_clicked():
            self.task_18_show_descr_btn.setParent(None)
            self.task_18_widget_clicked_grid.addWidget(self.task_18_description_widget, 3, 0)

        self.task_18_show_ans_btn.clicked.connect(task_18_ans_button_clicked)
        self.task_18_show_descr_btn.clicked.connect(task_18_descr_button_clicked)

        self.task_18_get_file_btn.clicked.connect(lambda: task_get_file_button_clicked(18))


        # 192021192021192021
        self.tasks19_21tab_widget = QTabWidget()
        self.task_19_21_data = Task_Chooser.choose_task("19-21")

        self.tasks19_21_text = QWidget()
        self.tasks19_21text_layout = QGridLayout()
        self.task_19_header = QLabel(self.task_19_21_data['text'])
        self.task_19_header.setWordWrap(True)
        self.task_19_header.setAlignment(Qt.AlignCenter)
        self.tasks19_21text_layout.addWidget(self.task_19_header)
        self.tasks19_21_text.setLayout(self.tasks19_21text_layout)

        self.task_19_widget = QWidget()
        self.task_19_text = QLabel(self.task_19_21_data['19_text'])
        self.task_19_text.setWordWrap(True)
        self.task_19_text.setAlignment(Qt.AlignCenter)
        self.task_19_answer = QLabel(Localization.BASE_ANSWER + self.task_19_21_data['19_answer'])
        self.task_19_answer.setWordWrap(True)
        self.task_19_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_19_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_19_description = self.task_19_21_data['19_description']
        if self.task_19_21_data['19_python'].strip() != 'нет':
            self.task_19_description = self.task_19_description + '\n\n' + self.task_19_21_data['19_python']
        self.task_19_description_widget = QLabel(self.task_19_description)
        self.task_19_description_widget.setWordWrap(True)
        self.task_19_widget_clicked_grid = QGridLayout()
        
        self.task_19_widget_clicked_grid.addWidget(self.task_19_text, 0, 0)
        self.task_19_widget_clicked_grid.addWidget(self.task_19_show_ans_btn, 1, 0)
        self.task_19_widget_clicked_grid.addWidget(self.task_19_show_descr_btn, 2, 0)
        self.task_19_widget_clicked_grid.setRowStretch(3, 1) 
        self.task_19_widget.setLayout(self.task_19_widget_clicked_grid)

        self.task_19_scroll_area = QScrollArea()
        self.task_19_scroll_area.setWidgetResizable(True)
        self.task_19_scroll_area.setWidget(self.task_19_widget)

        def task_19_ans_button_clicked():
            self.task_19_show_ans_btn.setParent(None)
            self.task_19_widget_clicked_grid.addWidget(self.task_19_answer, 1, 0)
        def task_19_descr_button_clicked():
            self.task_19_show_descr_btn.setParent(None)
            self.task_19_widget_clicked_grid.addWidget(self.task_19_description_widget, 2, 0)

        self.task_19_show_ans_btn.clicked.connect(task_19_ans_button_clicked)
        self.task_19_show_descr_btn.clicked.connect(task_19_descr_button_clicked)


        self.task_20_widget = QWidget()
        self.task_20_text = QLabel(self.task_19_21_data['20_text'])
        self.task_20_text.setWordWrap(True)
        self.task_20_text.setAlignment(Qt.AlignCenter)
        self.task_20_answer = QLabel(Localization.BASE_ANSWER + self.task_19_21_data['20_answer'])
        self.task_20_answer.setWordWrap(True)
        self.task_20_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_20_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_20_description = self.task_19_21_data['20_description']
        if self.task_19_21_data['20_python'].strip() != 'нет':
            self.task_20_description = self.task_20_description + '\n\n' + self.task_19_21_data['20_python']
        self.task_20_description_widget = QLabel(self.task_20_description)
        self.task_20_description_widget.setWordWrap(True)
        self.task_20_widget_clicked_grid = QGridLayout()
        
        self.task_20_widget_clicked_grid.addWidget(self.task_20_text, 0, 0)
        self.task_20_widget_clicked_grid.addWidget(self.task_20_show_ans_btn, 1, 0)
        self.task_20_widget_clicked_grid.addWidget(self.task_20_show_descr_btn, 2, 0)
        self.task_20_widget_clicked_grid.setRowStretch(3, 1) 
        self.task_20_widget.setLayout(self.task_20_widget_clicked_grid)

        self.task_20_scroll_area = QScrollArea()
        self.task_20_scroll_area.setWidgetResizable(True)
        self.task_20_scroll_area.setWidget(self.task_20_widget)

        def task_20_ans_button_clicked():
            self.task_20_show_ans_btn.setParent(None)
            self.task_20_widget_clicked_grid.addWidget(self.task_20_answer, 1, 0)
        def task_20_descr_button_clicked():
            self.task_20_show_descr_btn.setParent(None)
            self.task_20_widget_clicked_grid.addWidget(self.task_20_description_widget, 2, 0)

        self.task_20_show_ans_btn.clicked.connect(task_20_ans_button_clicked)
        self.task_20_show_descr_btn.clicked.connect(task_20_descr_button_clicked)


        self.task_21_widget = QWidget()
        self.task_21_text = QLabel(self.task_19_21_data['21_text'])
        self.task_21_text.setWordWrap(True)
        self.task_21_text.setAlignment(Qt.AlignCenter)
        self.task_21_answer = QLabel(Localization.BASE_ANSWER + self.task_19_21_data['21_answer'])
        self.task_21_answer.setWordWrap(True)
        self.task_21_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_21_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_21_description = self.task_19_21_data['21_description']
        if self.task_19_21_data['21_python'].strip() != 'нет':
            self.task_21_description = self.task_21_description + '\n\n' + self.task_19_21_data['21_python']
        self.task_21_description_widget = QLabel(self.task_21_description)
        self.task_21_description_widget.setWordWrap(True)
        self.task_21_widget_clicked_grid = QGridLayout()
        
        self.task_21_widget_clicked_grid.addWidget(self.task_21_text, 0, 0)
        self.task_21_widget_clicked_grid.addWidget(self.task_21_show_ans_btn, 1, 0)
        self.task_21_widget_clicked_grid.addWidget(self.task_21_show_descr_btn, 2, 0)
        self.task_21_widget_clicked_grid.setRowStretch(3, 1) 
        self.task_21_widget.setLayout(self.task_21_widget_clicked_grid)

        self.task_21_scroll_area = QScrollArea()
        self.task_21_scroll_area.setWidgetResizable(True)
        self.task_21_scroll_area.setWidget(self.task_21_widget)

        def task_21_ans_button_clicked():
            self.task_21_show_ans_btn.setParent(None)
            self.task_21_widget_clicked_grid.addWidget(self.task_21_answer, 1, 0)
        def task_21_descr_button_clicked():
            self.task_21_show_descr_btn.setParent(None)
            self.task_21_widget_clicked_grid.addWidget(self.task_21_description_widget, 2, 0)

        self.task_21_show_ans_btn.clicked.connect(task_21_ans_button_clicked)
        self.task_21_show_descr_btn.clicked.connect(task_21_descr_button_clicked)

        self.tasks19_21tab_widget.addTab(self.tasks19_21_text, Localization.T19_21_TEXT_TAB)
        self.tasks19_21tab_widget.addTab(self.task_19_scroll_area, Localization.T19_21_TAB_1)
        self.tasks19_21tab_widget.addTab(self.task_20_scroll_area, Localization.T19_21_TAB_2)
        self.tasks19_21tab_widget.addTab(self.task_21_scroll_area, Localization.T19_21_TAB_3)


        # 2222222222222222
        self.task_22_widget = QWidget()
        self.task_22_data = Task_Chooser.choose_task(22)
        self.task_22_text = QLabel(self.task_22_data['text'] + "\n" + Config.readTask22Example())
        self.task_22_text.setWordWrap(True)
        self.task_22_answer = QLabel(Localization.BASE_ANSWER + self.task_22_data['answer'])
        self.task_22_answer.setWordWrap(True)
        self.task_22_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_22_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_22_description = self.task_22_data['description']
        if self.task_22_data['python'].strip() != 'нет':
            self.task_22_description = self.task_22_description + '\n\n' + self.task_22_data['python']
        self.task_22_description_widget = QLabel(self.task_22_description)
        self.task_22_description_widget.setWordWrap(True)
        self.task_22_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_22_file_path = 'data/tasks_data/22/' + self.task_22_data['id'] + '.xlsx'
        self.task_22_widget_clicked_grid = QGridLayout()
        
        self.task_22_widget_clicked_grid.addWidget(self.task_22_text, 0, 0, alignment=Qt.AlignCenter)
        self.task_22_widget_clicked_grid.addWidget(self.task_22_get_file_btn, 1, 0)
        self.task_22_widget_clicked_grid.addWidget(self.task_22_show_ans_btn, 2, 0)
        self.task_22_widget_clicked_grid.addWidget(self.task_22_show_descr_btn, 3, 0)
        self.task_22_widget_clicked_grid.setRowStretch(4, 1)
        self.task_22_widget.setLayout(self.task_22_widget_clicked_grid)

        def task_22_ans_button_clicked():
            self.task_22_show_ans_btn.setParent(None)
            self.task_22_widget_clicked_grid.addWidget(self.task_22_answer, 2, 0)
        def task_22_descr_button_clicked():
            self.task_22_show_descr_btn.setParent(None)
            self.task_22_widget_clicked_grid.addWidget(self.task_22_description_widget, 3, 0)

        self.task_22_show_ans_btn.clicked.connect(task_22_ans_button_clicked)
        self.task_22_show_descr_btn.clicked.connect(task_22_descr_button_clicked)

        self.task_22_get_file_btn.clicked.connect(lambda: task_get_file_button_clicked(22))


        # 23232323232323232323
        self.task_23_widget = QWidget()
        self.task_23_data = Task_Chooser.choose_task(23)
        self.task_23_text = QLabel(self.task_23_data['text'])
        self.task_23_text.setWordWrap(True)
        self.task_23_text.setAlignment(Qt.AlignCenter)
        self.task_23_answer = QLabel(Localization.BASE_ANSWER + self.task_23_data['answer'])
        self.task_23_answer.setWordWrap(True)
        self.task_23_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_23_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_23_description = self.task_23_data['description']
        if self.task_23_data['python'].strip() != 'нет':
            self.task_23_description = self.task_23_description + '\n\n' + self.task_23_data['python']
        self.task_23_description_widget = QLabel(self.task_23_description)
        self.task_23_description_widget.setWordWrap(True)
        self.task_23_widget_clicked_grid = QGridLayout()
        
        self.task_23_widget_clicked_grid.addWidget(self.task_23_text, 0, 0)
        self.task_23_widget_clicked_grid.addWidget(self.task_23_show_ans_btn, 1, 0)
        self.task_23_widget_clicked_grid.addWidget(self.task_23_show_descr_btn, 2, 0)
        self.task_23_widget_clicked_grid.setRowStretch(3, 1) 
        self.task_23_widget.setLayout(self.task_23_widget_clicked_grid)

        def task_23_ans_button_clicked():
            self.task_23_show_ans_btn.setParent(None)
            self.task_23_widget_clicked_grid.addWidget(self.task_23_answer, 1, 0)
        def task_23_descr_button_clicked():
            self.task_23_show_descr_btn.setParent(None)
            self.task_23_widget_clicked_grid.addWidget(self.task_23_description_widget, 2, 0)

        self.task_23_show_ans_btn.clicked.connect(task_23_ans_button_clicked)
        self.task_23_show_descr_btn.clicked.connect(task_23_descr_button_clicked)


        # 2424242424242424242424242424
        self.task_24_widget = QWidget()
        self.task_24_data = Task_Chooser.choose_task(24)
        self.task_24_text = QLabel(self.task_24_data['text'])
        self.task_24_text.setWordWrap(True)
        self.task_24_text.setAlignment(Qt.AlignCenter)
        self.task_24_answer = QLabel(Localization.BASE_ANSWER + self.task_24_data['answer'])
        self.task_24_answer.setWordWrap(True)
        self.task_24_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_24_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_24_description = self.task_24_data['description']
        if self.task_24_data['python'].strip() != 'нет':
            self.task_24_description = self.task_24_description + '\n\n' + self.task_24_data['python']
        self.task_24_description_widget = QLabel(self.task_24_description)
        self.task_24_description_widget.setWordWrap(True)
        self.task_24_widget_clicked_grid = QGridLayout()

        self.task_24_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_24_file_path = 'data/tasks_data/24/' + self.task_24_data['id'] + '.txt'
        
        self.task_24_widget_clicked_grid.addWidget(self.task_24_text, 0, 0)
        self.task_24_widget_clicked_grid.addWidget(self.task_24_get_file_btn, 1, 0)
        self.task_24_widget_clicked_grid.addWidget(self.task_24_show_ans_btn, 2, 0)
        self.task_24_widget_clicked_grid.addWidget(self.task_24_show_descr_btn, 3, 0)
        self.task_24_widget_clicked_grid.setRowStretch(4, 1) 
        self.task_24_widget.setLayout(self.task_24_widget_clicked_grid)

        def task_24_ans_button_clicked():
            self.task_24_show_ans_btn.setParent(None)
            self.task_24_widget_clicked_grid.addWidget(self.task_24_answer, 2, 0)
        def task_24_descr_button_clicked():
            self.task_24_show_descr_btn.setParent(None)
            self.task_24_widget_clicked_grid.addWidget(self.task_24_description_widget, 3, 0)

        self.task_24_show_ans_btn.clicked.connect(task_24_ans_button_clicked)
        self.task_24_show_descr_btn.clicked.connect(task_24_descr_button_clicked)

        self.task_24_get_file_btn.clicked.connect(lambda: task_get_file_button_clicked(24))


        # 2525252525252525252525252525
        self.task_25_widget = QWidget()
        self.task_25_data = Task_Chooser.choose_task(25)
        self.task_25_text = QLabel(self.task_25_data['text'])
        self.task_25_text.setWordWrap(True)
        self.task_25_text.setAlignment(Qt.AlignCenter)
        self.task_25_answer = QLabel('Ответ:\n' + self.task_25_data['answer'])
        self.task_25_answer.setWordWrap(True)
        self.task_25_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_25_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_25_description = self.task_25_data['description']
        if self.task_25_data['python'].strip() != 'нет':
            self.task_25_description = self.task_25_description + '\n\n' + self.task_25_data['python']
        self.task_25_description_widget = QLabel(self.task_25_description)
        self.task_25_description_widget.setWordWrap(True)
        self.task_25_widget_clicked_grid = QGridLayout()
        
        self.task_25_widget_clicked_grid.addWidget(self.task_25_text, 0, 0)
        self.task_25_widget_clicked_grid.addWidget(self.task_25_show_ans_btn, 1, 0)
        self.task_25_widget_clicked_grid.addWidget(self.task_25_show_descr_btn, 2, 0)
        self.task_25_widget_clicked_grid.setRowStretch(3, 1) 
        self.task_25_widget.setLayout(self.task_25_widget_clicked_grid)

        def task_25_ans_button_clicked():
            self.task_25_show_ans_btn.setParent(None)
            self.task_25_widget_clicked_grid.addWidget(self.task_25_answer, 1, 0)
        def task_25_descr_button_clicked():
            self.task_25_show_descr_btn.setParent(None)
            self.task_25_widget_clicked_grid.addWidget(self.task_25_description_widget, 2, 0)

        self.task_25_show_ans_btn.clicked.connect(task_25_ans_button_clicked)
        self.task_25_show_descr_btn.clicked.connect(task_25_descr_button_clicked)


        # 2626262626262626262626262626
        self.task_26_widget = QWidget()
        self.task_26_data = Task_Chooser.choose_task(26)
        self.task_26_text = QLabel(self.task_26_data['text'])
        self.task_26_text.setWordWrap(True)
        self.task_26_text.setAlignment(Qt.AlignCenter)
        self.task_26_answer = QLabel(Localization.BASE_ANSWER + self.task_26_data['answer'])
        self.task_26_answer.setWordWrap(True)
        self.task_26_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_26_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_26_description = self.task_26_data['description']
        if self.task_26_data['python'].strip() != 'нет':
            self.task_26_description = self.task_26_description + '\n\n' + self.task_26_data['python']
        self.task_26_description_widget = QLabel(self.task_26_description)
        self.task_26_description_widget.setWordWrap(True)
        self.task_26_widget_clicked_grid = QGridLayout()

        self.task_26_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_26_file_path = 'data/tasks_data/26/' + self.task_26_data['id'] + '.txt'
        
        self.task_26_widget_clicked_grid.addWidget(self.task_26_text, 0, 0)
        self.task_26_widget_clicked_grid.addWidget(self.task_26_get_file_btn, 1, 0)
        self.task_26_widget_clicked_grid.addWidget(self.task_26_show_ans_btn, 2, 0)
        self.task_26_widget_clicked_grid.addWidget(self.task_26_show_descr_btn, 3, 0)
        self.task_26_widget_clicked_grid.setRowStretch(4, 1) 
        self.task_26_widget.setLayout(self.task_26_widget_clicked_grid)

        def task_26_ans_button_clicked():
            self.task_26_show_ans_btn.setParent(None)
            self.task_26_widget_clicked_grid.addWidget(self.task_26_answer, 2, 0)
        def task_26_descr_button_clicked():
            self.task_26_show_descr_btn.setParent(None)
            self.task_26_widget_clicked_grid.addWidget(self.task_26_description_widget, 3, 0)

        self.task_26_show_ans_btn.clicked.connect(task_26_ans_button_clicked)
        self.task_26_show_descr_btn.clicked.connect(task_26_descr_button_clicked)

        self.task_26_get_file_btn.clicked.connect(lambda: task_get_file_button_clicked(26))


        # 2727272727272727272727272727
        self.task_27_widget = QWidget()
        self.task_27_data = Task_Chooser.choose_task(27)
        self.task_27_text = QLabel(self.task_27_data['text'])
        self.task_27_text.setWordWrap(True)
        self.task_27_text.setAlignment(Qt.AlignCenter)
        self.task_27_answer = QLabel(Localization.BASE_ANSWER + self.task_27_data['answer'])
        self.task_27_answer.setWordWrap(True)
        self.task_27_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_27_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_27_description = self.task_27_data['description']
        if self.task_27_data['python'].strip() != 'нет':
            self.task_27_description = self.task_27_description + '\n\n' + self.task_27_data['python']
        self.task_27_description_widget = QLabel(self.task_27_description)
        self.task_27_description_widget.setWordWrap(True)
        self.task_27_widget_clicked_grid = QGridLayout()

        self.task_27_get_file_a_btn = QPushButton(Localization.GET_FILE_A, self)
        self.task_27_get_file_b_btn = QPushButton(Localization.GET_FILE_B, self)
        self.task_27_file_a_path = 'data/tasks_data/27/' + self.task_27_data['id'] + '_A.txt'
        self.task_27_file_b_path = 'data/tasks_data/27/' + self.task_27_data['id'] + '_B.txt'
        
        self.task_27_widget_clicked_grid.addWidget(self.task_27_text, 0, 0, 1, 2)
        self.task_27_widget_clicked_grid.addWidget(self.task_27_get_file_a_btn, 1, 0, 1, 1)
        self.task_27_widget_clicked_grid.addWidget(self.task_27_get_file_b_btn, 1, 1, 1, 1)
        self.task_27_widget_clicked_grid.addWidget(self.task_27_show_ans_btn, 2, 0, 1, 2)
        self.task_27_widget_clicked_grid.addWidget(self.task_27_show_descr_btn, 3, 0, 1, 2)
        self.task_27_widget_clicked_grid.setRowStretch(4, 1) 
        self.task_27_widget.setLayout(self.task_27_widget_clicked_grid)

        def task_27_ans_button_clicked():
            self.task_27_show_ans_btn.setParent(None)
            self.task_27_widget_clicked_grid.addWidget(self.task_27_answer, 2, 0, 1, 2)
        def task_27_descr_button_clicked():
            self.task_27_show_descr_btn.setParent(None)
            self.task_27_widget_clicked_grid.addWidget(self.task_27_description_widget, 3, 0, 1, 2)

        self.task_27_show_ans_btn.clicked.connect(task_27_ans_button_clicked)
        self.task_27_show_descr_btn.clicked.connect(task_27_descr_button_clicked)

        def task_27_get_file_a_button_clicked():
            task_id = self.task_27_data['id']
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_27_file_a_path, destination_path + f"/27_{task_id}_A.txt")
                QMessageBox.information(self, Localization.EMAIL_SUCCESS_HEADER, Localization.EXAM_SUCCESS % (f"27_{task_id}_A.txt"), QMessageBox.Ok)
            except PermissionError:
                show_permission_error(self)
            except FileNotFoundError:
                pass
            except Exception as E:
                Logger.add_line_to_log("Error getting file for task 27_A. More: %s" % E)
                show_unknown_file_getting_error(self)
        self.task_27_get_file_a_btn.clicked.connect(task_27_get_file_a_button_clicked)

        def task_27_get_file_b_button_clicked():
            task_id = self.task_27_data['id']
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_27_file_b_path, destination_path + f"/27_{task_id}_B.txt")
                QMessageBox.information(self, Localization.EMAIL_SUCCESS_HEADER, Localization.EXAM_SUCCESS % (f"27_{task_id}_B.txt"), QMessageBox.Ok)
            except PermissionError:
                show_permission_error(self)
            except FileNotFoundError:
                pass
            except Exception as E:
                Logger.add_line_to_log("Error getting file for task 27_B. More: %s" % E)
                show_unknown_file_getting_error(self)
        self.task_27_get_file_b_btn.clicked.connect(task_27_get_file_b_button_clicked)


        # aft
        self.grid_clicked = QGridLayout()
        self.grid_clicked.addWidget(self.lbl2, 0, 0, alignment=Qt.AlignCenter)
        self.task_widgets = {
            '1': self.task_1_widget,
            '2': self.task_2_widget,
            '3': self.task_3_widget,
            '4': self.task_4_widget,
            '5': self.task_5_widget,
            '6': self.task_6_widget,
            '7': self.task_7_widget,
            '8': self.task_8_widget,
            '9': self.task_9_widget,
            '10': self.task_10_widget,
            '11': self.task_11_widget,
            '12': self.task_12_widget,
            '13': self.task_13_widget,
            '14': self.task_14_widget,
            '15': self.task_15_widget,
            '16': self.task_16_widget,
            '17': self.task_17_widget,
            '18': self.task_18_widget,
            '19-21': self.tasks19_21tab_widget,
            '22': self.task_22_widget,
            '23': self.task_23_widget,
            '24': self.task_24_widget,
            '25': self.task_25_widget,
            '26': self.task_26_widget,
            '27': self.task_27_widget
        }
        try:
            self.scrollArea_base_task = QScrollArea()
            self.scrollArea_base_task.setWidgetResizable(True)
            self.scrollArea_base_task.setWidget(self.task_widgets[task_num])
            self.grid_clicked.addWidget(self.scrollArea_base_task, 1, 0)
        except KeyError:
            pass
        self.grid_clicked.addWidget(self.back_btn, 2, 0)

        if task_num == "19-21":
            self.save_key = self.__dict__['task_19_21_data']['id']
        else:
            self.save_key = self.__dict__['task_%s_data' % str(task_num)]['id']
        save_manager.add_id_to_save(task_num, self.save_key)

        self.scrollArea = QScrollArea()
        self.setCentralWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)
        self.contents = QWidget()
        self.scrollArea.setWidget(self.contents)
        self.contents.setLayout(self.grid_clicked)

    def setupUi(self, BaseWindow):
        BaseWindow.resize(1000, 600)
        BaseWindow.move(100, 100)
        self.combo_last_picked_index = None
        self.setupUi_continue()