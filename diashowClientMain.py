import sys

from PyQt5 import QtWidgets, Qt
from PyQt5.QtGui import QCursor

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    screensize = app.desktop().availableGeometry().size()

    app.setOverrideCursor(QCursor(Qt.BlankCursor))
    #main_window = MainWindow(screensize)
    #main_window.show()
    sys.exit(app.exec_())