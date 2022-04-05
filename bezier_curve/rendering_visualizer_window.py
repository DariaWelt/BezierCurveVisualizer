from math import floor
from typing import List

import numpy as np
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtWidgets import QWidget

from bezier_curve.bezier import bezier_curve_range
from bezier_curve.constants import WINDOW_GEOMETRY, BEZIER_DRAWING_STEPS_NUM, POINT_RADIUS


class BezierRenderingVisualizer(QWidget):

    def __init__(self):
        super(BezierRenderingVisualizer, self).__init__()
        self.setGeometry(*WINDOW_GEOMETRY)
        self.paint_area_shift = 30
        self.curve_points = np.array([[30, 350], [200, 50], [350, 660], [600, 30], [660, 350]])
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
        p.end()

    def curve_animation(self):
        self.graphPixmap = self.bezierPixmap.copy()
        p = QtGui.QPainter()
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
            p.drawEllipse(QPoint(*cur_points[0]), POINT_RADIUS, POINT_RADIUS)
            for i in range(len(cur_points) - 1):
                p.drawLine(cur_points[i][0], cur_points[i][1],
                           cur_points[i + 1][0], cur_points[i + 1][1])
                p.drawEllipse(QPoint(*cur_points[i + 1]), POINT_RADIUS, POINT_RADIUS)
            cur_points = [cur_points[i] + (cur_points[i + 1] - cur_points[i]) * self.cur_state
                          for i in range(len(cur_points) - 1)]
        p.setPen(red_pen)
        p.setBrush(red_brush)
        p.drawEllipse(QPoint(*cur_points[0]), POINT_RADIUS, POINT_RADIUS)
        p.end()
        self.cur_state += self.state_speed
        self.cur_state -= floor(self.cur_state)
        self.update()

    def set_curve_points(self, points: List[List[float]]):
        points = np.array(points)
        points = (points - points.min())
        points = points / points.max() * (WINDOW_GEOMETRY[2] - self.paint_area_shift * 2) + self.paint_area_shift
        self.curve_points = points
        self.bezierPixmap = self.draw_bezier()
        self.update()

    def draw_bezier(self) -> QtGui.QPixmap:
        pm = QtGui.QPixmap(WINDOW_GEOMETRY[2], WINDOW_GEOMETRY[3])
        pm.fill(QtCore.Qt.white)
        p = QtGui.QPainter()
        p.begin(pm)
        red_pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
        green_pen = QtGui.QPen(QtCore.Qt.green, 1, QtCore.Qt.DashLine)
        red_brush = QtGui.QBrush(QtCore.Qt.red)
        green_brush = QtGui.QBrush(QtCore.Qt.green)
        p.setPen(red_pen)
        p.setBrush(red_brush)
        cur_point = self.curve_points[0]
        for point in bezier_curve_range(BEZIER_DRAWING_STEPS_NUM, self.curve_points):
            p.drawLine(cur_point[0], cur_point[1], point[0], point[1])
            cur_point = point
        p.setPen(green_pen)
        p.setBrush(green_brush)
        p.drawEllipse(QPoint(*self.curve_points[0]), POINT_RADIUS, POINT_RADIUS)
        for i in range(len(self.curve_points) - 1):
            p.drawLine(self.curve_points[i][0], self.curve_points[i][1],
                       self.curve_points[i + 1][0], self.curve_points[i + 1][1])
            p.drawEllipse(QPoint(*self.curve_points[i + 1]), POINT_RADIUS, POINT_RADIUS)
        p.end()
        return pm
