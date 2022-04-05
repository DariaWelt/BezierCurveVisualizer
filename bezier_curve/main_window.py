from PyQt5.QtWidgets import QMainWindow, QGridLayout, QStackedWidget, QToolBar, QToolButton, QFileDialog, QMessageBox

from bezier_curve.constants import WINDOW_GEOMETRY
from bezier_curve.curve_manipulating_window import BezierCurveManipulator
from bezier_curve.rendering_visualizer_window import BezierRenderingVisualizer


class MainWindow(QMainWindow):
    def load_curve(self):
        points = []
        filename = QFileDialog.getOpenFileName(self, 'Загрузить координаты кривой', '', "txt Files (*.txt)",
                                               options=QFileDialog.DontUseNativeDialog)
        if filename[0] == '':
            return
        try:
            with open(filename[0], 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if len(line) < 3:
                        continue
                    line = line[:-1]
                    line = ''.join(line.split(' '))
                    x, y = line.split(',')
                    points.append([float(x), float(y)])
        except Exception as e:
            error(e.message)
            return
        if len(points) > 1:
            self.points = points
            self.update_points()

    def update_points(self):
        self.rendering_visualizer_window.set_curve_points(self.points)
        self.manipulating_window.set_curve_points(self.points)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(*WINDOW_GEOMETRY)
        self.setWindowTitle('Визуализация рендеринга кривой Безье')
        self.l0 = QGridLayout()
        self.manipulating_window = BezierCurveManipulator()
        self.rendering_visualizer_window = BezierRenderingVisualizer()

        self.pages = QStackedWidget(self)
        self.pages.addWidget(self.manipulating_window)
        self.pages.addWidget(self.rendering_visualizer_window)

        self.setCentralWidget(self.pages)
        self._create_toolbar()

    def _create_toolbar(self):
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.open_manipulator_button = QToolButton()
        self.open_manipulator_button.setText('Манипулятор')
        self.open_manipulator_button.setChecked(True)
        self.open_manipulator_button.setAutoExclusive(True)
        self.open_manipulator_button.clicked.connect(
            lambda: self.centralWidget().setCurrentIndex(self.pages.indexOf(self.manipulating_window))
        )
        self.open_visualizer_button = QToolButton()
        self.open_visualizer_button.setText('Анимация построения')
        self.open_visualizer_button.setChecked(True)
        self.open_visualizer_button.setAutoExclusive(True)
        self.open_visualizer_button.clicked.connect(
            lambda: self.centralWidget().setCurrentIndex(self.pages.indexOf(self.rendering_visualizer_window))
        )

        self.load_curve_button = QToolButton()
        self.load_curve_button.setText('Загрузить кривую')
        self.load_curve_button.setChecked(True)
        self.load_curve_button.setAutoExclusive(True)
        self.load_curve_button.clicked.connect(self.load_curve)

        self.toolbar.addWidget(self.load_curve_button)
        self.toolbar.addWidget(self.open_manipulator_button)
        self.toolbar.addWidget(self.open_visualizer_button)


def error(text: str) -> None:
    err = QMessageBox()
    err.setWindowTitle("Ошибка")
    err.setText(text)
    err.setIcon(QMessageBox.Warning)
    err.setStandardButtons(QMessageBox.Ok)
    err.exec_()

