# ------------------ PySide2 - Qt Designer - Matplotlib ------------------
from PySide6.QtWidgets import*
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTimer

from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure

import numpy as np
import random

from device_connection import get_sensor_data
from model_com import model_com

# ------------------ MplWidget ------------------
class MplWidget(QWidget):
    
    def __init__(self, parent = None):
        
        QWidget.__init__(self, parent)
        
        self.canvas = FigureCanvas(Figure())
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(NavigationToolbar(self.canvas, self))
        
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)    

# ------------------ MainWidget ------------------
class MainWidget(QWidget):

    def __init__(self):
        self.time = []
        self.sensor0 = []
        self.sensor1 = []
        self.sensor2 = []
        self.sensor3 = []
        self.hit = False
        self.last = 0
        self.timer_var = 0
        self.timer = None
        self.en_sensor0 = True
        self.en_sensor1 = True
        self.en_sensor2 = True
        self.en_sensor3 = True
        self.time_pred = None
        
        QWidget.__init__(self)

        designer_file = QFile("form.ui")
        designer_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        loader.registerCustomWidget(MplWidget)
        self.ui = loader.load(designer_file, self)

        designer_file.close()

        self.ui.pushButton_generate_random_signal.clicked.connect(self.do_req)
        self.ui.pushButton_start_pred.clicked.connect(self.start_pred)
        self.ui.pushButton_pause_graph.clicked.connect(self.pause_graph)
        self.setWindowTitle("PenguinInvasion")

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.ui)
        self.setLayout(grid_layout)



    def update_graph(self):
        self.last+=1
        if len(self.sensor0) >= 40:
            self.hit = True
        if self.hit:
            self.sensor0.pop(0)
            self.sensor1.pop(0)
            self.sensor2.pop(0)
            self.sensor3.pop(0)

        max_len = max(len(self.sensor0), len(self.sensor1), len(self.sensor2), len(self.sensor3))

        self.sensor0.append(get_sensor_data()[0])
        self.sensor1.append(get_sensor_data()[1])
        self.sensor2.append(get_sensor_data()[2])
        self.sensor3.append(get_sensor_data()[3])
        if len(self.time) < 40:
            self.time.append(self.timer_var)
            self.timer_var += 1
        if len(self.time) == len(self.sensor0) and len(self.time) == len(self.sensor1) and len(self.time) == len(self.sensor2) and len(self.time) == len(self.sensor3):
            self.ui.MplWidget.canvas.axes.cla()
            if self.ui.checkBox_sensor0.isChecked():
                self.ui.MplWidget.canvas.axes.plot(self.time, self.sensor0)
            if self.ui.checkBox_sensor1.isChecked():
                self.ui.MplWidget.canvas.axes.plot(self.time, self.sensor1)
            if self.ui.checkBox_sensor2.isChecked():
                self.ui.MplWidget.canvas.axes.plot(self.time, self.sensor2)
            if self.ui.checkBox_sensor3.isChecked():
                self.ui.MplWidget.canvas.axes.plot(self.time, self.sensor3)
        
        self.ui.MplWidget.canvas.draw()

    def do_req(self):
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(100)
        if not self.ui.pushButton_start_pred.isEnabled():
            self.ui.pushButton_start_pred.setEnabled(True)
    
    def pause_graph(self):
        if self.timer != None:
            self.timer.stop()
            if self.timer_pred != None:
                self.timer_pred.stop()
            if self.ui.pushButton_start_pred.isEnabled():
                self.ui.pushButton_start_pred.setEnabled(False)
        

    def make_pred(self):
        res = model_com('www.google.com',
                        self.sensor0, self.sensor1, self.sensor2, self.sensor3)
        print('ress', str(res))

    def start_pred(self):
        self.timer_pred = QTimer()
        self.timer_pred.setSingleShot(False)
        self.timer_pred.timeout.connect(self.make_pred)
        self.timer_pred.start(10000)

app = QApplication([])
window = MainWidget()
window.show()
app.exec_()
