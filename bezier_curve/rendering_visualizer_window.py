from math import floor
from typing import List

import numpy as np
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget

from bezier_curve import bezier_curve_range


class BezierRenderingVisualizer(QWidget):

    def __init__(self):
        super(BezierRenderingVisualizer, self).__init__()
        window_geometry = [100, 100, 700, 700]
        self.setGeometry(*window_geometry)
        self.paint_area_shift = 20
        self.setWindowTitle('Bezier Curves')
        self.curve_points = np.array([[20, 350], [200, 50], [350, 670], [600, 20], [680, 350]])
        self.cur_state = 0.0
        self.state_speed = 0.001
        self.bezierPixmap = self.draw_bezier()
        self.graphPixmap = self.bezierPixmap.copy()

        timer = QTimer(self)
        timer.timeout.connect(self.curve_animation)
        timer.start(10)

    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        #p.setRenderHints(QtGui.QPainter.Antialiasing, True)
        p.drawPixmap(0, 0, self.graphPixmap)

    def curve_animation(self):
        self.graphPixmap = self.bezierPixmap.copy()
        p = QtGui.QPainter(self.graphPixmap)
        p.begin(self.graphPixmap)
        gray_pen = QtGui.QPen(QtCore.Qt.gray, 1, QtCore.Qt.DashLine)
        red_pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
        gray_brush = QtGui.QBrush(QtCore.Qt.gray)
        red_brush = QtGui.QBrush(QtCore.Qt.red)
        p.setPen(gray_pen)
        p.setBrush(gray_brush)

        cur_points = [self.curve_points[i] + (self.curve_points[i + 1] - self.curve_points[i]) * self.cur_state
                      for i in range(len(self.curve_points) - 1)]
        while len(cur_points) > 1:
            p.drawEllipse(*cur_points[0], 5, 5)
            for i in range(len(cur_points) - 1):
                p.drawLine(cur_points[i][0], cur_points[i][1],
                           cur_points[i + 1][0], cur_points[i + 1][1])
                p.drawEllipse(*cur_points[i + 1], 5, 5)
            cur_points = [cur_points[i] + (cur_points[i + 1] - cur_points[i]) * self.cur_state
                          for i in range(len(cur_points) - 1)]
        p.setPen(red_pen)
        p.setBrush(red_brush)
        p.drawEllipse(*cur_points[0], 7, 7)
        p.end()
        self.cur_state += self.state_speed
        self.cur_state -= floor(self.cur_state)
        self.update()

    def set_curve_points(self, points: List[List[float]]):
        points = np.array(points)
        points = (points - points.min())
        points = points / points.max() * (700 - self.paint_area_shift * 2) + self.paint_area_shift
        self.curve_points = points
        self.bezierPixmap = self.draw_bezier()

    def draw_bezier(self) -> QtGui.QPixmap:
        steps = 1000
        pm = QtGui.QPixmap(700, 700)
        pm.fill(QtCore.Qt.white)
        p = QtGui.QPainter(pm)
        p.begin(pm)
        red_pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
        green_pen = QtGui.QPen(QtCore.Qt.green, 1, QtCore.Qt.DashLine)
        red_brush = QtGui.QBrush(QtCore.Qt.red)
        green_brush = QtGui.QBrush(QtCore.Qt.green)
        p.setPen(red_pen)
        p.setBrush(red_brush)
        if len(self.curve_points) > 1:
            cur_point = self.curve_points[0]
            for point in bezier_curve_range(steps, self.curve_points):
                p.drawLine(cur_point[0], cur_point[1], point[0], point[1])
                cur_point = point
            p.setPen(green_pen)
            p.setBrush(green_brush)
            p.drawEllipse(*self.curve_points[0], 7, 7)
            for i in range(len(self.curve_points) - 1):
                p.drawLine(self.curve_points[i][0], self.curve_points[i][1],
                           self.curve_points[i + 1][0], self.curve_points[i + 1][1])
                p.drawEllipse(*self.curve_points[i + 1], 7, 7)
        else:
            p.drawText(300, 300, 'Неверный формат файла. На вход ожидается файл с указанием не менее двух точек кривой')
        p.end()
        return pm
