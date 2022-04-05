import sys

from PyQt5.QtWidgets import QApplication

from bezier_curve.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec_()


if __name__ == '__main__':
    main()