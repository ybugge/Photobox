import sys

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtGui import QCursor

from DiashowClientPages.MainWindow import MainWindow
from DiashowClientPages.MainWindow import MainWindow

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    screensize = app.desktop().screenGeometry().size()
    app.setOverrideCursor(QCursor(Qt.BlankCursor))
    main_window = MainWindow(screensize)
    main_window.show()
    sys.exit(app.exec_())