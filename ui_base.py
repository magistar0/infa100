import os
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap

from task_manager import Task_Chooser
from data_manager import Localization
import save_manager


class UI_BaseWindow(object):
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
        self.statusBar()

        self.menubar_var = self.menuBar()
        self.fileMenu_var = self.menubar_var.addMenu('&' + Localization.FILE)
        self.fileMenu_var.addAction(self.exitAction_var)

        self.lbl = QLabel(Localization.CHOOSE_TASK, self)
        self.show_btn = QPushButton(Localization.SHOW, self)
        self.show_btn.clicked.connect(self.show_btn_clicked)

        self.centralWidget = QWidget()
        self.combo = QComboBox()
        self.list_of_items = [Localization.TASK + str(num) for num in range(1, 28)]
        self.combo.addItems(self.list_of_items)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.lbl, 1, 0, alignment=Qt.AlignCenter)
        grid.addWidget(self.combo, 2, 0, 4, 0)
        grid.addWidget(self.show_btn, 3, 0, 5, 0)
        
        self.centralWidget.setLayout(grid)
        self.setCentralWidget(self.centralWidget)

    def show_btn_clicked(self):
        task_num = self.combo.currentText().replace(Localization.TASK, '')

        self.lbl2 = QLabel(Localization.TASK_HEADER % task_num, self)
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
        task_1_widget_clicked_grid = QGridLayout()

        self.task_1_picture_path = 'data/tasks_data/1/' + self.task_1_data['id'] + '.png'
        self.task_1_picture_exists = True if os.path.exists(self.task_1_picture_path) else False
        if self.task_1_picture_exists:
            self.task_1_picture = QPixmap(self.task_1_picture_path)
            self.task_1_picture_lbl = QLabel(self)
            self.task_1_picture_lbl.setPixmap(self.task_1_picture)
        
        task_1_widget_clicked_grid.addWidget(self.task_1_text, 1, 0, 7, 0)
        if self.task_1_picture_exists:
            task_1_widget_clicked_grid.addWidget(self.task_1_picture_lbl, 10, 0, 12, 0, alignment=Qt.AlignCenter)
        task_1_widget_clicked_grid.addWidget(self.task_1_show_ans_btn, 25, 0, 27, 0)
        task_1_widget_clicked_grid.addWidget(self.task_1_show_descr_btn, 55, 0, 63, 0)
        self.task_1_widget.setLayout(task_1_widget_clicked_grid)

        def task_1_ans_button_clicked():
            self.task_1_show_ans_btn.setParent(None)
            task_1_widget_clicked_grid.addWidget(self.task_1_answer, 25, 0, 27, 0)
        def task_1_descr_button_clicked():
            self.task_1_show_descr_btn.setParent(None)
            task_1_widget_clicked_grid.addWidget(self.task_1_description_widget, 55, 0, 63, 0)

        self.task_1_show_ans_btn.clicked.connect(task_1_ans_button_clicked)
        self.task_1_show_descr_btn.clicked.connect(task_1_descr_button_clicked)


        # 222222222
        self.task_2_widget = QWidget()
        self.task_2_data = Task_Chooser.choose_task(2)
        self.task_2_text = QLabel(self.task_2_data['text'])
        self.task_2_text.setWordWrap(True)
        self.task_2_text.setAlignment(Qt.AlignCenter)
        self.task_2_answer = QLabel('Ответ: ' + self.task_2_data['answer'])
        self.task_2_answer.setWordWrap(True)
        self.task_2_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_2_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_2_description = self.task_2_data['description']
        self.task_2_description_widget = QLabel(self.task_2_description)
        self.task_2_description_widget.setWordWrap(True)
        task_2_widget_clicked_grid = QGridLayout()

        self.task_2_picture_path = 'data/tasks_data/2/' + self.task_2_data['id'] + '.png'
        self.task_2_picture_exists = True if os.path.exists(self.task_2_picture_path) else False
        if self.task_2_picture_exists:
            self.task_2_picture = QPixmap(self.task_2_picture_path)
            self.task_2_picture_lbl = QLabel(self)
            self.task_2_picture_lbl.setPixmap(self.task_2_picture)
        
        task_2_widget_clicked_grid.addWidget(self.task_2_text, 1, 0, 7, 0)
        if self.task_2_picture_exists:
            task_2_widget_clicked_grid.addWidget(self.task_2_picture_lbl, 10, 0, 12, 0, alignment=Qt.AlignCenter)
        task_2_widget_clicked_grid.addWidget(self.task_2_show_ans_btn, 25, 0, 27, 0)
        task_2_widget_clicked_grid.addWidget(self.task_2_show_descr_btn, 55, 0, 63, 0)
        self.task_2_widget.setLayout(task_2_widget_clicked_grid)

        def task_2_ans_button_clicked():
            self.task_2_show_ans_btn.setParent(None)
            task_2_widget_clicked_grid.addWidget(self.task_2_answer, 25, 0, 27, 0)
        def task_2_descr_button_clicked():
            self.task_2_show_descr_btn.setParent(None)
            task_2_widget_clicked_grid.addWidget(self.task_2_description_widget, 55, 0, 63, 0)

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

        self.task_3_answer = QLabel('Ответ: ' + self.task_3_data['answer'])
        self.task_3_answer.setWordWrap(True)
        self.task_3_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_3_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_3_description = self.task_3_data['description']
        self.task_3_description_widget = QLabel(self.task_3_description)
        self.task_3_description_widget.setWordWrap(True)
        task_3_widget_clicked_grid = QGridLayout()

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
        
        task_3_widget_clicked_grid.addWidget(self.task_3_text1, 0, 0, 1, 0)
        task_3_widget_clicked_grid.addWidget(self.task_3_get_file_btn, 2, 0, 3, 0)
        task_3_widget_clicked_grid.addWidget(self.task_3_text2, 4, 0, 6, 0)
        task_3_widget_clicked_grid.addWidget(self.task_3_picture_2to3_lbl, 9, 0, 11, 0, alignment=Qt.AlignCenter)
        task_3_widget_clicked_grid.addWidget(self.task_3_text3, 15, 0, 16, 0)
        task_3_widget_clicked_grid.addWidget(self.task_3_picture_3to4_lbl, 25, 0, 27, 0, alignment=Qt.AlignCenter)
        task_3_widget_clicked_grid.addWidget(self.task_3_text4, 39, 0, 41, 0)
        task_3_widget_clicked_grid.addWidget(self.task_3_picture_4to5_lbl, 62, 0, 64, 0, alignment=Qt.AlignCenter)
        task_3_widget_clicked_grid.addWidget(self.task_3_text5, 86, 0, 87, 0)
        task_3_widget_clicked_grid.addWidget(self.task_3_picture_5to6_lbl, 166, 0, 168, 0, alignment=Qt.AlignCenter)
        task_3_widget_clicked_grid.addWidget(self.task_3_text6, 330, 0, 332, 0)
        task_3_widget_clicked_grid.addWidget(self.task_3_show_ans_btn, 650, 0, 652, 0)
        task_3_widget_clicked_grid.addWidget(self.task_3_show_descr_btn, 1400, 0, 1407, 0)
        self.task_3_widget.setLayout(task_3_widget_clicked_grid)

        def task_3_ans_button_clicked():
            self.task_3_show_ans_btn.setParent(None)
            task_3_widget_clicked_grid.addWidget(self.task_3_answer, 650, 0, 652, 0)
        def task_3_descr_button_clicked():
            self.task_3_show_descr_btn.setParent(None)
            task_3_widget_clicked_grid.addWidget(self.task_3_description_widget, 1400, 0, 1407, 0)
        def task_3_get_file_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_3_file_path, destination_path)
            except FileNotFoundError:
                pass

        self.task_3_show_ans_btn.clicked.connect(task_3_ans_button_clicked)
        self.task_3_show_descr_btn.clicked.connect(task_3_descr_button_clicked)
        self.task_3_get_file_btn.clicked.connect(task_3_get_file_button_clicked)


        # 4444444444
        self.task_4_widget = QWidget()
        self.task_4_data = Task_Chooser.choose_task(4)
        self.task_4_text = QLabel(self.task_4_data['text'])
        self.task_4_text.setWordWrap(True)
        self.task_4_text.setAlignment(Qt.AlignCenter)
        self.task_4_answer = QLabel('Ответ: ' + self.task_4_data['answer'])
        self.task_4_answer.setWordWrap(True)
        self.task_4_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_4_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_4_description = self.task_4_data['description']
        self.task_4_description_widget = QLabel(self.task_4_description)
        self.task_4_description_widget.setWordWrap(True)
        task_4_widget_clicked_grid = QGridLayout()
        
        task_4_widget_clicked_grid.addWidget(self.task_4_text, 1, 0, 7, 0)
        task_4_widget_clicked_grid.addWidget(self.task_4_show_ans_btn, 10, 0, 12, 0)
        task_4_widget_clicked_grid.addWidget(self.task_4_show_descr_btn, 25, 0, 33, 0)
        self.task_4_widget.setLayout(task_4_widget_clicked_grid)

        def task_4_ans_button_clicked():
            self.task_4_show_ans_btn.setParent(None)
            task_4_widget_clicked_grid.addWidget(self.task_4_answer, 10, 0, 12, 0)
        def task_4_descr_button_clicked():
            self.task_4_show_descr_btn.setParent(None)
            task_4_widget_clicked_grid.addWidget(self.task_4_description_widget, 25, 0, 33, 0)

        self.task_4_show_ans_btn.clicked.connect(task_4_ans_button_clicked)
        self.task_4_show_descr_btn.clicked.connect(task_4_descr_button_clicked)


        # 5555555555
        self.task_5_widget = QWidget()
        self.task_5_data = Task_Chooser.choose_task(5)
        self.task_5_text = QLabel(self.task_5_data['text'])
        self.task_5_text.setWordWrap(True)
        self.task_5_text.setAlignment(Qt.AlignCenter)
        self.task_5_answer = QLabel('Ответ: ' + self.task_5_data['answer'])
        self.task_5_answer.setWordWrap(True)
        self.task_5_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_5_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_5_description = self.task_5_data['description']
        self.task_5_description_widget = QLabel(self.task_5_description)
        self.task_5_description_widget.setWordWrap(True)
        task_5_widget_clicked_grid = QGridLayout()
        
        task_5_widget_clicked_grid.addWidget(self.task_5_text, 1, 0, 7, 0)
        task_5_widget_clicked_grid.addWidget(self.task_5_show_ans_btn, 10, 0, 12, 0)
        task_5_widget_clicked_grid.addWidget(self.task_5_show_descr_btn, 25, 0, 33, 0)
        self.task_5_widget.setLayout(task_5_widget_clicked_grid)

        def task_5_ans_button_clicked():
            self.task_5_show_ans_btn.setParent(None)
            task_5_widget_clicked_grid.addWidget(self.task_5_answer, 10, 0, 12, 0)
        def task_5_descr_button_clicked():
            self.task_5_show_descr_btn.setParent(None)
            task_5_widget_clicked_grid.addWidget(self.task_5_description_widget, 25, 0, 33, 0)

        self.task_5_show_ans_btn.clicked.connect(task_5_ans_button_clicked)
        self.task_5_show_descr_btn.clicked.connect(task_5_descr_button_clicked)


        # 66666666
        self.task_6_widget = QWidget()
        self.task_6_data = Task_Chooser.choose_task(6)
        self.task_6_text = QLabel(self.task_6_data['text'] + '\n\n' + self.task_6_data['program'])
        self.task_6_text.setWordWrap(True)
        self.task_6_answer = QLabel('Ответ: ' + self.task_6_data['answer'])
        self.task_6_answer.setWordWrap(True)
        self.task_6_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_6_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_6_description = self.task_6_data['description']
        if self.task_6_data['python'].strip() != 'нет':
            self.task_6_description = self.task_6_description + '\n\n' + self.task_6_data['python']
        self.task_6_description_widget = QLabel(self.task_6_description)
        self.task_6_description_widget.setWordWrap(True)
        task_6_widget_clicked_grid = QGridLayout()
        
        task_6_widget_clicked_grid.addWidget(self.task_6_text, 1, 0, 7, 0, alignment=Qt.AlignCenter)
        task_6_widget_clicked_grid.addWidget(self.task_6_show_ans_btn, 10, 0, 12, 0)
        task_6_widget_clicked_grid.addWidget(self.task_6_show_descr_btn, 25, 0, 33, 0)
        self.task_6_widget.setLayout(task_6_widget_clicked_grid)

        def task_6_ans_button_clicked():
            self.task_6_show_ans_btn.setParent(None)
            task_6_widget_clicked_grid.addWidget(self.task_6_answer, 10, 0, 12, 0)
        def task_6_descr_button_clicked():
            self.task_6_show_descr_btn.setParent(None)
            task_6_widget_clicked_grid.addWidget(self.task_6_description_widget, 25, 0, 33, 0)

        self.task_6_show_ans_btn.clicked.connect(task_6_ans_button_clicked)
        self.task_6_show_descr_btn.clicked.connect(task_6_descr_button_clicked)


        # 7777777777
        self.task_7_widget = QWidget()
        self.task_7_data = Task_Chooser.choose_task(7)
        self.task_7_text = QLabel(self.task_7_data['text'])
        self.task_7_text.setWordWrap(True)
        self.task_7_text.setAlignment(Qt.AlignCenter)
        self.task_7_answer = QLabel('Ответ: ' + self.task_7_data['answer'])
        self.task_7_answer.setWordWrap(True)
        self.task_7_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_7_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_7_description = self.task_7_data['description']
        self.task_7_description_widget = QLabel(self.task_7_description)
        self.task_7_description_widget.setWordWrap(True)
        task_7_widget_clicked_grid = QGridLayout()
        
        task_7_widget_clicked_grid.addWidget(self.task_7_text, 1, 0, 7, 0)
        task_7_widget_clicked_grid.addWidget(self.task_7_show_ans_btn, 10, 0, 12, 0)
        task_7_widget_clicked_grid.addWidget(self.task_7_show_descr_btn, 27, 0, 33, 0)
        self.task_7_widget.setLayout(task_7_widget_clicked_grid)

        def task_7_ans_button_clicked():
            self.task_7_show_ans_btn.setParent(None)
            task_7_widget_clicked_grid.addWidget(self.task_7_answer, 10, 0, 12, 0)
        def task_7_descr_button_clicked():
            self.task_7_show_descr_btn.setParent(None)
            task_7_widget_clicked_grid.addWidget(self.task_7_description_widget, 27, 0, 33, 0)

        self.task_7_show_ans_btn.clicked.connect(task_7_ans_button_clicked)
        self.task_7_show_descr_btn.clicked.connect(task_7_descr_button_clicked)


        # 88888888888888
        self.task_8_widget = QWidget()
        self.task_8_data = Task_Chooser.choose_task(8)
        self.task_8_text = QLabel(self.task_8_data['text'])
        self.task_8_text.setWordWrap(True)
        self.task_8_text.setAlignment(Qt.AlignCenter)
        self.task_8_answer = QLabel('Ответ: ' + self.task_8_data['answer'])
        self.task_8_answer.setWordWrap(True)
        self.task_8_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_8_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_8_description = self.task_8_data['description']
        if self.task_8_data['python'].strip() != 'нет':
            self.task_8_description = self.task_8_description + '\n\n' + self.task_8_data['python']
        self.task_8_description_widget = QLabel(self.task_8_description)
        self.task_8_description_widget.setWordWrap(True)
        task_8_widget_clicked_grid = QGridLayout()
        
        task_8_widget_clicked_grid.addWidget(self.task_8_text, 1, 0, 7, 0)
        task_8_widget_clicked_grid.addWidget(self.task_8_show_ans_btn, 10, 0, 12, 0)
        task_8_widget_clicked_grid.addWidget(self.task_8_show_descr_btn, 25, 0, 33, 0)
        self.task_8_widget.setLayout(task_8_widget_clicked_grid)

        def task_8_ans_button_clicked():
            self.task_8_show_ans_btn.setParent(None)
            task_8_widget_clicked_grid.addWidget(self.task_8_answer, 10, 0, 12, 0)
        def task_8_descr_button_clicked():
            self.task_8_show_descr_btn.setParent(None)
            task_8_widget_clicked_grid.addWidget(self.task_8_description_widget, 25, 0, 33, 0)

        self.task_8_show_ans_btn.clicked.connect(task_8_ans_button_clicked)
        self.task_8_show_descr_btn.clicked.connect(task_8_descr_button_clicked)


        # 9999999999
        self.task_9_widget = QWidget()
        self.task_9_data = Task_Chooser.choose_task(9)
        self.task_9_text = QLabel(self.task_9_data['text'])
        self.task_9_text.setWordWrap(True)
        self.task_9_text.setAlignment(Qt.AlignCenter)
        self.task_9_answer = QLabel('Ответ: ' + self.task_9_data['answer'])
        self.task_9_answer.setWordWrap(True)
        self.task_9_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_9_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_9_description = self.task_9_data['description']
        self.task_9_description_widget = QLabel(self.task_9_description)
        self.task_9_description_widget.setWordWrap(True)
        task_9_widget_clicked_grid = QGridLayout()

        self.task_9_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_9_file_path = 'data/tasks_data/9/' + self.task_9_data['id'] + '.xlsx'
        
        task_9_widget_clicked_grid.addWidget(self.task_9_text, 1, 0, 9, 0)
        task_9_widget_clicked_grid.addWidget(self.task_9_get_file_btn, 10, 0, 12, 0)
        task_9_widget_clicked_grid.addWidget(self.task_9_show_ans_btn, 29, 0, 33, 0)
        task_9_widget_clicked_grid.addWidget(self.task_9_show_descr_btn, 70, 0, 74, 0)
        self.task_9_widget.setLayout(task_9_widget_clicked_grid)

        def task_9_ans_button_clicked():
            self.task_9_show_ans_btn.setParent(None)
            task_9_widget_clicked_grid.addWidget(self.task_9_answer, 29, 0, 33, 0)
        def task_9_descr_button_clicked():
            self.task_9_show_descr_btn.setParent(None)
            task_9_widget_clicked_grid.addWidget(self.task_9_description_widget, 70, 0, 74, 0)
        def task_9_get_file_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_9_file_path, destination_path)
            except FileNotFoundError:
                pass

        self.task_9_show_ans_btn.clicked.connect(task_9_ans_button_clicked)
        self.task_9_show_descr_btn.clicked.connect(task_9_descr_button_clicked)
        self.task_9_get_file_btn.clicked.connect(task_9_get_file_button_clicked)


        # 10101010101010101010
        self.task_10_widget = QWidget()
        self.task_10_data = Task_Chooser.choose_task(10)
        self.task_10_text = QLabel(self.task_10_data['text'])
        self.task_10_text.setWordWrap(True)
        self.task_10_text.setAlignment(Qt.AlignCenter)
        self.task_10_answer = QLabel('Ответ: ' + self.task_10_data['answer'])
        self.task_10_answer.setWordWrap(True)
        self.task_10_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_10_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_10_description = self.task_10_data['description']
        self.task_10_description_widget = QLabel(self.task_10_description)
        self.task_10_description_widget.setWordWrap(True)
        task_10_widget_clicked_grid = QGridLayout()

        self.task_10_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_10_file_path = 'data/tasks_data/10/' + self.task_10_data['id'] + '.docx'
        
        task_10_widget_clicked_grid.addWidget(self.task_10_text, 1, 0, 9, 0)
        task_10_widget_clicked_grid.addWidget(self.task_10_get_file_btn, 10, 0, 12, 0)
        task_10_widget_clicked_grid.addWidget(self.task_10_show_ans_btn, 29, 0, 33, 0)
        task_10_widget_clicked_grid.addWidget(self.task_10_show_descr_btn, 60, 0, 64, 0)
        self.task_10_widget.setLayout(task_10_widget_clicked_grid)

        def task_10_ans_button_clicked():
            self.task_10_show_ans_btn.setParent(None)
            task_10_widget_clicked_grid.addWidget(self.task_10_answer, 29, 0, 33, 0)
        def task_10_descr_button_clicked():
            self.task_10_show_descr_btn.setParent(None)
            task_10_widget_clicked_grid.addWidget(self.task_10_description_widget, 60, 0, 64, 0)
        def task_10_get_file_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_10_file_path, destination_path)
            except FileNotFoundError:
                pass

        self.task_10_show_ans_btn.clicked.connect(task_10_ans_button_clicked)
        self.task_10_show_descr_btn.clicked.connect(task_10_descr_button_clicked)
        self.task_10_get_file_btn.clicked.connect(task_10_get_file_button_clicked)


        # 11111111111111111111
        self.task_11_widget = QWidget()
        self.task_11_data = Task_Chooser.choose_task(11)
        self.task_11_text = QLabel(self.task_11_data['text'])
        self.task_11_text.setWordWrap(True)
        self.task_11_text.setAlignment(Qt.AlignCenter)
        self.task_11_answer = QLabel('Ответ: ' + self.task_11_data['answer'])
        self.task_11_answer.setWordWrap(True)
        self.task_11_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_11_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_11_description = self.task_11_data['description']
        self.task_11_description_widget = QLabel(self.task_11_description)
        self.task_11_description_widget.setWordWrap(True)
        task_11_widget_clicked_grid = QGridLayout()
        
        task_11_widget_clicked_grid.addWidget(self.task_11_text, 1, 0, 7, 0)
        task_11_widget_clicked_grid.addWidget(self.task_11_show_ans_btn, 10, 0, 12, 0)
        task_11_widget_clicked_grid.addWidget(self.task_11_show_descr_btn, 27, 0, 33, 0)
        self.task_11_widget.setLayout(task_11_widget_clicked_grid)

        def task_11_ans_button_clicked():
            self.task_11_show_ans_btn.setParent(None)
            task_11_widget_clicked_grid.addWidget(self.task_11_answer, 10, 0, 12, 0)
        def task_11_descr_button_clicked():
            self.task_11_show_descr_btn.setParent(None)
            task_11_widget_clicked_grid.addWidget(self.task_11_description_widget, 27, 0, 33, 0)

        self.task_11_show_ans_btn.clicked.connect(task_11_ans_button_clicked)
        self.task_11_show_descr_btn.clicked.connect(task_11_descr_button_clicked)


        # 12121212121212121212
        self.task_12_widget = QWidget()
        self.task_12_data = Task_Chooser.choose_task(12)
        self.task_12_text = QLabel(self.task_12_data['text'])
        self.task_12_text.setWordWrap(True)
        self.task_12_answer = QLabel('Ответ: ' + self.task_12_data['answer'])
        self.task_12_answer.setWordWrap(True)
        self.task_12_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_12_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_12_description = self.task_12_data['description']
        if self.task_12_data['python'].strip() != 'нет':
            self.task_12_description = self.task_12_description + '\n\n' + self.task_12_data['python']
        self.task_12_description_widget = QLabel(self.task_12_description)
        self.task_12_description_widget.setWordWrap(True)
        task_12_widget_clicked_grid = QGridLayout()

        if self.task_12_data['hasPictures'] == True:
            self.task_12_picture_path = 'data/tasks_data/12/' + self.task_12_data['id'] + '.png'
            self.task_12_picture_exists = True if os.path.exists(self.task_12_picture_path) else False
            if self.task_12_picture_exists:
                self.task_12_picture = QPixmap(self.task_12_picture_path)
                self.task_12_picture_lbl = QLabel(self)
                self.task_12_picture_lbl.setPixmap(self.task_12_picture)

            self.task_12_ans_picture_path = 'data/tasks_data/12/' + self.task_12_data['id'] + '_ans.png'
            self.task_12_ans_picture_exists = True if os.path.exists(self.task_12_ans_picture_path) else False
            if self.task_12_ans_picture_exists:
                self.task_12_ans_picture = QPixmap(self.task_12_ans_picture_path)
                self.task_12_ans_picture_lbl = QLabel(self)
                self.task_12_ans_picture_lbl.setPixmap(self.task_12_ans_picture)

        def task_12_ans_button_clicked():
            self.task_12_show_ans_btn.setParent(None)
            task_12_widget_clicked_grid.addWidget(self.task_12_answer, 18, 0, 20, 0)
        def task_12_descr_button_clicked_has_pictures_false():
            self.task_12_show_descr_btn.setParent(None)
            task_12_widget_clicked_grid.addWidget(self.task_12_description_widget, 40, 0, 46, 0)
        def task_12_descr_button_clicked_has_pictures_true():
            self.task_12_show_descr_btn.setParent(None)
            task_12_widget_clicked_grid.addWidget(self.task_12_ans_picture_lbl, 25, 0, 46, 1)
            task_12_widget_clicked_grid.addWidget(self.task_12_description_widget, 25, 2, 46, 9)

        if self.task_12_data['hasPictures'] == False:
            task_12_widget_clicked_grid.addWidget(self.task_12_text, 1, 0, 15, 0)
            task_12_widget_clicked_grid.addWidget(self.task_12_show_ans_btn, 18, 0, 20, 0)
            task_12_widget_clicked_grid.addWidget(self.task_12_show_descr_btn, 40, 0, 46, 0)
            self.task_12_widget.setLayout(task_12_widget_clicked_grid)
            self.task_12_show_ans_btn.clicked.connect(task_12_ans_button_clicked)
            self.task_12_show_descr_btn.clicked.connect(task_12_descr_button_clicked_has_pictures_false)
        elif self.task_12_data['hasPictures'] == True:
            task_12_widget_clicked_grid.addWidget(self.task_12_picture_lbl, 1, 0, 15, 1)
            task_12_widget_clicked_grid.addWidget(self.task_12_text, 1, 2, 15, 9)
            task_12_widget_clicked_grid.addWidget(self.task_12_show_ans_btn, 18, 0, 20, 0)
            task_12_widget_clicked_grid.addWidget(self.task_12_show_descr_btn, 40, 0, 46, 0)
            self.task_12_widget.setLayout(task_12_widget_clicked_grid)
            self.task_12_show_ans_btn.clicked.connect(task_12_ans_button_clicked)
            self.task_12_show_descr_btn.clicked.connect(task_12_descr_button_clicked_has_pictures_true)


        # 13131313131313131313
        self.task_13_widget = QWidget()
        self.task_13_data = Task_Chooser.choose_task(13)
        self.task_13_text = QLabel(self.task_13_data['text'])
        self.task_13_text.setWordWrap(True)
        self.task_13_text.setAlignment(Qt.AlignCenter)
        self.task_13_answer = QLabel('Ответ: ' + self.task_13_data['answer'])
        self.task_13_answer.setWordWrap(True)
        self.task_13_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_13_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_13_description = self.task_13_data['description']
        self.task_13_description_widget = QLabel(self.task_13_description)
        self.task_13_description_widget.setWordWrap(True)
        task_13_widget_clicked_grid = QGridLayout()

        self.task_13_text_widgth = self.task_13_text.frameGeometry().width()
        self.task_13_text_height = self.task_13_text.frameGeometry().height()

        self.task_13_picture_path = 'data/tasks_data/13/' + self.task_13_data['id'] + '.png'
        self.task_13_picture_exists = True if os.path.exists(self.task_13_picture_path) else False
        if self.task_13_picture_exists:
            self.task_13_picture = QPixmap(self.task_13_picture_path)
            self.task_13_picture = self.task_13_picture.scaled(self.task_13_text_widgth, self.task_13_text_height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.task_13_picture_lbl = QLabel(self)
            self.task_13_picture_lbl.setPixmap(self.task_13_picture)
        
        task_13_widget_clicked_grid.addWidget(self.task_13_text, 1, 0, 7, 0)
        if self.task_13_picture_exists:
            task_13_widget_clicked_grid.addWidget(self.task_13_picture_lbl, 10, 0, 12, 0, alignment=Qt.AlignCenter)
        task_13_widget_clicked_grid.addWidget(self.task_13_show_ans_btn, 25, 0, 27, 0)
        task_13_widget_clicked_grid.addWidget(self.task_13_show_descr_btn, 55, 0, 63, 0)
        self.task_13_widget.setLayout(task_13_widget_clicked_grid)

        def task_13_ans_button_clicked():
            self.task_13_show_ans_btn.setParent(None)
            task_13_widget_clicked_grid.addWidget(self.task_13_answer, 25, 0, 27, 0)
        def task_13_descr_button_clicked():
            self.task_13_show_descr_btn.setParent(None)
            task_13_widget_clicked_grid.addWidget(self.task_13_description_widget, 55, 0, 63, 0)

        self.task_13_show_ans_btn.clicked.connect(task_13_ans_button_clicked)
        self.task_13_show_descr_btn.clicked.connect(task_13_descr_button_clicked)


        # 1414141414141414141414141414
        self.task_14_widget = QWidget()
        self.task_14_data = Task_Chooser.choose_task(14)
        self.task_14_text = QLabel(self.task_14_data['text'])
        self.task_14_text.setWordWrap(True)
        self.task_14_text.setAlignment(Qt.AlignCenter)
        self.task_14_answer = QLabel('Ответ: ' + self.task_14_data['answer'])
        self.task_14_answer.setWordWrap(True)
        self.task_14_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_14_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_14_description = self.task_14_data['description']
        if self.task_14_data['python'].strip() != 'нет':
            self.task_14_description = self.task_14_description + '\n\n' + self.task_14_data['python']
        self.task_14_description_widget = QLabel(self.task_14_description)
        self.task_14_description_widget.setWordWrap(True)
        task_14_widget_clicked_grid = QGridLayout()
        
        task_14_widget_clicked_grid.addWidget(self.task_14_text, 1, 0, 7, 0)
        task_14_widget_clicked_grid.addWidget(self.task_14_show_ans_btn, 10, 0, 12, 0)
        task_14_widget_clicked_grid.addWidget(self.task_14_show_descr_btn, 25, 0, 33, 0)
        self.task_14_widget.setLayout(task_14_widget_clicked_grid)

        def task_14_ans_button_clicked():
            self.task_14_show_ans_btn.setParent(None)
            task_14_widget_clicked_grid.addWidget(self.task_14_answer, 10, 0, 12, 0)
        def task_14_descr_button_clicked():
            self.task_14_show_descr_btn.setParent(None)
            task_14_widget_clicked_grid.addWidget(self.task_14_description_widget, 25, 0, 33, 0)

        self.task_14_show_ans_btn.clicked.connect(task_14_ans_button_clicked)
        self.task_14_show_descr_btn.clicked.connect(task_14_descr_button_clicked)


        # 1515151515151515151515151515
        self.task_15_widget = QWidget()
        self.task_15_data = Task_Chooser.choose_task(15)
        self.task_15_text = QLabel(self.task_15_data['text'])
        self.task_15_text.setWordWrap(True)
        self.task_15_text.setAlignment(Qt.AlignCenter)
        self.task_15_answer = QLabel('Ответ: ' + self.task_15_data['answer'])
        self.task_15_answer.setWordWrap(True)
        self.task_15_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_15_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_15_description = self.task_15_data['description']
        if self.task_15_data['python'].strip() != 'нет':
            self.task_15_description = self.task_15_description + '\n\n' + self.task_15_data['python']
        self.task_15_description_widget = QLabel(self.task_15_description)
        self.task_15_description_widget.setWordWrap(True)
        task_15_widget_clicked_grid = QGridLayout()
        
        task_15_widget_clicked_grid.addWidget(self.task_15_text, 1, 0, 7, 0)
        task_15_widget_clicked_grid.addWidget(self.task_15_show_ans_btn, 10, 0, 12, 0)
        task_15_widget_clicked_grid.addWidget(self.task_15_show_descr_btn, 25, 0, 33, 0)
        self.task_15_widget.setLayout(task_15_widget_clicked_grid)

        def task_15_ans_button_clicked():
            self.task_15_show_ans_btn.setParent(None)
            task_15_widget_clicked_grid.addWidget(self.task_15_answer, 10, 0, 12, 0)
        def task_15_descr_button_clicked():
            self.task_15_show_descr_btn.setParent(None)
            task_15_widget_clicked_grid.addWidget(self.task_15_description_widget, 25, 0, 33, 0)

        self.task_15_show_ans_btn.clicked.connect(task_15_ans_button_clicked)
        self.task_15_show_descr_btn.clicked.connect(task_15_descr_button_clicked)


        # 1616161616161616
        self.task_16_widget = QWidget()
        self.task_16_data = Task_Chooser.choose_task(16)
        self.task_16_text_for_lbl = self.task_16_data['text']
        if self.task_16_data['program'].strip() != 'нет':
            self.task_16_text_for_lbl = self.task_16_text_for_lbl + '\n\n' + self.task_16_data['program']
        self.task_16_text = QLabel(self.task_16_text_for_lbl)
        self.task_16_text.setWordWrap(True)
        self.task_16_answer = QLabel('Ответ: ' + self.task_16_data['answer'])
        self.task_16_answer.setWordWrap(True)
        self.task_16_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_16_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_16_description = self.task_16_data['description']
        self.task_16_description_widget = QLabel(self.task_16_description)
        self.task_16_description_widget.setWordWrap(True)
        task_16_widget_clicked_grid = QGridLayout()
        
        task_16_widget_clicked_grid.addWidget(self.task_16_text, 1, 0, 7, 0, alignment=Qt.AlignCenter)
        task_16_widget_clicked_grid.addWidget(self.task_16_show_ans_btn, 10, 0, 12, 0)
        task_16_widget_clicked_grid.addWidget(self.task_16_show_descr_btn, 25, 0, 33, 0)
        self.task_16_widget.setLayout(task_16_widget_clicked_grid)

        def task_16_ans_button_clicked():
            self.task_16_show_ans_btn.setParent(None)
            task_16_widget_clicked_grid.addWidget(self.task_16_answer, 10, 0, 12, 0)
        def task_16_descr_button_clicked():
            self.task_16_show_descr_btn.setParent(None)
            task_16_widget_clicked_grid.addWidget(self.task_16_description_widget, 25, 0, 33, 0)

        self.task_16_show_ans_btn.clicked.connect(task_16_ans_button_clicked)
        self.task_16_show_descr_btn.clicked.connect(task_16_descr_button_clicked)


        # 1717171717171717171717171717
        self.task_17_widget = QWidget()
        self.task_17_data = Task_Chooser.choose_task(17)
        self.task_17_text = QLabel(self.task_17_data['text'])
        self.task_17_text.setWordWrap(True)
        self.task_17_text.setAlignment(Qt.AlignCenter)
        self.task_17_answer = QLabel('Ответ: ' + self.task_17_data['answer'])
        self.task_17_answer.setWordWrap(True)
        self.task_17_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_17_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_17_description = self.task_17_data['description']
        if self.task_17_data['python'].strip() != 'нет':
            self.task_17_description = self.task_17_description + '\n\n' + self.task_17_data['python']
        self.task_17_description_widget = QLabel(self.task_17_description)
        self.task_17_description_widget.setWordWrap(True)
        task_17_widget_clicked_grid = QGridLayout()

        self.task_17_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_17_file_path = 'data/tasks_data/17/' + self.task_17_data['fileName']
        
        task_17_widget_clicked_grid.addWidget(self.task_17_text, 1, 0, 7, 0)
        task_17_widget_clicked_grid.addWidget(self.task_17_get_file_btn, 5, 0, 9, 0)
        task_17_widget_clicked_grid.addWidget(self.task_17_show_ans_btn, 10, 0, 12, 0)
        task_17_widget_clicked_grid.addWidget(self.task_17_show_descr_btn, 25, 0, 33, 0)
        self.task_17_widget.setLayout(task_17_widget_clicked_grid)

        def task_17_ans_button_clicked():
            self.task_17_show_ans_btn.setParent(None)
            task_17_widget_clicked_grid.addWidget(self.task_17_answer, 10, 0, 12, 0)
        def task_17_descr_button_clicked():
            self.task_17_show_descr_btn.setParent(None)
            task_17_widget_clicked_grid.addWidget(self.task_17_description_widget, 25, 0, 33, 0)

        self.task_17_show_ans_btn.clicked.connect(task_17_ans_button_clicked)
        self.task_17_show_descr_btn.clicked.connect(task_17_descr_button_clicked)

        def task_17_get_file_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_17_file_path, destination_path)
            except FileNotFoundError:
                pass
        self.task_17_get_file_btn.clicked.connect(task_17_get_file_button_clicked)


        # 1818181818181818181818181818
        self.task_18_widget = QWidget()
        self.task_18_data = Task_Chooser.choose_task(18)
        self.task_18_text = QLabel(self.task_18_data['text'])
        self.task_18_text.setWordWrap(True)
        self.task_18_text.setAlignment(Qt.AlignCenter)
        self.task_18_answer = QLabel('Ответ: ' + self.task_18_data['answer'])
        self.task_18_answer.setWordWrap(True)
        self.task_18_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_18_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_18_description = self.task_18_data['description']
        self.task_18_description_widget = QLabel(self.task_18_description)
        self.task_18_description_widget.setWordWrap(True)
        task_18_widget_clicked_grid = QGridLayout()

        self.task_18_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_18_file_path = 'data/tasks_data/18/' + self.task_18_data['id'] + '.xlsx'

        self.task_18_picture_path = 'data/tasks_data/18/example.png'
        self.task_18_picture = QPixmap(self.task_18_picture_path)
        self.task_18_picture_lbl = QLabel(self)
        self.task_18_picture_lbl.setPixmap(self.task_18_picture)
        
        task_18_widget_clicked_grid.addWidget(self.task_18_text, 1, 0, 5, 0)
        task_18_widget_clicked_grid.addWidget(self.task_18_picture_lbl, 5, 0, 9, 0, alignment=Qt.AlignCenter)
        task_18_widget_clicked_grid.addWidget(self.task_18_get_file_btn, 15, 0, 17, 0)
        task_18_widget_clicked_grid.addWidget(self.task_18_show_ans_btn, 40, 0, 42, 0)
        task_18_widget_clicked_grid.addWidget(self.task_18_show_descr_btn, 95, 0, 97, 0)
        self.task_18_widget.setLayout(task_18_widget_clicked_grid)

        def task_18_ans_button_clicked():
            self.task_18_show_ans_btn.setParent(None)
            task_18_widget_clicked_grid.addWidget(self.task_18_answer, 40, 0, 42, 0)
        def task_18_descr_button_clicked():
            self.task_18_show_descr_btn.setParent(None)
            task_18_widget_clicked_grid.addWidget(self.task_18_description_widget, 95, 0, 103, 0)

        self.task_18_show_ans_btn.clicked.connect(task_18_ans_button_clicked)
        self.task_18_show_descr_btn.clicked.connect(task_18_descr_button_clicked)

        def task_18_get_file_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_18_file_path, destination_path)
            except FileNotFoundError:
                pass
        self.task_18_get_file_btn.clicked.connect(task_18_get_file_button_clicked)


        # 19191919191919191919
        self.task_19_widget = QWidget()
        self.task_19_data = Task_Chooser.choose_task(19)
        self.task_19_text = QLabel(self.task_19_data['text'])
        self.task_19_text.setWordWrap(True)
        self.task_19_text.setAlignment(Qt.AlignCenter)
        self.task_19_answer = QLabel('Ответ: ' + self.task_19_data['answer'])
        self.task_19_answer.setWordWrap(True)
        self.task_19_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_19_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_19_description = self.task_19_data['description']
        self.task_19_description_widget = QLabel(self.task_19_description)
        self.task_19_description_widget.setWordWrap(True)
        task_19_widget_clicked_grid = QGridLayout()
        
        task_19_widget_clicked_grid.addWidget(self.task_19_text, 1, 0, 7, 0)
        task_19_widget_clicked_grid.addWidget(self.task_19_show_ans_btn, 10, 0, 12, 0)
        task_19_widget_clicked_grid.addWidget(self.task_19_show_descr_btn, 27, 0, 33, 0)
        self.task_19_widget.setLayout(task_19_widget_clicked_grid)

        def task_19_ans_button_clicked():
            self.task_19_show_ans_btn.setParent(None)
            task_19_widget_clicked_grid.addWidget(self.task_19_answer, 10, 0, 12, 0)
        def task_19_descr_button_clicked():
            self.task_19_show_descr_btn.setParent(None)
            task_19_widget_clicked_grid.addWidget(self.task_19_description_widget, 27, 0, 33, 0)

        self.task_19_show_ans_btn.clicked.connect(task_19_ans_button_clicked)
        self.task_19_show_descr_btn.clicked.connect(task_19_descr_button_clicked)


        # 20202020202020202020
        self.task_20_widget = QWidget()
        self.task_20_data = Task_Chooser.choose_task(20)
        self.task_20_text = QLabel(self.task_20_data['text'])
        self.task_20_text.setWordWrap(True)
        self.task_20_text.setAlignment(Qt.AlignCenter)
        self.task_20_answer = QLabel('Ответ: ' + self.task_20_data['answer'])
        self.task_20_answer.setWordWrap(True)
        self.task_20_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_20_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_20_description = self.task_20_data['description']
        self.task_20_description_widget = QLabel(self.task_20_description)
        self.task_20_description_widget.setWordWrap(True)
        task_20_widget_clicked_grid = QGridLayout()
        
        task_20_widget_clicked_grid.addWidget(self.task_20_text, 1, 0, 7, 0)
        task_20_widget_clicked_grid.addWidget(self.task_20_show_ans_btn, 10, 0, 12, 0)
        task_20_widget_clicked_grid.addWidget(self.task_20_show_descr_btn, 27, 0, 33, 0)
        self.task_20_widget.setLayout(task_20_widget_clicked_grid)

        def task_20_ans_button_clicked():
            self.task_20_show_ans_btn.setParent(None)
            task_20_widget_clicked_grid.addWidget(self.task_20_answer, 10, 0, 12, 0)
        def task_20_descr_button_clicked():
            self.task_20_show_descr_btn.setParent(None)
            task_20_widget_clicked_grid.addWidget(self.task_20_description_widget, 27, 0, 33, 0)

        self.task_20_show_ans_btn.clicked.connect(task_20_ans_button_clicked)
        self.task_20_show_descr_btn.clicked.connect(task_20_descr_button_clicked)


        # 21212121212121212121
        self.task_21_widget = QWidget()
        self.task_21_data = Task_Chooser.choose_task(21)
        self.task_21_text = QLabel(self.task_21_data['text'])
        self.task_21_text.setWordWrap(True)
        self.task_21_text.setAlignment(Qt.AlignCenter)
        self.task_21_answer = QLabel('Ответ: ' + self.task_21_data['answer'])
        self.task_21_answer.setWordWrap(True)
        self.task_21_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_21_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_21_description = self.task_21_data['description']
        self.task_21_description_widget = QLabel(self.task_21_description)
        self.task_21_description_widget.setWordWrap(True)
        task_21_widget_clicked_grid = QGridLayout()
        
        task_21_widget_clicked_grid.addWidget(self.task_21_text, 1, 0, 7, 0)
        task_21_widget_clicked_grid.addWidget(self.task_21_show_ans_btn, 10, 0, 12, 0)
        task_21_widget_clicked_grid.addWidget(self.task_21_show_descr_btn, 27, 0, 33, 0)
        self.task_21_widget.setLayout(task_21_widget_clicked_grid)

        def task_21_ans_button_clicked():
            self.task_21_show_ans_btn.setParent(None)
            task_21_widget_clicked_grid.addWidget(self.task_21_answer, 10, 0, 12, 0)
        def task_21_descr_button_clicked():
            self.task_21_show_descr_btn.setParent(None)
            task_21_widget_clicked_grid.addWidget(self.task_21_description_widget, 27, 0, 33, 0)

        self.task_21_show_ans_btn.clicked.connect(task_21_ans_button_clicked)
        self.task_21_show_descr_btn.clicked.connect(task_21_descr_button_clicked)


        # 2222222222222222
        self.task_22_widget = QWidget()
        self.task_22_data = Task_Chooser.choose_task(22)
        self.task_22_text = QLabel(self.task_22_data['text'] + '\n\n' + self.task_22_data['program'])
        self.task_22_text.setWordWrap(True)
        self.task_22_answer = QLabel('Ответ: ' + self.task_22_data['answer'])
        self.task_22_answer.setWordWrap(True)
        self.task_22_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_22_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_22_description = self.task_22_data['description']
        if self.task_22_data['python'].strip() != 'нет':
            self.task_22_description = self.task_22_description + '\n\n' + self.task_22_data['python']
        self.task_22_description_widget = QLabel(self.task_22_description)
        self.task_22_description_widget.setWordWrap(True)
        task_22_widget_clicked_grid = QGridLayout()
        
        task_22_widget_clicked_grid.addWidget(self.task_22_text, 1, 0, 7, 0, alignment=Qt.AlignCenter)
        task_22_widget_clicked_grid.addWidget(self.task_22_show_ans_btn, 10, 0, 12, 0)
        task_22_widget_clicked_grid.addWidget(self.task_22_show_descr_btn, 25, 0, 33, 0)
        self.task_22_widget.setLayout(task_22_widget_clicked_grid)

        def task_22_ans_button_clicked():
            self.task_22_show_ans_btn.setParent(None)
            task_22_widget_clicked_grid.addWidget(self.task_22_answer, 10, 0, 12, 0)
        def task_22_descr_button_clicked():
            self.task_22_show_descr_btn.setParent(None)
            task_22_widget_clicked_grid.addWidget(self.task_22_description_widget, 25, 0, 33, 0)

        self.task_22_show_ans_btn.clicked.connect(task_22_ans_button_clicked)
        self.task_22_show_descr_btn.clicked.connect(task_22_descr_button_clicked)


        # 23232323232323232323
        self.task_23_widget = QWidget()
        self.task_23_data = Task_Chooser.choose_task(23)
        self.task_23_text = QLabel(self.task_23_data['text'])
        self.task_23_text.setWordWrap(True)
        self.task_23_text.setAlignment(Qt.AlignCenter)
        self.task_23_answer = QLabel('Ответ: ' + self.task_23_data['answer'])
        self.task_23_answer.setWordWrap(True)
        self.task_23_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_23_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_23_description = self.task_23_data['description']
        self.task_23_description_widget = QLabel(self.task_23_description)
        self.task_23_description_widget.setWordWrap(True)
        task_23_widget_clicked_grid = QGridLayout()
        
        task_23_widget_clicked_grid.addWidget(self.task_23_text, 1, 0, 7, 0)
        task_23_widget_clicked_grid.addWidget(self.task_23_show_ans_btn, 10, 0, 12, 0)
        task_23_widget_clicked_grid.addWidget(self.task_23_show_descr_btn, 27, 0, 33, 0)
        self.task_23_widget.setLayout(task_23_widget_clicked_grid)

        def task_23_ans_button_clicked():
            self.task_23_show_ans_btn.setParent(None)
            task_23_widget_clicked_grid.addWidget(self.task_23_answer, 10, 0, 12, 0)
        def task_23_descr_button_clicked():
            self.task_23_show_descr_btn.setParent(None)
            task_23_widget_clicked_grid.addWidget(self.task_23_description_widget, 27, 0, 33, 0)

        self.task_23_show_ans_btn.clicked.connect(task_23_ans_button_clicked)
        self.task_23_show_descr_btn.clicked.connect(task_23_descr_button_clicked)


        # 2424242424242424242424242424
        self.task_24_widget = QWidget()
        self.task_24_data = Task_Chooser.choose_task(24)
        self.task_24_text = QLabel(self.task_24_data['text'])
        self.task_24_text.setWordWrap(True)
        self.task_24_text.setAlignment(Qt.AlignCenter)
        self.task_24_answer = QLabel('Ответ: ' + self.task_24_data['answer'])
        self.task_24_answer.setWordWrap(True)
        self.task_24_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_24_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_24_description = self.task_24_data['description']
        if self.task_24_data['python'].strip() != 'нет':
            self.task_24_description = self.task_24_description + '\n\n' + self.task_24_data['python']
        self.task_24_description_widget = QLabel(self.task_24_description)
        self.task_24_description_widget.setWordWrap(True)
        task_24_widget_clicked_grid = QGridLayout()

        self.task_24_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_24_file_path = 'data/tasks_data/24/' + self.task_24_data['id'] + '.txt'
        
        task_24_widget_clicked_grid.addWidget(self.task_24_text, 1, 0, 7, 0)
        task_24_widget_clicked_grid.addWidget(self.task_24_get_file_btn, 10, 0, 12, 0)
        task_24_widget_clicked_grid.addWidget(self.task_24_show_ans_btn, 25, 0, 27, 0)
        task_24_widget_clicked_grid.addWidget(self.task_24_show_descr_btn, 60, 0, 68, 0)
        self.task_24_widget.setLayout(task_24_widget_clicked_grid)

        def task_24_ans_button_clicked():
            self.task_24_show_ans_btn.setParent(None)
            task_24_widget_clicked_grid.addWidget(self.task_24_answer, 25, 0, 27, 0)
        def task_24_descr_button_clicked():
            self.task_24_show_descr_btn.setParent(None)
            task_24_widget_clicked_grid.addWidget(self.task_24_description_widget, 60, 0, 68, 0)

        self.task_24_show_ans_btn.clicked.connect(task_24_ans_button_clicked)
        self.task_24_show_descr_btn.clicked.connect(task_24_descr_button_clicked)

        def task_24_get_file_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_24_file_path, destination_path)
            except FileNotFoundError:
                pass
        self.task_24_get_file_btn.clicked.connect(task_24_get_file_button_clicked)


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
        task_25_widget_clicked_grid = QGridLayout()
        
        task_25_widget_clicked_grid.addWidget(self.task_25_text, 1, 0, 7, 0)
        task_25_widget_clicked_grid.addWidget(self.task_25_show_ans_btn, 10, 0, 12, 0)
        task_25_widget_clicked_grid.addWidget(self.task_25_show_descr_btn, 25, 0, 33, 0)
        self.task_25_widget.setLayout(task_25_widget_clicked_grid)

        def task_25_ans_button_clicked():
            self.task_25_show_ans_btn.setParent(None)
            task_25_widget_clicked_grid.addWidget(self.task_25_answer, 10, 0, 12, 0)
        def task_25_descr_button_clicked():
            self.task_25_show_descr_btn.setParent(None)
            task_25_widget_clicked_grid.addWidget(self.task_25_description_widget, 25, 0, 33, 0)

        self.task_25_show_ans_btn.clicked.connect(task_25_ans_button_clicked)
        self.task_25_show_descr_btn.clicked.connect(task_25_descr_button_clicked)


        # 2626262626262626262626262626
        self.task_26_widget = QWidget()
        self.task_26_data = Task_Chooser.choose_task(26)
        self.task_26_text = QLabel(self.task_26_data['text'])
        self.task_26_text.setWordWrap(True)
        self.task_26_text.setAlignment(Qt.AlignCenter)
        self.task_26_answer = QLabel('Ответ: ' + self.task_26_data['answer'])
        self.task_26_answer.setWordWrap(True)
        self.task_26_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_26_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_26_description = self.task_26_data['description']
        if self.task_26_data['python'].strip() != 'нет':
            self.task_26_description = self.task_26_description + '\n\n' + self.task_26_data['python']
        self.task_26_description_widget = QLabel(self.task_26_description)
        self.task_26_description_widget.setWordWrap(True)
        task_26_widget_clicked_grid = QGridLayout()

        self.task_26_get_file_btn = QPushButton(Localization.GET_FILE, self)
        self.task_26_file_path = 'data/tasks_data/26/' + self.task_26_data['id'] + '.txt'
        
        task_26_widget_clicked_grid.addWidget(self.task_26_text, 1, 0, 7, 0)
        task_26_widget_clicked_grid.addWidget(self.task_26_get_file_btn, 10, 0, 12, 0)
        task_26_widget_clicked_grid.addWidget(self.task_26_show_ans_btn, 25, 0, 27, 0)
        task_26_widget_clicked_grid.addWidget(self.task_26_show_descr_btn, 60, 0, 68, 0)
        self.task_26_widget.setLayout(task_26_widget_clicked_grid)

        def task_26_ans_button_clicked():
            self.task_26_show_ans_btn.setParent(None)
            task_26_widget_clicked_grid.addWidget(self.task_26_answer, 25, 0, 27, 0)
        def task_26_descr_button_clicked():
            self.task_26_show_descr_btn.setParent(None)
            task_26_widget_clicked_grid.addWidget(self.task_26_description_widget, 60, 0, 68, 0)

        self.task_26_show_ans_btn.clicked.connect(task_26_ans_button_clicked)
        self.task_26_show_descr_btn.clicked.connect(task_26_descr_button_clicked)

        def task_26_get_file_button_clicked():
            destination_path = QFileDialog.getExistingDirectory(self,Localization.FILE_DIALOG_SAVE,'.')
            try:
                shutil.copy(self.task_26_file_path, destination_path)
            except FileNotFoundError:
                pass
        self.task_26_get_file_btn.clicked.connect(task_26_get_file_button_clicked)


        # 2727272727272727272727272727
        self.task_27_widget = QWidget()
        self.task_27_data = Task_Chooser.choose_task(27)
        self.task_27_text = QLabel(self.task_27_data['text'])
        self.task_27_text.setWordWrap(True)
        self.task_27_text.setAlignment(Qt.AlignCenter)
        self.task_27_answer = QLabel('Ответ: ' + self.task_27_data['answer'])
        self.task_27_answer.setWordWrap(True)
        self.task_27_show_ans_btn = QPushButton(Localization.SHOW_ANSWER, self)
        self.task_27_show_descr_btn = QPushButton(Localization.SHOW_DESCRIPTION, self)
        self.task_27_description = self.task_27_data['description']
        if self.task_27_data['python'].strip() != 'нет':
            self.task_27_description = self.task_27_description + '\n\n' + self.task_27_data['python']
        self.task_27_description_widget = QLabel(self.task_27_description)
        self.task_27_description_widget.setWordWrap(True)
        task_27_widget_clicked_grid = QGridLayout()

        self.task_27_get_file_a_btn = QPushButton(Localization.GET_FILE_A, self)
        self.task_27_get_file_b_btn = QPushButton(Localization.GET_FILE_B, self)
        self.task_27_file_a_path = 'data/tasks_data/27/' + self.task_27_data['id'] + '_A.txt'
        self.task_27_file_b_path = 'data/tasks_data/27/' + self.task_27_data['id'] + '_B.txt'
        
        task_27_widget_clicked_grid.addWidget(self.task_27_text, 1, 0, 7, 0)
        task_27_widget_clicked_grid.addWidget(self.task_27_get_file_a_btn, 10, 0, 12, 1)
        task_27_widget_clicked_grid.addWidget(self.task_27_get_file_b_btn, 10, 1, 12, 1)
        task_27_widget_clicked_grid.addWidget(self.task_27_show_ans_btn, 25, 0, 27, 0)
        task_27_widget_clicked_grid.addWidget(self.task_27_show_descr_btn, 60, 0, 68, 0)
        self.task_27_widget.setLayout(task_27_widget_clicked_grid)

        def task_27_ans_button_clicked():
            self.task_27_show_ans_btn.setParent(None)
            task_27_widget_clicked_grid.addWidget(self.task_27_answer, 25, 0, 27, 0)
        def task_27_descr_button_clicked():
            self.task_27_show_descr_btn.setParent(None)
            task_27_widget_clicked_grid.addWidget(self.task_27_description_widget, 60, 0, 68, 0)

        self.task_27_show_ans_btn.clicked.connect(task_27_ans_button_clicked)
        self.task_27_show_descr_btn.clicked.connect(task_27_descr_button_clicked)

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


        # aft
        self.grid_clicked = QGridLayout()
        self.grid_clicked.addWidget(self.lbl2, 1, 0, alignment=Qt.AlignCenter)
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
            '19': self.task_19_widget,
            '20': self.task_20_widget,
            '21': self.task_21_widget,
            '22': self.task_22_widget,
            '23': self.task_23_widget,
            '24': self.task_24_widget,
            '25': self.task_25_widget,
            '26': self.task_26_widget,
            '27': self.task_27_widget
        }
        try:
            self.grid_clicked.addWidget(self.task_widgets[task_num], 2, 0, 4, 0)
        except KeyError:
            pass
        self.grid_clicked.addWidget(self.back_btn, 6, 0, 8, 0)

        save_manager.add_id_to_save(task_num, self.__dict__['task_%s_data' % str(task_num)]['id'])

        self.scrollArea = QScrollArea()
        self.setCentralWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)
        self.contents = QWidget()
        self.scrollArea.setWidget(self.contents)
        self.contents.setLayout(self.grid_clicked)

    def setupUi(self, BaseWindow):
        BaseWindow.resize(1000, 600)
        BaseWindow.move(100, 100)
        self.setupUi_continue()