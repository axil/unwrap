import sys
import numpy as np
from PyQt5 import QtWidgets, QtCore, uic
import pyqtgraph as pg
from math import pi
from PyQt5.QtCore import pyqtSlot as slot 

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

def hex2pen(x):
    return pg.mkPen(x)

BLUE = hex2pen("#1f77b4")
GREEN = hex2pen("#2ca02c")
ORANGE = hex2pen('#ff7f0e')
RED = hex2pen('#d62728')

Design, _ = uic.loadUiType('design.ui')

N = 1000

def wrap(x):
    return (x + pi) % (2*pi) - pi

def unwrap(x):
    return np.unwrap(x)


class ExampleApp(QtWidgets.QMainWindow, Design):
    def calc_y(self):
        np.random.seed(self.t)
        return np.sin(2*pi/(N/5)*self.x) + self.a*self.x + self.d*np.random.randn(N)

    def update_data(self):
        self.y = self.calc_y()
        self.w = wrap(self.y)
        self.u = unwrap(self.w)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.a = 0.
        self.d = 0.
        self.t = 0
        self.x = np.arange(N)
        self.update_data()
        self.wrapped_curve = self.canvas1.plot(self.w, symbol='o', symbolSize=5, pen=GREEN)
        self.orig_curve = self.canvas2.plot(self.y, symbol='o', symbolSize=5, pen=BLUE)
        self.unwrapped_curve = self.canvas3.plot(self.u, symbol='o', symbolSize=5, pen=ORANGE)
#  ‘o’ circle (default) * ‘s’ square * ‘t’ triangle * ‘d’ diamond * ‘+’ plus

    @QtCore.pyqtSlot()
    def on_pushButton_clicked(self):
        print('hi')
        self.curve.setData({'y': [-1,-4,-9]})

    def update(self):
        self.update_data()
        self.orig_curve.setData({'y': self.y})
        self.wrapped_curve.setData({'y': self.w})
        self.unwrapped_curve.setData({'y': self.u})

    @slot(int)
    def on_a_slider_valueChanged(self, v):
        self.a = -v/N
        self.update()

    @slot(int)
    def on_d_slider_valueChanged(self, v):
        self.d = v/99
        self.update()

    @slot(int)
    def on_t_slider_valueChanged(self, v):
        self.t = v
        self.update()

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))   # Более современная тема оформления
    app.setPalette(QtWidgets.QApplication.style().standardPalette())  # Берём цвета из темы оформления
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
