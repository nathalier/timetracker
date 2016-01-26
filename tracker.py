__author__ = 'Nathalie'

import sys
from PyQt4 import QtCore, QtGui

from dbconnector import pull_data
from mainform import Ui_MainWindow


class TtForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # QtCore.QObject.connect(self.ui.startStop_btn, QtCore.SIGNAL("clicked()"), self.start_or_stop)
        # QtCore.CObject.connect(self.ui.currentTask_cb, QtCore.SIGNAL(""))

    def start_or_stop(self):
        pass





if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = TtForm()
    myapp.show()
    pull_data()
    sys.exit(app.exec_())