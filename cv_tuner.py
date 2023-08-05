'''
CvTuner ver 0.0.1
License: GPL3
Author: gear
twitter(X): @_gear_geek_
Usage: 
- GitHub Repository: https://github.com/gear2nd-droid/CvTuner
'''

import sys
import os
import platform
import glob
import cv2
import math
import importlib
import time
import threading
import image_processing as prcs
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
try:
    import __builtin__
except ImportError:
    import builtins as __builtin__
    
VERSION_TEXT = '''
CvTuner ver 0.0.1
Author: gear (@_gear_geek_)
'''
    
class GraphicsSceneCustom(QtWidgets.QGraphicsScene):
    def __init__(self, image, fval, parent=None, window=None):
        QGraphicsScene.__init__(self, parent)
        self.parent = parent
        self.window = window
        self.image = image
        self.fval = fval
        
    def mousePressEvent(self, event):
        pos = event.scenePos()
        x = int(pos.x())
        y = int(pos.y())
        ret = self.image.shape
        image_height = ret[0]
        image_width = ret[1]
        if len(ret) == 2:
            channel = 1
        else:
            channel = ret[2]        
        if 0 <= x and x < image_width and 0 <= y and y < image_height:
            if channel == 1:
                text = '{0}'.format(self.image[y][x])
            elif channel == 2:
                text = '{0}, {1}'.format(self.image[y][x][0], self.image[y][x][1])
            elif channel == 3:
                text = '{0}, {1}, {2}'.format(self.image[y][x][0], self.image[y][x][1], self.image[y][x][2])
            elif channel == 4:
                text = '{0}, {1}, {2}, {3}'.format(self.image[y][x][0], self.image[y][x][1], self.image[y][x][2], self.image[y][x][3])
            msg = QMessageBox()
            msg.setWindowTitle('Color pick')
            posx = math.floor(x / self.fval)
            posy = math.floor(y / self.fval)
            msg.setText('PosX:{0}, PosY:{1}\nPixel:{2}'.format(posx, posy, text))
            msg.exec_()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'CvTuner'
        self.dir_path = ''
        self.left = 0
        self.top = 75
        self.width = 1280
        self.height = 768
        self.initUI()
        # script auto open
        self.script_path = 'image_processing.py'
        f = open(self.script_path, 'r')
        alltext = f.read()
        f.close()
        self.editor.setPlainText(alltext)
        # init param
        importlib.reload(prcs)
        prm = prcs.init_parameter(self.message_console)
        keys = prm.keys()
        self.table_param.setRowCount(len(keys))
        for i, key in enumerate(keys):
            self.table_param.setItem(i, 0, QTableWidgetItem(key))
            self.table_param.setItem(i, 1, QTableWidgetItem(prm[key]))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # button style
        self.button_style_sheet = """
                                        QPushButton {
                                            background-color: #CCCCCC;
                                            color: #333333;
                                            border: none;
                                            padding: 10px 20px;
                                            border-radius: 10px;
                                        }
                                        QPushButton:hover {
                                            background-color: #AAAAAA;
                                        }
                                    """
        
        # layout
        self.left_panel_setting(self)
        self.central_panel_setting(self)
        self.right_panel_setting(self)
        
        # menu
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.file_menu = self.menubar.addMenu('File')
        self.help_menu = self.menubar.addMenu('Help')
        # menu:folder
        action_menu_folder_open = QAction('Folder open', self)
        action_menu_folder_open.triggered.connect(self.menu_folder_open)
        self.file_menu.addAction(action_menu_folder_open)
        # separator
        self.file_menu.addSeparator()
        # menu:script
        action_menu_script_open = QAction('Script open', self)
        action_menu_script_open.triggered.connect(self.menu_script_open)
        self.file_menu.addAction(action_menu_script_open)
        action_menu_script_save = QAction('Script save', self)
        action_menu_script_save.triggered.connect(self.menu_script_save)
        self.file_menu.addAction(action_menu_script_save)
        action_menu_script_reload = QAction('Script reload', self)
        action_menu_script_reload.triggered.connect(self.menu_script_reload)
        self.file_menu.addAction(action_menu_script_reload)
        # version
        action_menu_version = QAction('Version', self)
        action_menu_version.triggered.connect(self.menu_version_dialog)
        self.help_menu.addAction(action_menu_version)
        
        # splitter
        self.splitter = QSplitter()
        splitter_style_sheet = """
            QSplitter::handle {
                background: gray;
            }
            QSplitter::handle:horizontal {
                width: 1px;
            }
            QSplitter::handle:vertical {
                height: 1px;
            }
        """
        self.splitter.setStyleSheet(splitter_style_sheet)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.addWidget(QWidget())
        self.splitter.addWidget(QWidget())
        self.splitter.addWidget(QWidget())
        self.splitter.widget(0).setLayout(self.left_pane_layout)
        self.splitter.widget(1).setLayout(self.central_layout)
        self.splitter.widget(2).setLayout(self.right_layout)
        
        # main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.splitter)
        central_widget = QWidget(self)
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        self.signal_connecter(self)
        self.show()
        
        # parameter
        self.patern_idx = 0

    def left_panel_setting(self,MainWindow):
        global message_console
        self.editor = QPlainTextEdit(MainWindow)

        self.message_console = QtWidgets.QTextEdit(MainWindow)
        self.message_console.setMinimumHeight(30)
        self.message_console.setReadOnly(True)
        self.message_console.setStyleSheet("background-color: rgb(26, 26, 26);")
        self.message_console.setTextColor(QColor('#ffffff'))

        self.message_splitter = QSplitter()
        self.message_splitter.setOrientation(Qt.Vertical)
        self.message_splitter.addWidget(self.editor)
        self.message_splitter.addWidget(self.message_console)
        self.message_splitter.setSizes([8,2])
        
        self.left_pane_layout = QVBoxLayout()
        self.left_pane_layout.addWidget(self.message_splitter)

    def central_panel_setting(self, MainWindow):
        self.comboBox = QComboBox(MainWindow)
        self.number_edit = QTextEdit(MainWindow)
        self.number_edit.setMinimumSize(50, 20)
        self.number_edit.setMaximumSize(50, 30)
        self.number_label = QLabel(MainWindow)
        self.number_label.setMinimumSize(50, 20)
        self.number_label.setMaximumSize(50, 30)
        self.filename_label = QLabel(MainWindow)
        self.start_button = QtWidgets.QToolButton(MainWindow)
        self.left_button = QtWidgets.QToolButton(MainWindow)
        self.right_button = QtWidgets.QToolButton(MainWindow)
        self.end_button = QtWidgets.QToolButton(MainWindow)
        self.start_button.setArrowType(Qt.LeftArrow)
        self.left_button.setArrowType(Qt.LeftArrow)
        self.right_button.setArrowType(Qt.RightArrow)
        self.end_button.setArrowType(Qt.RightArrow)
        
        self.graphicsView = QGraphicsView(MainWindow)
        self.view_width = 640
        self.view_height = 480
        self.graphicsView.setMinimumSize(QtCore.QSize(self.view_width + 2, self.view_height + 2))
        
        
        self.histgramView = QWidget(MainWindow)
        self.histgramView.setMaximumSize(QtCore.QSize(self.view_width + 2, 160))
        self.histgramLayout = QVBoxLayout(self.histgramView)
        self.histgramLayout.setContentsMargins(0, 0, 0, 0)
        self.histgram_figure = plt.figure()
        self.histgram_axis = self.histgram_figure.add_subplot(1, 1, 1)
        self.histgram_canvas = FigureCanvas(self.histgram_figure)  

        self.histgram_ymax = 10000
        self.histgram_ymin = 0
        self.histgram_xmax = 256
        self.histgram_xmin = 0
        self.histgram_layout_h = QHBoxLayout()
        self.histgram_layout_v = QVBoxLayout()
        self.histgram_ymaxlabel = QLabel(MainWindow)
        self.histgram_ymaxlabel.setText('Y max')
        self.histgram_ymaxvalue = QTextEdit(MainWindow)
        self.histgram_ymaxvalue.setMaximumSize(100,25)
        self.histgram_ymaxvalue.setText(str(self.histgram_ymax))
        self.histgram_yminlabel = QLabel(MainWindow)
        self.histgram_yminlabel.setText('Y min')
        self.histgram_yminvalue = QTextEdit(MainWindow)
        self.histgram_yminvalue.setMaximumSize(100,25)
        self.histgram_yminvalue.setText(str(self.histgram_ymin))
        self.histgram_xmaxlabel = QLabel(MainWindow)
        self.histgram_xmaxlabel.setText('X max')
        self.histgram_xmaxvalue = QTextEdit(MainWindow)
        self.histgram_xmaxvalue.setMaximumSize(100,25)
        self.histgram_xmaxvalue.setText(str(self.histgram_xmax))
        self.histgram_xminblabel = QLabel(MainWindow)
        self.histgram_xminblabel.setText('X min')
        self.histgram_xminvalue = QTextEdit(MainWindow)
        self.histgram_xminvalue.setMaximumSize(100,25)
        self.histgram_xminvalue.setText(str(self.histgram_xmin))
        self.histgram_layout_v.addWidget(self.histgram_ymaxlabel)
        self.histgram_layout_v.addWidget(self.histgram_ymaxvalue) 
        self.histgram_layout_v.addWidget(self.histgram_yminlabel)
        self.histgram_layout_v.addWidget(self.histgram_yminvalue) 
        self.histgram_layout_v.addWidget(self.histgram_xmaxlabel)
        self.histgram_layout_v.addWidget(self.histgram_xmaxvalue) 
        self.histgram_layout_v.addWidget(self.histgram_xminblabel)
        self.histgram_layout_v.addWidget(self.histgram_xminvalue) 
        self.histgram_layout_h.addWidget(self.histgramView) 
        self.histgram_layout_h.addLayout(self.histgram_layout_v)        
        
        self.tool_layout = QHBoxLayout()
        self.tool_layout.addWidget(self.number_edit)
        self.tool_layout.addWidget(self.number_label)
        self.tool_layout.addWidget(self.start_button)
        self.tool_layout.addWidget(self.left_button)
        self.tool_layout.addWidget(self.right_button)
        self.tool_layout.addWidget(self.end_button)
        self.tool_layout.addWidget(self.filename_label)
        self.tool_layout.addWidget(self.comboBox)

        self.graphic_seg_layout =  QVBoxLayout()
        self.graphic_seg_layout.addWidget(self.graphicsView)
        self.graphic_seg_layout.addLayout(self.histgram_layout_h)

        self.central_layout =  QVBoxLayout()
        self.central_layout.addLayout(self.tool_layout)
        self.central_layout.addLayout(self.graphic_seg_layout)

    def right_panel_setting(self, MainWindow):        
        self.table_param = QTableWidget(MainWindow)   
        self.table_param.setColumnCount(2)
        self.table_param.setHorizontalHeaderLabels(['Name', 'Value'])
        self.table_result = QTableWidget(MainWindow)   
        self.table_result.setColumnCount(2)
        self.table_result.setHorizontalHeaderLabels(['Name', 'Value']) 

        self.table_splitter = QSplitter()
        self.table_splitter.setOrientation(Qt.Vertical)
        self.table_splitter.addWidget(self.table_param)
        self.table_splitter.addWidget(self.table_result)
        self.table_splitter.setSizes([10,1])   

        self.right_button_layout = QtWidgets.QHBoxLayout()   
        self.execute_button = QtWidgets.QPushButton(MainWindow)
        self.execute_button.setStyleSheet(self.button_style_sheet)
        self.execute_button.setText('Execute')
        self.exe_start_button = QtWidgets.QPushButton(MainWindow)
        self.exe_start_button.setStyleSheet(self.button_style_sheet)
        self.exe_start_button.setText('Start')
        self.exe_stop_button = QtWidgets.QPushButton(MainWindow)
        self.exe_stop_button.setStyleSheet(self.button_style_sheet)
        self.exe_stop_button.setText('Stop')
        self.right_button_layout.addWidget(self.execute_button)
        self.right_button_layout.addWidget(self.exe_start_button)
        self.right_button_layout.addWidget(self.exe_stop_button)
             
        self.add_param_button = QtWidgets.QPushButton(MainWindow)
        self.add_param_button.setStyleSheet(self.button_style_sheet)
        self.add_param_button.setText('Add parameter')
        
        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_layout.addWidget(self.add_param_button)
        self.right_layout.addWidget(self.table_splitter)
        self.right_layout.addLayout(self.right_button_layout)
        
    def signal_connecter(self, MainWindow):
        self.start_button.pressed.connect(self.start_button_pressed)
        self.left_button.pressed.connect(self.left_button_pressed)
        self.right_button.pressed.connect(self.right_button_pressed)
        self.end_button.pressed.connect(self.end_button_pressed)
        self.comboBox.activated.connect(self.combo_activated)
        self.execute_button.pressed.connect(self.execute_pressed)
        self.exe_start_button.pressed.connect(self.exe_start_pressed)
        self.exe_stop_button.pressed.connect(self.exe_stop_pressed)
        self.add_param_button.pressed.connect(self.add_param_pressed)
        self.histgram_xmaxvalue.textChanged.connect(self.changed_xmax)
        self.histgram_xminvalue.textChanged.connect(self.changed_xmin)
        self.histgram_ymaxvalue.textChanged.connect(self.changed_ymax)
        self.histgram_yminvalue.textChanged.connect(self.changed_ymin)
        self.message_console.textChanged.connect(self.message_append)
        self.number_edit.textChanged.connect(self.changed_number)
        
    def print_console(self, message):
        __builtin__.print(message)
        self.message_console.setTextColor(QColor('#ffffff'))
        self.message_console.append(message)   

    def message_append(self):
        self.message_console.moveCursor(QTextCursor.End)  
        
    def execute(self):
        fullpath = self.file_list[self.file_idx]
        filename = os.path.basename(fullpath)
        self.filename_label.setText(filename)
        self.number_edit.setText(str(self.file_idx + 1))
        self.number_label.setText('/{0}'.format(len(self.file_list)))
        
        # init param
        prm = {}
        cnt = self.table_param.rowCount()
        for i in range(cnt):
            key = self.table_param.item(i, 0).text()
            val = self.table_param.item(i, 1).text()
            prm[key] = val
        
        # original
        self.image_dic = {}
        self.image_dic['original'] = cv2.imread(fullpath)
        
        # image_process
        importlib.reload(prcs)
        ret = prcs.image_process(self.image_dic, prm, filename, self.message_console)
        self.image_dic = ret[0]
        result = ret[1]
        self.draw_object()
        
        # table_result
        keys = result.keys()
        self.table_result.setRowCount(len(keys))
        for i, key in enumerate(keys):
            self.table_result.setItem(i, 0, QTableWidgetItem(key))
            self.table_result.setItem(i, 1, QTableWidgetItem(result[key]))
        
    def draw_object(self):
        # combobox
        keys = self.image_dic.keys()
        for i in range(self.comboBox.count()):
            self.comboBox.removeItem(0)
        self.comboBox.addItems(keys)
        # renew
        self.comboBox.setCurrentIndex(self.patern_idx)
        self.img = self.draw_image()
        self.draw_histgram()
        
    def draw_image(self):
        # dictionary
        buf = self.image_dic.keys()
        keys = []
        for key in buf:
            keys.append(key)
        # draw file
        key = keys[self.patern_idx]
        img = self.image_dic[key]
        ret = img.shape
        image_height = ret[0]
        image_width = ret[1]
        if len(ret) == 2:
            self.channel = 1
        else:
            self.channel = ret[2]
        fval = min(self.view_width / image_width, self.view_height / image_height)
        # image edit
        draw_img = cv2.resize(img, dsize=None, fx = fval, fy = fval)
        image_width = math.floor(image_width * fval)
        image_height = math.floor(image_height * fval)
        if self.channel == 3:
            image = QtGui.QImage(draw_img, image_width, image_height, QImage.Format_BGR888)
        elif self.channel ==1:
            image = QtGui.QImage(draw_img, image_width, image_height, QImage.Format_Grayscale8)
        elif self.channel == 4:
            image = QtGui.QImage(draw_img, image_width, image_height, QImage.Format_BGRA8888)
        else:
            image = QtGui.QImage(draw_img, image_width, image_height, QImage.Format_BGR888)
        # scene
        pixmap = QtGui.QPixmap.fromImage(image)
        self.graphics_scene = GraphicsSceneCustom(draw_img, fval)
        self.graphics_scene.addPixmap(pixmap)
        self.graphicsView.setScene(self.graphics_scene)
        self.graphicsView.show()
        return img
        
    def draw_histgram(self):
        color = ["b", "g", "r"]
        x = range(256)
        self.histgram_axis.cla()
        plt.xlim((self.histgram_xmin, self.histgram_xmax))
        plt.ylim((self.histgram_ymin, self.histgram_ymax))
        xtick = [self.histgram_xmin]
        for i in range(8):
            buf = math.floor((self.histgram_xmax - self.histgram_xmin) / 8 * i + self.histgram_xmin)
            xtick.append(buf)
        plt.xticks(xtick)
        for ch in range(self.channel):
            hist = cv2.calcHist([self.img], channels=[ch], mask=None, histSize=[256], ranges=[0, 256])
            hist = hist.squeeze(axis=-1)
            self.histgram_axis.plot(x, hist, color[ch])
        self.histgramLayout.removeWidget(self.histgram_canvas)
        self.histgram_canvas = FigureCanvas(self.histgram_figure)
        self.histgramLayout.addWidget(self.histgram_canvas)   
            
    def menu_folder_open(self):
        self.dir_path = QFileDialog.getExistingDirectory(self, 'Open Folder', os.path.expanduser('~'))
        if len(self.dir_path) > 0:
            self.file_list = glob.glob(self.dir_path + r'/*.*')
            self.file_idx = 0
            title = 'CvTuner - SCRIPT: {0} , FOLDER: {1}'.format(self.script_path, self.dir_path)
            self.setWindowTitle(title)
            self.execute()
        
    def menu_script_open(self):
        dir = os.path.expanduser('~')
        filters = "Script files (*.py)"
        selected_filter = "Script (*.py)"
        options = QFileDialog.Option.ReadOnly
        ret = QFileDialog.getOpenFileName(self, 'Open Script', dir, filters, selected_filter, options)
        self.script_path = ret[0]
        selectedFilter = ret[1]
        if self.dir_path == '':
            title = 'CvTuner - SCRIPT: {0}'.format(self.script_path)
        else:
            title = 'CvTuner - SCRIPT: {0} , FOLDER: {1}'.format(self.script_path, self.dir_path)
        self.setWindowTitle(title)
        # copy
        self.menu_script_reload()
        
    def menu_script_save(self):
        alltext = self.editor.toPlainText()
        # script
        f = open(self.script_path, 'w')
        f.write(alltext)
        f.close()
        # image_processing
        f = open('image_processing.py', 'w')
        f.write(alltext)
        f.close()
        
    def menu_script_reload(self):
        f = open(self.script_path, 'r')
        alltext = f.read()
        f.close()
        self.editor.setPlainText(alltext)
        self.menu_script_save()
        # init param
        importlib.reload(prcs)
        prm = prcs.init_parameter(self.message_console)
        keys = prm.keys()
        self.table_param.setRowCount(len(keys))
        for i, key in enumerate(keys):
            self.table_param.setItem(i, 0, QTableWidgetItem(key))
            self.table_param.setItem(i, 1, QTableWidgetItem(prm[key]))
        
    def start_button_pressed(self):
        self.file_idx = 0
        self.execute()
        
    def left_button_pressed(self):
        self.file_idx -= 1
        if self.file_idx < 0:
            self.file_idx = 0
        self.execute()
        
    def right_button_pressed(self):
        self.file_idx += 1
        if self.file_idx >= len(self.file_list):
            self.file_idx = len(self.file_list) - 1
        self.execute()
        
    def end_button_pressed(self):
        self.file_idx = len(self.file_list) - 1
        self.execute()
        
    def combo_activated(self, arg1=None, arg2=None):
        self.patern_idx = arg1
        self.draw_object()
        
    def execute_pressed(self):
        self.menu_script_save()
        self.execute()
        
    def exe_start_pressed(self):
        self.menu_script_save()
        self.executing = True
        self.thread = ExeThread(self)
        self.thread.start()
        
    def exe_stop_pressed(self):
        self.executing = False
        
    def add_param_pressed(self):
        cnt = self.table_param.rowCount()
        self.table_param.setRowCount(cnt + 1)
        
    def changed_xmax(self):
        try:
            buf = int(self.histgram_xmaxvalue.toPlainText())
            self.histgram_xmax = buf
            self.draw_histgram()
        except:
            pass
        
    def changed_xmin(self):
        try:
            buf = int(self.histgram_xminvalue.toPlainText())
            self.histgram_xmin = buf
            self.draw_histgram()
        except:
            pass
        
    def changed_ymax(self):
        try:
            buf = int(self.histgram_ymaxvalue.toPlainText())
            self.histgram_ymax = buf
            self.draw_histgram()
        except:
            pass
        
    def changed_ymin(self):
        try:
            buf = int(self.histgram_yminvalue.toPlainText())
            self.histgram_ymin = buf
            self.draw_histgram()
        except:
            pass
            
    def changed_number(self):
        try:
            buf = int(self.number_edit.toPlainText())
            if 1 <= buf and buf <= len(self.file_list):
                if self.file_idx != buf - 1:
                    self.file_idx = buf - 1
                    self.execute()
        except:
            pass
            
    def menu_version_dialog(self):
        msg = QMessageBox()
        msg.setWindowTitle('Version')
        msg.setText(VERSION_TEXT)
        msg.exec_()

class ExeThread(QThread):
    def __init__(self, obj):
        self.obj = obj
        super(ExeThread, self).__init__()

    def run(self):
        while(self.obj.executing):
            self.obj.right_button_pressed()
            #time.sleep(1)
            if self.obj.file_idx == len(self.obj.file_list) - 1:
                break
                
if __name__ == "__main__":
    global app, main_window
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())