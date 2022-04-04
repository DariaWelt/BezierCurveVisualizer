import sys

from PyQt5.QtWidgets import QApplication

from rendering_visualizer_window import BezierRenderingVisualizer


def main(args):
    app = QApplication(sys.argv)
    ex = BezierRenderingVisualizer()
    ex.show()
    app.exec_()


if __name__ == '__main__':
    main(sys.argv[1:])