import os
import shutil
import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap

from task_manager import Task_Chooser
from data_manager import Localization, Config, Email, ID_Vars, Logger
import save_manager


class UI_VarWindow(object):
    def __init__(self):
        self.setByIdSelf()
        self.setVarIdSelf()
        self.getTasksData(self.by_id)

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

    def getTasksData(self, var_by_id=None):
        if var_by_id is None:
            var_by_id = False
        self.tasks_data = dict()
        if var_by_id:
            self.var_data = ID_Vars.get_data_by_id(self.var_id)
            for task in range(1, 28):
                self.task_id_in_base = self.var_data[str(task)]
                self.task_list = Task_Chooser.get_task_list(task)
                for elem in self.task_list:
                    if elem['id'] == self.task_id_in_base:
                        self.tasks_data[task] = elem
                        if not save_manager.check_id_in_save(task, self.task_id_in_base):
                            save_manager.add_id_to_save(task, self.task_id_in_base)
                        break
            Logger.add_line_to_log("Succesfully loaded ID %s." % self.var_id)
        else:
            for number in range(1, 28):
                self.tasks_data[number] = Task_Chooser.choose_task(number)
                save_manager.add_id_to_save(number, self.tasks_data[number]['id'])
        self.user_answers = [None for _ in range(28)]

    def timerSetup(self):
        self.start = False
        self.count = Config.TIMER_TIME_IN_SECONDS
        self.start = True

    def timerAction(self):
        if self.start:
            self.count -= 1
            if self.count == 0:
                self.start = False
                self.timer_has_ended = True
                self.timer_text_lbl.setText(Localization.TIMER_TEXT_TIME_EXPIRED)
                self.finish()
        if self.start:
            hours = str(self.count // 3600)
            hours = '0' + hours if len(hours) == 1 else hours
            minutes = str((self.count % 3600) // 60)
            minutes = '0' + minutes if len(minutes) == 1 else minutes
            seconds = str((self.count % 3600) % 60)
            seconds = '0' + seconds if len(seconds) == 1 else seconds
            remaining_text = Config.TIMER_FORMAT % (hours, minutes, seconds) 
            text = Localization.TIMER_TEXT % remaining_text
            self.timer_text_lbl.setText(text)


    def setupUi(self, BaseWindow):
        BaseWindow.resize(1000, 600)
        BaseWindow.move(300, 300)
        self.setWindowTitle(Localization.VAR_WIN_TITLE)
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

        self.centralWidget = QWidget()
        self.centralLayout = QGridLayout()

        self.contents_nums = QWidget()
        self.nums_widget_layout = QGridLayout()
        self.buttons_list = [None] + [QPushButton(str(number), self) for number in range(1, 28)]
        self.placing_x = 0
        for button in self.buttons_list[1:]:
            self.nums_widget_layout.addWidget(button, self.placing_x, 0)
            self.placing_x = self.placing_x + 1
        self.contents_nums.setLayout(self.nums_widget_layout)

        self.contents_tasks = QStackedWidget()
        self.contents_default = QWidget()
        self.tasks_widget_layout_default = QGridLayout()
        self.default_text = QLabel(Localization.VAR_DEFAULT_TEXT)
        self.tasks_widget_layout_default.addWidget(self.default_text)
        self.contents_default.setLayout(self.tasks_widget_layout_default)

        self.timer = QTimer()
        self.start = False
        self.count = 0
        self.timer.timeout.connect(self.timerAction)
        self.timer.start(1000)
        self.timer_text_lbl = QLabel('Таймер запустится, когда вы откроете любое задание.')
        self.timer_isnt_started = True
        self.timer_has_ended = False
        self.var_saved = False


        # 111111111
        self.task_1_widget = QWidget()
        self.task_1_data = self.tasks_data[1]
        self.task_1_text = QLabel(self.task_1_data['text'])
        self.task_1_text.setWordWrap(True)
        self.task_1_text.setAlignment(Qt.AlignCenter)
        self.task_1_answer = self.task_1_data['answer']
        self.task_1_widget_clicked_grid = QGridLayout()

        self.task_1_picture_path = 'data/tasks_data/1/' + self.task_1_data['id'] + '.png'
        self.task_1_picture_exists = True if os.path.exists(self.task_1_picture_path) else False
        if self.task_1_picture_exists:
            self.task_1_picture = QPixmap(self.task_1_picture_path)
            self.task_1_picture_lbl = QLabel(self)
            self.task_1_picture_lbl.setPixmap(self.task_1_picture)

        self.task_1_blank = QLineEdit()
        self.task_1_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_1():
            self.user_answers[1] = self.task_1_blank.text()
            self.task_1_blank.setEnabled(False)
            self.task_1_save_button.setParent(None)
            self.task_1_widget_clicked_grid.addWidget(self.task_1_edit_button, 28, 0, 29, 0)
        def edit_task_1():
            self.task_1_blank.setEnabled(True)
            self.task_1_edit_button.setParent(None)
            self.task_1_widget_clicked_grid.addWidget(self.task_1_save_button, 28, 0, 29, 0)
        self.task_1_save_button = QPushButton(Localization.SAVE)
        self.task_1_save_button.clicked.connect(save_task_1)
        self.task_1_edit_button = QPushButton(Localization.EDIT)
        self.task_1_edit_button.clicked.connect(edit_task_1)
        
        self.task_1_widget_clicked_grid.addWidget(self.task_1_text, 1, 0, 7, 0)
        if self.task_1_picture_exists:
            self.task_1_widget_clicked_grid.addWidget(self.task_1_picture_lbl, 8, 0, 15, 0, alignment=Qt.AlignCenter)
        self.task_1_widget_clicked_grid.addWidget(self.task_1_blank, 25, 0, 26, 0)
        self.task_1_widget_clicked_grid.addWidget(self.task_1_save_button, 28, 0, 29, 0)
        self.task_1_widget.setLayout(self.task_1_widget_clicked_grid)


        # 222222222
        self.task_2_widget = QWidget()
        self.task_2_data = self.tasks_data[2]
        self.task_2_text = QLabel(self.task_2_data['text'])
        self.task_2_text.setWordWrap(True)
        self.task_2_text.setAlignment(Qt.AlignCenter)
        self.task_2_answer = self.task_2_data['answer']
        self.task_2_widget_clicked_grid = QGridLayout()

        self.task_2_picture_path = 'data/tasks_data/2/' + self.task_2_data['id'] + '.png'
        self.task_2_picture_exists = True if os.path.exists(self.task_2_picture_path) else False
        if self.task_2_picture_exists:
            self.task_2_picture = QPixmap(self.task_2_picture_path)
            self.task_2_picture_lbl = QLabel(self)
            self.task_2_picture_lbl.setPixmap(self.task_2_picture)

        self.task_2_blank = QLineEdit()
        self.task_2_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_2():
            self.user_answers[2] = self.task_2_blank.text()
            self.task_2_blank.setEnabled(False)
            self.task_2_save_button.setParent(None)
            self.task_2_widget_clicked_grid.addWidget(self.task_2_edit_button, 28, 0, 29, 0)
        def edit_task_2():
            self.task_2_blank.setEnabled(True)
            self.task_2_edit_button.setParent(None)
            self.task_2_widget_clicked_grid.addWidget(self.task_2_save_button, 28, 0, 29, 0)
        self.task_2_save_button = QPushButton(Localization.SAVE)
        self.task_2_save_button.clicked.connect(save_task_2)
        self.task_2_edit_button = QPushButton(Localization.EDIT)
        self.task_2_edit_button.clicked.connect(edit_task_2)
        
        self.task_2_widget_clicked_grid.addWidget(self.task_2_text, 1, 0, 7, 0)
        if self.task_2_picture_exists:
            self.task_2_widget_clicked_grid.addWidget(self.task_2_picture_lbl, 8, 0, 25, 0, alignment=Qt.AlignCenter)
        self.task_2_widget_clicked_grid.addWidget(self.task_2_blank, 25, 0, 26, 0)
        self.task_2_widget_clicked_grid.addWidget(self.task_2_save_button, 28, 0, 29, 0)
        self.task_2_widget.setLayout(self.task_2_widget_clicked_grid)


        #333333333
        self.task_3_widget = QWidget()
        self.task_3_data = self.tasks_data[3]

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

        self.task_3_answer = self.task_3_data['answer']
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

        self.task_3_blank = QLineEdit()
        self.task_3_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_3():
            self.user_answers[3] = self.task_3_blank.text()
            self.task_3_blank.setEnabled(False)
            self.task_3_save_button.setParent(None)
            self.task_3_widget_clicked_grid.addWidget(self.task_3_edit_button, 1400, 0, 1407, 0)
        def edit_task_3():
            self.task_3_blank.setEnabled(True)
            self.task_3_edit_button.setParent(None)
            self.task_3_widget_clicked_grid.addWidget(self.task_3_save_button, 1400, 0, 1407, 0)
        self.task_3_save_button = QPushButton(Localization.SAVE)
        self.task_3_save_button.clicked.connect(save_task_3)
        self.task_3_edit_button = QPushButton(Localization.EDIT)
        self.task_3_edit_button.clicked.connect(edit_task_3)
        
        self.task_3_widget_clicked_grid.addWidget(self.task_3_text1, 0, 0, 1, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_get_file_btn, 2, 0, 3, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_text2, 4, 0, 6, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_picture_2to3_lbl, 9, 0, 11, 0, alignment=Qt.AlignCenter)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_text3, 15, 0, 16, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_picture_3to4_lbl, 25, 0, 27, 0, alignment=Qt.AlignCenter)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_text4, 39, 0, 41, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_picture_4to5_lbl, 62, 0, 64, 0, alignment=Qt.AlignCenter)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_text5, 86, 0, 87, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_picture_5to6_lbl, 166, 0, 168, 0, alignment=Qt.AlignCenter)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_text6, 330, 0, 332, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_blank, 650, 0, 652, 0)
        self.task_3_widget_clicked_grid.addWidget(self.task_3_save_button, 1400, 0, 1407, 0)
        self.task_3_widget.setLayout(self.task_3_widget_clicked_grid)

        def task_3_get_file_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_3_file_path, destination_path)
            except FileNotFoundError:
                pass

        self.task_3_get_file_btn.clicked.connect(task_3_get_file_button_clicked)


        #444444444
        self.task_4_widget = QWidget()
        self.task_4_data = self.tasks_data[4]
        self.task_4_text = QLabel(self.task_4_data['text'])
        self.task_4_text.setWordWrap(True)
        self.task_4_text.setAlignment(Qt.AlignCenter)
        self.task_4_answer = self.task_4_data['answer']
        self.task_4_widget_clicked_grid = QGridLayout()

        self.task_4_blank = QLineEdit()
        self.task_4_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_4():
            self.user_answers[4] = self.task_4_blank.text()
            self.task_4_blank.setEnabled(False)
            self.task_4_save_button.setParent(None)
            self.task_4_widget_clicked_grid.addWidget(self.task_4_edit_button, 9, 0, 10, 0)
        def edit_task_4():
            self.task_4_blank.setEnabled(True)
            self.task_4_edit_button.setParent(None)
            self.task_4_widget_clicked_grid.addWidget(self.task_4_save_button, 9, 0, 10, 0)
        self.task_4_save_button = QPushButton(Localization.SAVE)
        self.task_4_save_button.clicked.connect(save_task_4)
        self.task_4_edit_button = QPushButton(Localization.EDIT)
        self.task_4_edit_button.clicked.connect(edit_task_4)
        
        self.task_4_widget_clicked_grid.addWidget(self.task_4_text, 1, 0, 7, 0)
        self.task_4_widget_clicked_grid.addWidget(self.task_4_blank, 8, 0, 9, 0)
        self.task_4_widget_clicked_grid.addWidget(self.task_4_save_button, 9, 0, 10, 0)
        self.task_4_widget.setLayout(self.task_4_widget_clicked_grid)


        #555555555
        self.task_5_widget = QWidget()
        self.task_5_data = self.tasks_data[5]
        self.task_5_text = QLabel(self.task_5_data['text'])
        self.task_5_text.setWordWrap(True)
        self.task_5_text.setAlignment(Qt.AlignCenter)
        self.task_5_answer = self.task_5_data['answer']
        self.task_5_widget_clicked_grid = QGridLayout()

        self.task_5_blank = QLineEdit()
        self.task_5_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_5():
            self.user_answers[5] = self.task_5_blank.text()
            self.task_5_blank.setEnabled(False)
            self.task_5_save_button.setParent(None)
            self.task_5_widget_clicked_grid.addWidget(self.task_5_edit_button, 9, 0, 10, 0)
        def edit_task_5():
            self.task_5_blank.setEnabled(True)
            self.task_5_edit_button.setParent(None)
            self.task_5_widget_clicked_grid.addWidget(self.task_5_save_button, 9, 0, 10, 0)
        self.task_5_save_button = QPushButton(Localization.SAVE)
        self.task_5_save_button.clicked.connect(save_task_5)
        self.task_5_edit_button = QPushButton(Localization.EDIT)
        self.task_5_edit_button.clicked.connect(edit_task_5)
        
        self.task_5_widget_clicked_grid.addWidget(self.task_5_text, 1, 0, 7, 0)
        self.task_5_widget_clicked_grid.addWidget(self.task_5_blank, 8, 0, 9, 0)
        self.task_5_widget_clicked_grid.addWidget(self.task_5_save_button, 9, 0, 10, 0)
        self.task_5_widget.setLayout(self.task_5_widget_clicked_grid)


        #666666666
        self.task_6_widget = QWidget()
        self.task_6_data = self.tasks_data[6]
        self.task_6_text = QLabel(self.task_6_data['text'] + '\n\n' + self.task_6_data['program'])
        self.task_6_text.setWordWrap(True)
        self.task_6_answer = self.task_6_data['answer']
        self.task_6_widget_clicked_grid = QGridLayout()

        self.task_6_blank = QLineEdit()
        self.task_6_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_6():
            self.user_answers[6] = self.task_6_blank.text()
            self.task_6_blank.setEnabled(False)
            self.task_6_save_button.setParent(None)
            self.task_6_widget_clicked_grid.addWidget(self.task_6_edit_button, 9, 0, 10, 0)
        def edit_task_6():
            self.task_6_blank.setEnabled(True)
            self.task_6_edit_button.setParent(None)
            self.task_6_widget_clicked_grid.addWidget(self.task_6_save_button, 9, 0, 10, 0)
        self.task_6_save_button = QPushButton(Localization.SAVE)
        self.task_6_save_button.clicked.connect(save_task_6)
        self.task_6_edit_button = QPushButton(Localization.EDIT)
        self.task_6_edit_button.clicked.connect(edit_task_6)
        
        self.task_6_widget_clicked_grid.addWidget(self.task_6_text, 1, 0, 7, 0, alignment=Qt.AlignCenter)
        self.task_6_widget_clicked_grid.addWidget(self.task_6_blank, 8, 0, 9, 0)
        self.task_6_widget_clicked_grid.addWidget(self.task_6_save_button, 9, 0, 10, 0)
        self.task_6_widget.setLayout(self.task_6_widget_clicked_grid)


        #777777777
        self.task_7_widget = QWidget()
        self.task_7_data = self.tasks_data[7]
        self.task_7_text = QLabel(self.task_7_data['text'])
        self.task_7_text.setWordWrap(True)
        self.task_5_text.setAlignment(Qt.AlignCenter)
        self.task_7_answer = self.task_7_data['answer']
        self.task_7_widget_clicked_grid = QGridLayout()

        self.task_7_blank = QLineEdit()
        self.task_7_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_7():
            self.user_answers[7] = self.task_7_blank.text()
            self.task_7_blank.setEnabled(False)
            self.task_7_save_button.setParent(None)
            self.task_7_widget_clicked_grid.addWidget(self.task_7_edit_button, 9, 0, 10, 0)
        def edit_task_7():
            self.task_7_blank.setEnabled(True)
            self.task_7_edit_button.setParent(None)
            self.task_7_widget_clicked_grid.addWidget(self.task_7_save_button, 9, 0, 10, 0)
        self.task_7_save_button = QPushButton(Localization.SAVE)
        self.task_7_save_button.clicked.connect(save_task_7)
        self.task_7_edit_button = QPushButton(Localization.EDIT)
        self.task_7_edit_button.clicked.connect(edit_task_7)
        
        self.task_7_widget_clicked_grid.addWidget(self.task_7_text, 1, 0, 7, 0)
        self.task_7_widget_clicked_grid.addWidget(self.task_7_blank, 8, 0, 9, 0)
        self.task_7_widget_clicked_grid.addWidget(self.task_7_save_button, 9, 0, 10, 0)
        self.task_7_widget.setLayout(self.task_7_widget_clicked_grid)


        #888888888
        self.task_8_widget = QWidget()
        self.task_8_data = self.tasks_data[8]
        self.task_8_text = QLabel(self.task_8_data['text'])
        self.task_8_text.setWordWrap(True)
        self.task_8_text.setAlignment(Qt.AlignCenter)
        self.task_8_answer = self.task_8_data['answer']
        self.task_8_widget_clicked_grid = QGridLayout()

        self.task_8_blank = QLineEdit()
        self.task_8_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_8():
            self.user_answers[8] = self.task_8_blank.text()
            self.task_8_blank.setEnabled(False)
            self.task_8_save_button.setParent(None)
            self.task_8_widget_clicked_grid.addWidget(self.task_8_edit_button, 9, 0, 10, 0)
        def edit_task_8():
            self.task_8_blank.setEnabled(True)
            self.task_8_edit_button.setParent(None)
            self.task_8_widget_clicked_grid.addWidget(self.task_8_save_button, 9, 0, 10, 0)
        self.task_8_save_button = QPushButton(Localization.SAVE)
        self.task_8_save_button.clicked.connect(save_task_8)
        self.task_8_edit_button = QPushButton(Localization.EDIT)
        self.task_8_edit_button.clicked.connect(edit_task_8)
        
        self.task_8_widget_clicked_grid.addWidget(self.task_8_text, 1, 0, 7, 0)
        self.task_8_widget_clicked_grid.addWidget(self.task_8_blank, 8, 0, 9, 0)
        self.task_8_widget_clicked_grid.addWidget(self.task_8_save_button, 9, 0, 10, 0)
        self.task_8_widget.setLayout(self.task_8_widget_clicked_grid)


        #999999999
        self.task_9_widget = QWidget()
        self.task_9_data = self.tasks_data[9]
        self.task_9_text = QLabel(self.task_9_data['text'])
        self.task_9_text.setWordWrap(True)
        self.task_9_text.setAlignment(Qt.AlignCenter)
        self.task_9_answer = self.task_9_data['answer']
        self.task_9_widget_clicked_grid = QGridLayout()

        self.task_9_blank = QLineEdit()
        self.task_9_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_9():
            self.user_answers[9] = self.task_9_blank.text()
            self.task_9_blank.setEnabled(False)
            self.task_9_save_button.setParent(None)
            self.task_9_widget_clicked_grid.addWidget(self.task_9_edit_button, 11, 0, 12, 0)
        def edit_task_9():
            self.task_9_blank.setEnabled(True)
            self.task_9_edit_button.setParent(None)
            self.task_9_widget_clicked_grid.addWidget(self.task_9_save_button, 11, 0, 12, 0)
        self.task_9_save_button = QPushButton(Localization.SAVE)
        self.task_9_save_button.clicked.connect(save_task_9)
        self.task_9_edit_button = QPushButton(Localization.EDIT)
        self.task_9_edit_button.clicked.connect(edit_task_9)

        self.task_9_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_9_file_path = 'data/tasks_data/9/' + self.task_9_data['id'] + '.xlsx'
        def task_9_get_file_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_9_file_path, destination_path)
            except FileNotFoundError:
                pass
            self.task_9_get_file_btn.clicked.connect(task_9_get_file_button_clicked)
        
        self.task_9_widget_clicked_grid.addWidget(self.task_9_text, 1, 0, 7, 0)
        self.task_9_widget_clicked_grid.addWidget(self.task_9_get_file_btn, 8, 0, 9, 0)
        self.task_9_widget_clicked_grid.addWidget(self.task_9_blank, 10, 0, 11, 0)
        self.task_9_widget_clicked_grid.addWidget(self.task_9_save_button, 11, 0, 12, 0)
        self.task_9_widget.setLayout(self.task_9_widget_clicked_grid)



        #101010101010101010
        self.task_10_widget = QWidget()
        self.task_10_data = self.tasks_data[10]
        self.task_10_text = QLabel(self.task_10_data['text'])
        self.task_10_text.setWordWrap(True)
        self.task_10_text.setAlignment(Qt.AlignCenter)
        self.task_10_answer = self.task_10_data['answer']
        self.task_10_widget_clicked_grid = QGridLayout()

        self.task_10_blank = QLineEdit()
        self.task_10_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_10():
            self.user_answers[10] = self.task_10_blank.text()
            self.task_10_blank.setEnabled(False)
            self.task_10_save_button.setParent(None)
            self.task_10_widget_clicked_grid.addWidget(self.task_10_edit_button, 11, 0, 12, 0)
        def edit_task_10():
            self.task_10_blank.setEnabled(True)
            self.task_10_edit_button.setParent(None)
            self.task_10_widget_clicked_grid.addWidget(self.task_10_save_button, 11, 0, 12, 0)
        self.task_10_save_button = QPushButton(Localization.SAVE)
        self.task_10_save_button.clicked.connect(save_task_10)
        self.task_10_edit_button = QPushButton(Localization.EDIT)
        self.task_10_edit_button.clicked.connect(edit_task_10)

        self.task_10_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_10_file_path = 'data/tasks_data/10/' + self.task_10_data['id'] + '.docx'
        def task_10_get_file_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_10_file_path, destination_path)
            except FileNotFoundError:
                pass
            self.task_10_get_file_btn.clicked.connect(task_10_get_file_button_clicked)
        
        self.task_10_widget_clicked_grid.addWidget(self.task_10_text, 1, 0, 7, 0)
        self.task_10_widget_clicked_grid.addWidget(self.task_10_get_file_btn, 8, 0, 10, 0)
        self.task_10_widget_clicked_grid.addWidget(self.task_10_blank, 9, 0, 11, 0)
        self.task_10_widget_clicked_grid.addWidget(self.task_10_save_button, 11, 0, 12, 0)
        self.task_10_widget.setLayout(self.task_10_widget_clicked_grid)


        #111111111111111111
        self.task_11_widget = QWidget()
        self.task_11_data = self.tasks_data[11]
        self.task_11_text = QLabel(self.task_11_data['text'])
        self.task_11_text.setWordWrap(True)
        self.task_11_text.setAlignment(Qt.AlignCenter)
        self.task_11_answer = self.task_11_data['answer']
        self.task_11_widget_clicked_grid = QGridLayout()

        self.task_11_blank = QLineEdit()
        self.task_11_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_11():
            self.user_answers[11] = self.task_11_blank.text()
            self.task_11_blank.setEnabled(False)
            self.task_11_save_button.setParent(None)
            self.task_11_widget_clicked_grid.addWidget(self.task_11_edit_button, 9, 0, 10, 0)
        def edit_task_11():
            self.task_11_blank.setEnabled(True)
            self.task_11_edit_button.setParent(None)
            self.task_11_widget_clicked_grid.addWidget(self.task_11_save_button, 9, 0, 10, 0)
        self.task_11_save_button = QPushButton(Localization.SAVE)
        self.task_11_save_button.clicked.connect(save_task_11)
        self.task_11_edit_button = QPushButton(Localization.EDIT)
        self.task_11_edit_button.clicked.connect(edit_task_11)
        
        self.task_11_widget_clicked_grid.addWidget(self.task_11_text, 1, 0, 7, 0)
        self.task_11_widget_clicked_grid.addWidget(self.task_11_blank, 8, 0, 9, 0)
        self.task_11_widget_clicked_grid.addWidget(self.task_11_save_button, 9, 0, 10, 0)
        self.task_11_widget.setLayout(self.task_11_widget_clicked_grid)


        # 12121212121212121212
        self.task_12_widget = QWidget()
        self.task_12_data = self.tasks_data[12]
        self.task_12_text = QLabel(self.task_12_data['text'])
        self.task_12_text.setWordWrap(True)
        self.task_12_answer = self.task_12_data['answer']
        self.task_12_widget_clicked_grid = QGridLayout()

        if self.task_12_data['hasPictures'] == True:
            self.task_12_picture_path = 'data/tasks_data/12/' + self.task_12_data['id'] + '.png'
            self.task_12_picture_exists = True if os.path.exists(self.task_12_picture_path) else False
            if self.task_12_picture_exists:
                self.task_12_picture = QPixmap(self.task_12_picture_path)
                self.task_12_picture_lbl = QLabel(self)
                self.task_12_picture_lbl.setPixmap(self.task_12_picture)

        self.task_12_blank = QLineEdit()
        self.task_12_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_12():
            self.user_answers[12] = self.task_12_blank.text()
            self.task_12_blank.setEnabled(False)
            self.task_12_save_button.setParent(None)
            self.task_12_widget_clicked_grid.addWidget(self.task_12_edit_button, 21, 0, 22, 0)
        def edit_task_12():
            self.task_12_blank.setEnabled(True)
            self.task_12_edit_button.setParent(None)
            self.task_12_widget_clicked_grid.addWidget(self.task_12_save_button, 21, 0, 22, 0)
        self.task_12_save_button = QPushButton(Localization.SAVE)
        self.task_12_save_button.clicked.connect(save_task_12)
        self.task_12_edit_button = QPushButton(Localization.EDIT)
        self.task_12_edit_button.clicked.connect(edit_task_12)

        if self.task_12_data['hasPictures'] == False:
            self.task_12_widget_clicked_grid.addWidget(self.task_12_text, 1, 0, 15, 0)
            self.task_12_widget_clicked_grid.addWidget(self.task_12_blank, 18, 0, 20, 0)
            self.task_12_widget_clicked_grid.addWidget(self.task_12_save_button, 21, 0, 22, 0)
            self.task_12_widget.setLayout(self.task_12_widget_clicked_grid)
        elif self.task_12_data['hasPictures'] == True:
            self.task_12_widget_clicked_grid.addWidget(self.task_12_picture_lbl, 1, 0, 15, 1)
            self.task_12_widget_clicked_grid.addWidget(self.task_12_text, 1, 2, 15, 9)
            self.task_12_widget_clicked_grid.addWidget(self.task_12_blank, 18, 0, 20, 0)
            self.task_12_widget_clicked_grid.addWidget(self.task_12_save_button, 21, 0, 22, 0)
            self.task_12_widget.setLayout(self.task_12_widget_clicked_grid)


        # 131313131313131313
        self.task_13_widget = QWidget()
        self.task_13_data = self.tasks_data[13]
        self.task_13_text = QLabel(self.task_13_data['text'])
        self.task_13_text.setWordWrap(True)
        self.task_13_text.setAlignment(Qt.AlignCenter)
        self.task_13_answer = self.task_13_data['answer']
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

        self.task_13_blank = QLineEdit()
        self.task_13_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_13():
            self.user_answers[13] = self.task_13_blank.text()
            self.task_13_blank.setEnabled(False)
            self.task_13_save_button.setParent(None)
            self.task_13_widget_clicked_grid.addWidget(self.task_13_edit_button, 30, 0, 31, 0)
        def edit_task_13():
            self.task_13_blank.setEnabled(True)
            self.task_13_edit_button.setParent(None)
            self.task_13_widget_clicked_grid.addWidget(self.task_13_save_button, 30, 0, 31, 0)
        self.task_13_save_button = QPushButton(Localization.SAVE)
        self.task_13_save_button.clicked.connect(save_task_13)
        self.task_13_edit_button = QPushButton(Localization.EDIT)
        self.task_13_edit_button.clicked.connect(edit_task_13)
        
        self.task_13_widget_clicked_grid.addWidget(self.task_13_text, 1, 0, 7, 0)
        if self.task_13_picture_exists:
            self.task_13_widget_clicked_grid.addWidget(self.task_13_picture_lbl, 8, 0, 15, 0, alignment=Qt.AlignCenter)
        self.task_13_widget_clicked_grid.addWidget(self.task_13_blank, 25, 0, 26, 0)
        self.task_13_widget_clicked_grid.addWidget(self.task_13_save_button, 30, 0, 31, 0)
        self.task_13_widget.setLayout(self.task_13_widget_clicked_grid)


        #141414141414141414
        self.task_14_widget = QWidget()
        self.task_14_data = self.tasks_data[14]
        self.task_14_text = QLabel(self.task_14_data['text'])
        self.task_14_text.setWordWrap(True)
        self.task_14_text.setAlignment(Qt.AlignCenter)
        self.task_14_answer = self.task_14_data['answer']
        self.task_14_widget_clicked_grid = QGridLayout()

        self.task_14_blank = QLineEdit()
        self.task_14_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_14():
            self.user_answers[14] = self.task_14_blank.text()
            self.task_14_blank.setEnabled(False)
            self.task_14_save_button.setParent(None)
            self.task_14_widget_clicked_grid.addWidget(self.task_14_edit_button, 9, 0, 10, 0)
        def edit_task_14():
            self.task_14_blank.setEnabled(True)
            self.task_14_edit_button.setParent(None)
            self.task_14_widget_clicked_grid.addWidget(self.task_14_save_button, 9, 0, 10, 0)
        self.task_14_save_button = QPushButton(Localization.SAVE)
        self.task_14_save_button.clicked.connect(save_task_14)
        self.task_14_edit_button = QPushButton(Localization.EDIT)
        self.task_14_edit_button.clicked.connect(edit_task_14)
        
        self.task_14_widget_clicked_grid.addWidget(self.task_14_text, 1, 0, 7, 0)
        self.task_14_widget_clicked_grid.addWidget(self.task_14_blank, 8, 0, 9, 0)
        self.task_14_widget_clicked_grid.addWidget(self.task_14_save_button, 9, 0, 10, 0)
        self.task_14_widget.setLayout(self.task_14_widget_clicked_grid)


        #151515151515151515
        self.task_15_widget = QWidget()
        self.task_15_data = self.tasks_data[15]
        self.task_15_text = QLabel(self.task_15_data['text'])
        self.task_15_text.setWordWrap(True)
        self.task_15_text.setAlignment(Qt.AlignCenter)
        self.task_15_answer = self.task_15_data['answer']
        self.task_15_widget_clicked_grid = QGridLayout()

        self.task_15_blank = QLineEdit()
        self.task_15_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_15():
            self.user_answers[15] = self.task_15_blank.text()
            self.task_15_blank.setEnabled(False)
            self.task_15_save_button.setParent(None)
            self.task_15_widget_clicked_grid.addWidget(self.task_15_edit_button, 9, 0, 10, 0)
        def edit_task_15():
            self.task_15_blank.setEnabled(True)
            self.task_15_edit_button.setParent(None)
            self.task_15_widget_clicked_grid.addWidget(self.task_15_save_button, 9, 0, 10, 0)
        self.task_15_save_button = QPushButton(Localization.SAVE)
        self.task_15_save_button.clicked.connect(save_task_15)
        self.task_15_edit_button = QPushButton(Localization.EDIT)
        self.task_15_edit_button.clicked.connect(edit_task_15)
        
        self.task_15_widget_clicked_grid.addWidget(self.task_15_text, 1, 0, 7, 0)
        self.task_15_widget_clicked_grid.addWidget(self.task_15_blank, 8, 0, 9, 0)
        self.task_15_widget_clicked_grid.addWidget(self.task_15_save_button, 9, 0, 10, 0)
        self.task_15_widget.setLayout(self.task_15_widget_clicked_grid)


        #161616161616161616
        self.task_16_widget = QWidget()
        self.task_16_data = self.tasks_data[16]
        self.task_16_text_for_lbl = self.task_16_data['text']
        if self.task_16_data['program'].strip() != 'нет':
            self.task_16_text_for_lbl = self.task_16_text_for_lbl + '\n\n' + self.task_16_data['program']
        self.task_16_text = QLabel(self.task_16_text_for_lbl)
        self.task_16_text.setWordWrap(True)
        self.task_16_answer = self.task_16_data['answer']
        self.task_16_widget_clicked_grid = QGridLayout()

        self.task_16_blank = QLineEdit()
        self.task_16_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_16():
            self.user_answers[16] = self.task_16_blank.text()
            self.task_16_blank.setEnabled(False)
            self.task_16_save_button.setParent(None)
            self.task_16_widget_clicked_grid.addWidget(self.task_16_edit_button, 9, 0, 10, 0)
        def edit_task_16():
            self.task_16_blank.setEnabled(True)
            self.task_16_edit_button.setParent(None)
            self.task_16_widget_clicked_grid.addWidget(self.task_16_save_button, 9, 0, 10, 0)
        self.task_16_save_button = QPushButton(Localization.SAVE)
        self.task_16_save_button.clicked.connect(save_task_16)
        self.task_16_edit_button = QPushButton(Localization.EDIT)
        self.task_16_edit_button.clicked.connect(edit_task_16)
        
        self.task_16_widget_clicked_grid.addWidget(self.task_16_text, 1, 0, 7, 0, alignment=Qt.AlignCenter)
        self.task_16_widget_clicked_grid.addWidget(self.task_16_blank, 8, 0, 9, 0)
        self.task_16_widget_clicked_grid.addWidget(self.task_16_save_button, 9, 0, 10, 0)
        self.task_16_widget.setLayout(self.task_16_widget_clicked_grid)


        #171717171717171717
        self.task_17_widget = QWidget()
        self.task_17_data = self.tasks_data[17]
        self.task_17_text = QLabel(self.task_17_data['text'])
        self.task_17_text.setWordWrap(True)
        self.task_17_text.setAlignment(Qt.AlignCenter)
        self.task_17_answer = self.task_17_data['answer']
        self.task_17_widget_clicked_grid = QGridLayout()

        self.task_17_blank = QLineEdit()
        self.task_17_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_17():
            self.user_answers[17] = self.task_17_blank.text()
            self.task_17_blank.setEnabled(False)
            self.task_17_save_button.setParent(None)
            self.task_17_widget_clicked_grid.addWidget(self.task_17_edit_button, 11, 0, 12, 0)
        def edit_task_17():
            self.task_17_blank.setEnabled(True)
            self.task_17_edit_button.setParent(None)
            self.task_17_widget_clicked_grid.addWidget(self.task_17_save_button, 11, 0, 12, 0)
        self.task_17_save_button = QPushButton(Localization.SAVE)
        self.task_17_save_button.clicked.connect(save_task_17)
        self.task_17_edit_button = QPushButton(Localization.EDIT)
        self.task_17_edit_button.clicked.connect(edit_task_17)

        self.task_17_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_17_file_path = 'data/tasks_data/17/' + self.task_17_data['fileName']
        def task_17_get_file_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_17_file_path, destination_path)
            except FileNotFoundError:
                pass
        self.task_17_get_file_btn.clicked.connect(task_17_get_file_button_clicked)
        
        self.task_17_widget_clicked_grid.addWidget(self.task_17_text, 1, 0, 7, 0)
        self.task_17_widget_clicked_grid.addWidget(self.task_17_get_file_btn, 8, 0, 10, 0)
        self.task_17_widget_clicked_grid.addWidget(self.task_17_blank, 9, 0, 11, 0)
        self.task_17_widget_clicked_grid.addWidget(self.task_17_save_button, 11, 0, 12, 0)
        self.task_17_widget.setLayout(self.task_17_widget_clicked_grid)


        #181818181818181818
        self.task_18_widget = QWidget()
        self.task_18_data = self.tasks_data[18]
        self.task_18_text = QLabel(self.task_18_data['text'])
        self.task_18_text.setWordWrap(True)
        self.task_18_text.setAlignment(Qt.AlignCenter)
        self.task_18_answer = self.task_18_data['answer']
        self.task_18_widget_clicked_grid = QGridLayout()

        self.task_18_blank = QLineEdit()
        self.task_18_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_18():
            self.user_answers[18] = self.task_18_blank.text()
            self.task_18_blank.setEnabled(False)
            self.task_18_save_button.setParent(None)
            self.task_18_widget_clicked_grid.addWidget(self.task_18_edit_button,14, 0, 15, 0)
        def edit_task_18():
            self.task_18_blank.setEnabled(True)
            self.task_18_edit_button.setParent(None)
            self.task_18_widget_clicked_grid.addWidget(self.task_18_save_button, 14, 0, 15, 0)
        self.task_18_save_button = QPushButton(Localization.SAVE)
        self.task_18_save_button.clicked.connect(save_task_18)
        self.task_18_edit_button = QPushButton(Localization.EDIT)
        self.task_18_edit_button.clicked.connect(edit_task_18)

        self.task_18_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_18_file_path = 'data/tasks_data/18/' + self.task_18_data['id'] + '.xlsx'
        def task_18_get_file_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_18_file_path, destination_path)
            except FileNotFoundError:
                pass
        self.task_18_get_file_btn.clicked.connect(task_18_get_file_button_clicked)

        self.task_18_picture_path = 'data/tasks_data/18/example.png'
        self.task_18_picture = QPixmap(self.task_18_picture_path)
        self.task_18_picture_lbl = QLabel(self)
        self.task_18_picture_lbl.setPixmap(self.task_18_picture)
        
        self.task_18_widget_clicked_grid.addWidget(self.task_18_text, 1, 0, 5, 0)
        self.task_18_widget_clicked_grid.addWidget(self.task_18_picture_lbl, 5, 0, 9, 0, alignment=Qt.AlignCenter)
        self.task_18_widget_clicked_grid.addWidget(self.task_18_get_file_btn, 10, 0, 11, 0)
        self.task_18_widget_clicked_grid.addWidget(self.task_18_blank, 12, 0, 13, 0)
        self.task_18_widget_clicked_grid.addWidget(self.task_18_save_button, 14, 0, 15, 0)
        self.task_18_widget.setLayout(self.task_18_widget_clicked_grid)


        #191919191919191919
        self.task_19_widget = QWidget()
        self.task_19_data = self.tasks_data[19]
        self.task_19_text = QLabel(self.task_19_data['text'])
        self.task_19_text.setWordWrap(True)
        self.task_19_text.setAlignment(Qt.AlignCenter)
        self.task_19_answer = self.task_19_data['answer']
        self.task_19_widget_clicked_grid = QGridLayout()

        self.task_19_blank = QLineEdit()
        self.task_19_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_19():
            self.user_answers[19] = self.task_19_blank.text()
            self.task_19_blank.setEnabled(False)
            self.task_19_save_button.setParent(None)
            self.task_19_widget_clicked_grid.addWidget(self.task_19_edit_button, 9, 0, 10, 0)
        def edit_task_19():
            self.task_19_blank.setEnabled(True)
            self.task_19_edit_button.setParent(None)
            self.task_19_widget_clicked_grid.addWidget(self.task_19_save_button, 9, 0, 10, 0)
        self.task_19_save_button = QPushButton(Localization.SAVE)
        self.task_19_save_button.clicked.connect(save_task_19)
        self.task_19_edit_button = QPushButton(Localization.EDIT)
        self.task_19_edit_button.clicked.connect(edit_task_19)
        
        self.task_19_widget_clicked_grid.addWidget(self.task_19_text, 1, 0, 7, 0)
        self.task_19_widget_clicked_grid.addWidget(self.task_19_blank, 8, 0, 9, 0)
        self.task_19_widget_clicked_grid.addWidget(self.task_19_save_button, 9, 0, 10, 0)
        self.task_19_widget.setLayout(self.task_19_widget_clicked_grid)


        #202020202020202020
        self.task_20_widget = QWidget()
        self.task_20_data = self.tasks_data[20]
        self.task_20_text = QLabel(self.task_20_data['text'])
        self.task_20_text.setWordWrap(True)
        self.task_20_text.setAlignment(Qt.AlignCenter)
        self.task_20_answer = self.task_20_data['answer']
        self.task_20_widget_clicked_grid = QGridLayout()

        self.task_20_blank = QLineEdit()
        self.task_20_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_20():
            self.user_answers[20] = self.task_20_blank.text()
            self.task_20_blank.setEnabled(False)
            self.task_20_save_button.setParent(None)
            self.task_20_widget_clicked_grid.addWidget(self.task_20_edit_button, 9, 0, 10, 0)
        def edit_task_20():
            self.task_20_blank.setEnabled(True)
            self.task_20_edit_button.setParent(None)
            self.task_20_widget_clicked_grid.addWidget(self.task_20_save_button, 9, 0, 10, 0)
        self.task_20_save_button = QPushButton(Localization.SAVE)
        self.task_20_save_button.clicked.connect(save_task_20)
        self.task_20_edit_button = QPushButton(Localization.EDIT)
        self.task_20_edit_button.clicked.connect(edit_task_20)
        
        self.task_20_widget_clicked_grid.addWidget(self.task_20_text, 1, 0, 7, 0)
        self.task_20_widget_clicked_grid.addWidget(self.task_20_blank, 8, 0, 9, 0)
        self.task_20_widget_clicked_grid.addWidget(self.task_20_save_button, 9, 0, 10, 0)
        self.task_20_widget.setLayout(self.task_20_widget_clicked_grid)


        #212121212121212121
        self.task_21_widget = QWidget()
        self.task_21_data = self.tasks_data[21]
        self.task_21_text = QLabel(self.task_21_data['text'])
        self.task_21_text.setWordWrap(True)
        self.task_21_text.setAlignment(Qt.AlignCenter)
        self.task_21_answer = self.task_21_data['answer']
        self.task_21_widget_clicked_grid = QGridLayout()

        self.task_21_blank = QLineEdit()
        self.task_21_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_21():
            self.user_answers[21] = self.task_21_blank.text()
            self.task_21_blank.setEnabled(False)
            self.task_21_save_button.setParent(None)
            self.task_21_widget_clicked_grid.addWidget(self.task_21_edit_button, 9, 0, 10, 0)
        def edit_task_21():
            self.task_21_blank.setEnabled(True)
            self.task_21_edit_button.setParent(None)
            self.task_21_widget_clicked_grid.addWidget(self.task_21_save_button, 9, 0, 10, 0)
        self.task_21_save_button = QPushButton(Localization.SAVE)
        self.task_21_save_button.clicked.connect(save_task_21)
        self.task_21_edit_button = QPushButton(Localization.EDIT)
        self.task_21_edit_button.clicked.connect(edit_task_21)
        
        self.task_21_widget_clicked_grid.addWidget(self.task_21_text, 1, 0, 7, 0)
        self.task_21_widget_clicked_grid.addWidget(self.task_21_blank, 8, 0, 9, 0)
        self.task_21_widget_clicked_grid.addWidget(self.task_21_save_button, 9, 0, 10, 0)
        self.task_21_widget.setLayout(self.task_21_widget_clicked_grid)


        #222222222222222222
        self.task_22_widget = QWidget()
        self.task_22_data = self.tasks_data[22]
        self.task_22_text_for_lbl = self.task_22_data['text']
        if self.task_22_data['program'].strip() != 'нет':
            self.task_22_text_for_lbl = self.task_22_text_for_lbl + '\n\n' + self.task_22_data['program']
        self.task_22_text = QLabel(self.task_22_text_for_lbl)
        self.task_22_text.setWordWrap(True)
        self.task_22_answer = self.task_22_data['answer']
        self.task_22_widget_clicked_grid = QGridLayout()

        self.task_22_blank = QLineEdit()
        self.task_22_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_22():
            self.user_answers[22] = self.task_22_blank.text()
            self.task_22_blank.setEnabled(False)
            self.task_22_save_button.setParent(None)
            self.task_22_widget_clicked_grid.addWidget(self.task_22_edit_button, 9, 0, 10, 0)
        def edit_task_22():
            self.task_22_blank.setEnabled(True)
            self.task_22_edit_button.setParent(None)
            self.task_22_widget_clicked_grid.addWidget(self.task_22_save_button, 9, 0, 10, 0)
        self.task_22_save_button = QPushButton(Localization.SAVE)
        self.task_22_save_button.clicked.connect(save_task_22)
        self.task_22_edit_button = QPushButton(Localization.EDIT)
        self.task_22_edit_button.clicked.connect(edit_task_22)
        
        self.task_22_widget_clicked_grid.addWidget(self.task_22_text, 1, 0, 7, 0, alignment=Qt.AlignCenter)
        self.task_22_widget_clicked_grid.addWidget(self.task_22_blank, 8, 0, 9, 0)
        self.task_22_widget_clicked_grid.addWidget(self.task_22_save_button, 9, 0, 10, 0)
        self.task_22_widget.setLayout(self.task_22_widget_clicked_grid)


        #232323232323232323
        self.task_23_widget = QWidget()
        self.task_23_data = self.tasks_data[23]
        self.task_23_text = QLabel(self.task_23_data['text'])
        self.task_23_text.setWordWrap(True)
        self.task_23_text.setAlignment(Qt.AlignCenter)
        self.task_23_answer = self.task_23_data['answer']
        self.task_23_widget_clicked_grid = QGridLayout()

        self.task_23_blank = QLineEdit()
        self.task_23_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_23():
            self.user_answers[23] = self.task_23_blank.text()
            self.task_23_blank.setEnabled(False)
            self.task_23_save_button.setParent(None)
            self.task_23_widget_clicked_grid.addWidget(self.task_23_edit_button, 9, 0, 10, 0)
        def edit_task_23():
            self.task_23_blank.setEnabled(True)
            self.task_23_edit_button.setParent(None)
            self.task_23_widget_clicked_grid.addWidget(self.task_23_save_button, 9, 0, 10, 0)
        self.task_23_save_button = QPushButton(Localization.SAVE)
        self.task_23_save_button.clicked.connect(save_task_23)
        self.task_23_edit_button = QPushButton(Localization.EDIT)
        self.task_23_edit_button.clicked.connect(edit_task_23)
        
        self.task_23_widget_clicked_grid.addWidget(self.task_23_text, 1, 0, 7, 0)
        self.task_23_widget_clicked_grid.addWidget(self.task_23_blank, 8, 0, 9, 0)
        self.task_23_widget_clicked_grid.addWidget(self.task_23_save_button, 9, 0, 10, 0)
        self.task_23_widget.setLayout(self.task_23_widget_clicked_grid)


        #242424242424242424
        self.task_24_widget = QWidget()
        self.task_24_data = self.tasks_data[24]
        self.task_24_text = QLabel(self.task_24_data['text'])
        self.task_24_text.setWordWrap(True)
        self.task_24_text.setAlignment(Qt.AlignCenter)
        self.task_24_answer = self.task_24_data['answer']
        self.task_24_widget_clicked_grid = QGridLayout()

        self.task_24_blank = QLineEdit()
        self.task_24_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_24():
            self.user_answers[24] = self.task_24_blank.text()
            self.task_24_blank.setEnabled(False)
            self.task_24_save_button.setParent(None)
            self.task_24_widget_clicked_grid.addWidget(self.task_24_edit_button, 11, 0, 12, 0)
        def edit_task_24():
            self.task_24_blank.setEnabled(True)
            self.task_24_edit_button.setParent(None)
            self.task_24_widget_clicked_grid.addWidget(self.task_24_save_button, 11, 0, 12, 0)
        self.task_24_save_button = QPushButton(Localization.SAVE)
        self.task_24_save_button.clicked.connect(save_task_24)
        self.task_24_edit_button = QPushButton(Localization.EDIT)
        self.task_24_edit_button.clicked.connect(edit_task_24)

        self.task_24_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_24_file_path = 'data/tasks_data/24/' + self.task_24_data['id'] + '.txt'
        def task_24_get_file_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_24_file_path, destination_path)
            except FileNotFoundError:
                pass
        self.task_24_get_file_btn.clicked.connect(task_24_get_file_button_clicked)
        
        self.task_24_widget_clicked_grid.addWidget(self.task_24_text, 1, 0, 7, 0)
        self.task_24_widget_clicked_grid.addWidget(self.task_24_get_file_btn, 8, 0, 10, 0)
        self.task_24_widget_clicked_grid.addWidget(self.task_24_blank, 9, 0, 11, 0)
        self.task_24_widget_clicked_grid.addWidget(self.task_24_save_button, 11, 0, 12, 0)
        self.task_24_widget.setLayout(self.task_24_widget_clicked_grid)


        #252525252525252525
        self.task_25_widget = QWidget()
        self.task_25_data = self.tasks_data[25]
        self.task_25_text = QLabel(self.task_25_data['text'])
        self.task_25_text.setWordWrap(True)
        self.task_25_text.setAlignment(Qt.AlignCenter)
        self.task_25_answer = self.task_25_data['answer']
        self.task_25_widget_clicked_grid = QGridLayout()

        self.task_25_blank = QLineEdit()
        self.task_25_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_25():
            self.user_answers[25] = self.task_25_blank.text()
            self.task_25_blank.setEnabled(False)
            self.task_25_save_button.setParent(None)
            self.task_25_widget_clicked_grid.addWidget(self.task_25_edit_button, 9, 0, 10, 0)
        def edit_task_25():
            self.task_25_blank.setEnabled(True)
            self.task_25_edit_button.setParent(None)
            self.task_25_widget_clicked_grid.addWidget(self.task_25_save_button, 9, 0, 10, 0)
        self.task_25_save_button = QPushButton(Localization.SAVE)
        self.task_25_save_button.clicked.connect(save_task_25)
        self.task_25_edit_button = QPushButton(Localization.EDIT)
        self.task_25_edit_button.clicked.connect(edit_task_25)
        
        self.task_25_widget_clicked_grid.addWidget(self.task_25_text, 1, 0, 7, 0)
        self.task_25_widget_clicked_grid.addWidget(self.task_25_blank, 8, 0, 9, 0)
        self.task_25_widget_clicked_grid.addWidget(self.task_25_save_button, 9, 0, 10, 0)
        self.task_25_widget.setLayout(self.task_25_widget_clicked_grid)


        #262626262626262626
        self.task_26_widget = QWidget()
        self.task_26_data = self.tasks_data[26]
        self.task_26_text = QLabel(self.task_26_data['text'])
        self.task_26_text.setWordWrap(True)
        self.task_26_text.setAlignment(Qt.AlignCenter)
        self.task_26_answer = self.task_26_data['answer']
        self.task_26_widget_clicked_grid = QGridLayout()

        self.task_26_blank = QLineEdit()
        self.task_26_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_26():
            self.user_answers[26] = self.task_26_blank.text()
            self.task_26_blank.setEnabled(False)
            self.task_26_save_button.setParent(None)
            self.task_26_widget_clicked_grid.addWidget(self.task_26_edit_button, 11, 0, 12, 0)
        def edit_task_26():
            self.task_26_blank.setEnabled(True)
            self.task_26_edit_button.setParent(None)
            self.task_26_widget_clicked_grid.addWidget(self.task_26_save_button, 11, 0, 12, 0)
        self.task_26_save_button = QPushButton(Localization.SAVE)
        self.task_26_save_button.clicked.connect(save_task_26)
        self.task_26_edit_button = QPushButton(Localization.EDIT)
        self.task_26_edit_button.clicked.connect(edit_task_26)

        self.task_26_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_26_file_path = 'data/tasks_data/26/' + self.task_26_data['id'] + '.txt'
        def task_26_get_file_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_26_file_path, destination_path)
            except FileNotFoundError:
                pass
        self.task_26_get_file_btn.clicked.connect(task_26_get_file_button_clicked)
        
        self.task_26_widget_clicked_grid.addWidget(self.task_26_text, 1, 0, 7, 0)
        self.task_26_widget_clicked_grid.addWidget(self.task_26_get_file_btn, 8, 0, 10, 0)
        self.task_26_widget_clicked_grid.addWidget(self.task_26_blank, 9, 0, 11, 0)
        self.task_26_widget_clicked_grid.addWidget(self.task_26_save_button, 11, 0, 12, 0)
        self.task_26_widget.setLayout(self.task_26_widget_clicked_grid)


        #272727272727272727
        self.task_27_widget = QWidget()
        self.task_27_data = self.tasks_data[27]
        self.task_27_text = QLabel(self.task_27_data['text'])
        self.task_27_text.setWordWrap(True)
        self.task_27_text.setAlignment(Qt.AlignCenter)
        self.task_27_answer = self.task_27_data['answer']
        self.task_27_widget_clicked_grid = QGridLayout()

        self.task_27_blank = QLineEdit()
        self.task_27_blank.setPlaceholderText(Localization.BLANK_PLACEHOLDER)
        def save_task_27():
            self.user_answers[27] = self.task_27_blank.text()
            self.task_27_blank.setEnabled(False)
            self.task_27_save_button.setParent(None)
            self.task_27_widget_clicked_grid.addWidget(self.task_27_edit_button, 11, 0, 12, 0)
        def edit_task_27():
            self.task_27_blank.setEnabled(True)
            self.task_27_edit_button.setParent(None)
            self.task_27_widget_clicked_grid.addWidget(self.task_27_save_button, 11, 0, 12, 0)
        self.task_27_save_button = QPushButton(Localization.SAVE)
        self.task_27_save_button.clicked.connect(save_task_27)
        self.task_27_edit_button = QPushButton(Localization.EDIT)
        self.task_27_edit_button.clicked.connect(edit_task_27)

        self.task_27_get_file_a_btn = QPushButton(Localization.GET_FILE_A, self)
        self.task_27_get_file_b_btn = QPushButton(Localization.GET_FILE_B, self)
        self.task_27_file_a_path = 'data/tasks_data/27/' + self.task_27_data['id'] + '_A.txt'
        self.task_27_file_b_path = 'data/tasks_data/27/' + self.task_27_data['id'] + '_B.txt'

        def task_27_get_file_a_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_27_file_a_path, destination_path)
            except FileNotFoundError:
                pass
        self.task_27_get_file_a_btn.clicked.connect(task_27_get_file_a_button_clicked)

        def task_27_get_file_b_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_27_file_b_path, destination_path)
            except FileNotFoundError:
                pass
        self.task_27_get_file_b_btn.clicked.connect(task_27_get_file_b_button_clicked)
        
        self.task_27_widget_clicked_grid.addWidget(self.task_27_text, 1, 0, 7, 0)
        self.task_27_widget_clicked_grid.addWidget(self.task_27_get_file_a_btn, 8, 0, 9, 0)
        self.task_27_widget_clicked_grid.addWidget(self.task_27_get_file_b_btn, 9, 0, 10, 0)
        self.task_27_widget_clicked_grid.addWidget(self.task_27_blank, 10, 0, 11, 0)
        self.task_27_widget_clicked_grid.addWidget(self.task_27_save_button, 11, 0, 12, 0)
        self.task_27_widget.setLayout(self.task_27_widget_clicked_grid)

        #aft
        self.widgets_list = {
            0: self.contents_default,
            1: self.task_1_widget,
            2: self.task_2_widget,
            3: self.task_3_widget,
            4: self.task_4_widget,
            5: self.task_5_widget,
            6: self.task_6_widget,
            7: self.task_7_widget,
            8: self.task_8_widget,
            9: self.task_9_widget,
            10: self.task_10_widget,
            11: self.task_11_widget,
            12: self.task_12_widget,
            13: self.task_13_widget,
            14: self.task_14_widget,
            15: self.task_15_widget,
            16: self.task_16_widget,
            17: self.task_17_widget,
            18: self.task_18_widget,
            19: self.task_19_widget,
            20: self.task_20_widget,
            21: self.task_21_widget,
            22: self.task_22_widget,
            23: self.task_23_widget,
            24: self.task_24_widget,
            25: self.task_25_widget,
            26: self.task_26_widget,
            27: self.task_27_widget
        }
        for key in self.widgets_list:
            self.contents_tasks.addWidget(self.widgets_list[key])

        def btn_clicked(button_num):
            try:
                if self.timer_isnt_started and not self.timer_has_ended:
                    self.timerSetup()
                try:
                    self.email_btn.setParent(None)
                    if not self.user_finished:
                        self.finish_btn = QPushButton(Localization.FINISH)
                    else:
                        self.finish_btn = QPushButton(Localization.SHOW_RESULTS)
                    self.finish_btn.clicked.connect(self.finish)
                    self.centralLayout.addWidget(self.finish_btn, 3, 0, 4, 3)
                except:
                    pass
                self.contents_tasks.setCurrentIndex(button_num)
            except KeyError:
                pass

        def buttons_set(num):
            self.buttons_list[num].clicked.connect(lambda: btn_clicked(num))
        for num in range(1, 28):
            buttons_set(num)

        self.contents_tasks.setCurrentIndex(0)
        self.scrollArea_nums = QScrollArea()
        self.scrollArea_nums.setWidgetResizable(True)
        self.scrollArea_nums.setWidget(self.contents_nums)

        self.scrollArea_tasks = QScrollArea()
        self.scrollArea_tasks.setWidgetResizable(True)
        self.scrollArea_tasks.setWidget(self.contents_tasks)

        self.finish_btn = QPushButton(Localization.FINISH)
        self.finish_btn.clicked.connect(self.finish)
        self.save_var_btn = QPushButton(Localization.SAVE_VAR)
        self.save_var_btn.clicked.connect(self.save_var_clicked)

        self.centralLayout.addWidget(self.scrollArea_tasks, 0, 0, 1, 1)
        self.centralLayout.addWidget(self.scrollArea_nums, 0, 2, 1, 12)
        self.centralLayout.addWidget(self.timer_text_lbl, 1, 0, 2, 12)
        self.centralLayout.addWidget(self.finish_btn, 3, 0, 4, 3)
        self.centralLayout.addWidget(self.save_var_btn, 3, 4, 4, 12)
        self.centralWidget.setLayout(self.centralLayout)
        self.setCentralWidget(self.centralWidget)

    def save_var_clicked(self):
        if not self.var_saved and not self.by_id:
            self.var_saved = True
            self.saved_var_id = ID_Vars.save_var(self.tasks_data)
            QMessageBox.information(self, Localization.EMAIL_SUCCESS_HEADER, Localization.BYID_SUCCESS_TEXT % self.saved_var_id, QMessageBox.Ok)
        elif self.by_id:
            QMessageBox.information(self, Localization.BYID_INFO_HEADER, Localization.BYID_SUCCESS_TEXT_LOADED % self.var_id, QMessageBox.Ok)
        else:
            QMessageBox.information(self, Localization.BYID_INFO_HEADER, Localization.BYID_SUCCESS_TEXT_ALREADY_SAVED % self.saved_var_id, QMessageBox.Ok)

    def finish(self):
        self.user_finished = True
        self.finish_time = Config.getCurrentTimeAsStr()
        self.start = False
        self.timer_has_ended = True
        if self.timer_text_lbl.text() != Localization.TIMER_TEXT_TIME_EXPIRED:
            self.timer_text_lbl.setText(Localization.TIMER_TEXT_USER_FINISH)

        self.finish_btn.setParent(None)
        self.email_btn = QPushButton(Localization.EMAIL_BUTTON)
        self.email_btn.clicked.connect(self.emailAction)
        self.centralLayout.addWidget(self.email_btn, 3, 0, 4, 3)

        for task in range(1, 28):
            self.finish_btn.setText(Localization.SHOW_RESULTS)
            button_name_1 = 'task_' + str(task) + '_save_button'
            button_name_2 = 'task_' + str(task) + '_edit_button'
            blank_name = 'task_' + str(task) + '_blank'
            self.__dict__[button_name_1].setParent(None)
            self.__dict__[button_name_2].setParent(None)
            self.__dict__[blank_name].setEnabled(False)

        self.results_contents = QWidget()
        self.widgets_list[28] = self.results_contents
        self.contents_tasks.addWidget(self.widgets_list[28])
        self.results_grid_clicked = QGridLayout()

        task_num = 1
        for column in range(1, 4):
            for task in range(task_num, task_num + 9):
                correct_text = Localization.CORRECT if self.user_answers[task] == self.tasks_data[task]['answer'] else Localization.INCORRECT
                header_text = Localization.RESULTS_HEADER_TEXT % (task, correct_text)
                user_text = Localization.YOUR_ANSWER % self.user_answers[task] if not self.user_answers[task] is None else Localization.NO_ANSWER
                descr_text = Localization.CORRECT_ANSWER % self.tasks_data[task]['answer']
                lbl = QLabel(header_text + '\n' + user_text + '\n' + descr_text)
                row = task
                if 10 <= row <= 18:
                    row = row - 9
                elif row >= 19:
                    row = row - 18
                row = row - 1
                self.results_grid_clicked.addWidget(lbl, row, column)
            task_num = task_num + 9

        self.user_results = [None]
        for task in range(1, 28):
            if self.user_answers[task] == self.tasks_data[task]['answer']:
                self.user_results.append(True)
            else:
                self.user_results.append(False)
        self.number_of_completed_tasks = self.user_results.count(True)
        self.result_text = Localization.RESULT % self.number_of_completed_tasks

        self.first_points = 0
        for ind in range(1, 28):
            if self.user_results[ind] and ind < 26:
                self.first_points = self.first_points + 1
            elif self.user_results[ind] and 26 <= ind <= 27:
                self.first_points = self.first_points + 2
        self.total_points = int(Config.POINTS[str(self.first_points)])
        self.points_form = Config.getPointsForm(self.first_points)
        self.result_points_text = Localization.RESULT_IN_POINTS % (self.first_points, self.points_form, self.total_points)
        self.result_text = self.result_text + '\n' + self.result_points_text

        self.res_lbl = QLabel(self.result_text)
        self.results_grid_clicked.addWidget(self.res_lbl, 9, 1, 10, 3, alignment=Qt.AlignCenter)
        
        self.results_contents.setLayout(self.results_grid_clicked)
        self.contents_tasks.setCurrentIndex(28)
    
    def emailAction(self):
        self.email_text, self.ok = QInputDialog.getText(self, Localization.EMAIL_ASK_HEADER,
            Localization.EMAIL_ASK_TEXT, flags=Qt.WindowCloseButtonHint)
        if Config.checkInternetConnection():
            if self.ok:
                self.result_file_content_writeable = self.generateResultFileContent()
                self.generateResultFile(self.result_file_content_writeable)
                self.email = self.email_text
                self.email_sent = Email.send_message(self.email)
                if not self.email_sent[0]:
                    Logger.add_line_to_log("Error sending Email. Code: 0. Cause: %s." % self.email_sent[1])
                    QMessageBox.critical(self, Localization.EMAIL_ERROR_HEADER, Localization.EMAIL_ERROR_0, QMessageBox.Ok)
                else:
                    Logger.add_line_to_log("Succesfully sent Email to %s." % self.email)
                    QMessageBox.information(self, Localization.EMAIL_SUCCESS_HEADER, Localization.EMAIL_SUCCESS_TEXT, QMessageBox.Ok)
                self.deleteResultFile()
            else:
                QMessageBox.critical(self, Localization.EMAIL_ERROR_HEADER, Localization.EMAIL_ERROR_1, QMessageBox.Ok)
        else:
            Logger.add_line_to_log("Error initializing Email module. Code: 2. Cause: no Internet access.")
            QMessageBox.critical(self, Localization.EMAIL_ERROR_HEADER, Localization.EMAIL_ERROR_2, QMessageBox.Ok)

    def generateResultFileContent(self):
        self.result_datetime_line = Localization.EMAIL_DATETIME_LINE + self.finish_time + '.\n'
        self.result_res_line = self.result_text + '\n'
        self.result_tasks_line = '\n'
        textltask = 1
        for elem in self.user_results[1:]:
            textlcorrect = Localization.EMAIL_CORRECT if elem else Localization.EMAIL_INCORRECT
            textl = Localization.EMAIL_TASK_TEXT % textltask + textlcorrect + '.'
            textltask += 1
            self.result_tasks_line = self.result_tasks_line + textl + '\n'
        self.result_file_content = self.result_datetime_line + self.result_res_line + self.result_tasks_line
        return self.result_file_content
    
    def generateResultFile(self, content):
        self.result_file_path = '%s/INFA100/result.txt' %  os.environ['APPDATA']
        with open(self.result_file_path, 'w', encoding='utf-8') as email_file:
            email_file.write(content)

    def deleteResultFile(self):
        if os.path.exists(self.result_file_path):
            os.remove(self.result_file_path)