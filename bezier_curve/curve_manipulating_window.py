from typing import List

import numpy as np
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QWidget

from bezier_curve.bezier import bezier_curve_range
from bezier_curve.constants import WINDOW_GEOMETRY, MANIPULATION_CLICK_SENSITIVE, POINT_RADIUS


class BezierCurveManipulator(QWidget):

    def __init__(self):
        super(BezierCurveManipulator, self).__init__()
        self.setGeometry(*WINDOW_GEOMETRY)
        self.grabKeyboard()
        self.paint_area_shift = 20
        self.curve_points = np.array([[30, 350], [200, 50], [350, 660], [600, 30], [660, 350]])
        self.bezierPixmap = self.draw_bezier()
        self.draggin_idx = -1
        self.keypress_state = 0

    def paintEvent(self, e):
        p = QtGui.QPainter()
        p.begin(self)
        p.drawPixmap(0, 0, self.bezierPixmap)
        p.end()

    def _get_point(self, evt):
        return np.array([evt.pos().x(), evt.pos().y()])

    def set_curve_points(self, points: List[List[float]]):
        points = np.array(points)
        points = (points - points.min())
        points = points / points.max() * (700 - self.paint_area_shift * 2) + self.paint_area_shift
        self.curve_points = points
        self.bezierPixmap = self.draw_bezier()
        self.update()

    def _get_chosed_point(self, candidate: np.ndarray, threshold: int):
        dist = self.curve_points - candidate
        dist = dist[:, 0] ** 2 + dist[:, 1] ** 2
        max_val = dist.max() + 1
        dist[dist > threshold] = max_val
        if dist.min() < max_val:
            return dist.argmin()
        else:
            return -1

    def mousePressEvent(self, evt):
        if self.draggin_idx == -1:
            point = self._get_point(evt)
            idx = self._get_chosed_point(point, MANIPULATION_CLICK_SENSITIVE)
            if idx >= 0:
                self.draggin_idx = idx

    def mouseMoveEvent(self, evt):
        if self.draggin_idx != -1:
            point = self._get_point(evt)
            self.curve_points[self.draggin_idx] = point
            self.bezierPixmap = self.draw_bezier()
            self.update()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_A:
            self.keypress_state = 1
        elif event.key() == QtCore.Qt.Key_D:
            self.keypress_state = -1

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_A and self.keypress_state == 1:
            self.keypress_state = 0
        elif event.key() == QtCore.Qt.Key_D and self.keypress_state == -1:
            self.keypress_state = 0

    def mouseReleaseEvent(self, evt):
        point = self._get_point(evt)
        if self.keypress_state == 1:
            self.curve_points = np.insert(self.curve_points, -2, np.array(point), axis=0)
        elif self.keypress_state == -1:
            idx = self._get_chosed_point(point, MANIPULATION_CLICK_SENSITIVE)
            if idx == -1:
                return
            self.curve_points = np.delete(self.curve_points, idx, axis=0)
            self.draggin_idx = -1
        elif self.draggin_idx != -1:
            self.curve_points[self.draggin_idx] = point
            self.draggin_idx = -1
        else:
            return
        self.keypress_state = 0
        self.bezierPixmap = self.draw_bezier()
        self.update()

    def draw_bezier(self):
        pm = QtGui.QPixmap(WINDOW_GEOMETRY[2], WINDOW_GEOMETRY[3])
        pm.fill(QtCore.Qt.white)
        p = QtGui.QPainter()
        p.begin(pm)
        steps = 1000
        black_pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        green_pen = QtGui.QPen(QtCore.Qt.green, 1, QtCore.Qt.SolidLine)
        black_brush = QtGui.QBrush(QtCore.Qt.black)
        green_brush = QtGui.QBrush(QtCore.Qt.green)

        p.setPen(black_pen)
        p.setBrush(black_brush)
        cur_point = self.curve_points[0]
        for point in bezier_curve_range(steps, self.curve_points):
            p.drawLine(cur_point[0], cur_point[1], point[0], point[1])
            cur_point = point
        for point in self.curve_points[1:-1]:
            p.drawEllipse(QPoint(*point), POINT_RADIUS, POINT_RADIUS)

        p.setPen(green_pen)
        p.setBrush(green_brush)
        p.drawEllipse(QPoint(*self.curve_points[0]), POINT_RADIUS, POINT_RADIUS)
        p.drawEllipse(QPoint(*self.curve_points[-1]), POINT_RADIUS, POINT_RADIUS)
        p.end()
        return pm
