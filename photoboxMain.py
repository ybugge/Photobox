import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from PhotoboxPages.MainWindow import MainWindow
from config.Config import cfgValue, CfgKey
import os

if __name__ == '__main__':
    cfgValue[CfgKey.IS_PI] = False
    #Check: OS = RasPi
    if(os.uname()[4].startswith("arm")):
        cfgValue[CfgKey.IS_PI] = True
        cfgValue[CfgKey.APPLICATION_CURSOR_HINT] = True

    app = QtWidgets.QApplication(sys.argv)
    screensize = app.desktop().availableGeometry().size()

    if(cfgValue[CfgKey.APPLICATION_CURSOR_HINT]):
        app.setOverrideCursor(QCursor(Qt.BlankCursor))
    main_window = MainWindow(screensize)
    main_window.show()
    sys.exit(app.exec_())
