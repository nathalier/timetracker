__author__ = 'Nathalie'

import sys
from PyQt4 import QtCore, QtGui
from time import time

from dbconnector import *
from mainform import Ui_MainWindow


TP_TODAY = 'Today'
TP_YESTERDAY = 'Yesterday'
TP_THIS_WEEK = 'This Week'
TP_LAST_WEEK = 'Last Week'
TP_THIS_MONTH = 'This Month'
TP_LAST_MONTH = 'Last Month'
TP_LIST = [TP_TODAY, TP_YESTERDAY, TP_THIS_WEEK, TP_LAST_WEEK, TP_THIS_MONTH, TP_LAST_MONTH]
TP_DEF = TP_TODAY
LABEL_START = "Start"
LABEL_STOP = "Pause"


class TtForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.task_started = False
        self.timer_start = 0
        self.time_spent = 0
        self.ui.startStop_btn.clicked.connect(self.start_btn_clicked)

        self.task_combo_init()
        self.tp_combo_init()

        # QtCore.QObject.connect(self.ui.startStop_btn, QtCore.SIGNAL("clicked()"), self.start_or_stop)
        # QtCore.CObject.connect(self.ui.currentTask_cb, QtCore.SIGNAL(""))

    def start_btn_clicked(self):
        self.task_started = not self.task_started
        if self.task_started:
            new_btn_title = LABEL_STOP
            self.timer_start = time()
            self.time_spent = 0
        else:
            new_btn_title = LABEL_START
            self.time_spent = time() - self.timer_start
            self.timer_start = 0
            self.ui.timeFromStart_lb.setText(str(int(self.time_spent)) + ' s')
        self.ui.startStop_btn.setText(new_btn_title)

        return

    def task_combo_init(self):
        tasks = retrieve_tasks()
        self.ui.task_combo.addItems(tasks)
        self.ui.task_combo.setAutoCompletion(True)
        self.ui.task_combo.setEditable(False)

    def tp_combo_init(self):
        self.ui.tp_combo.addItems(TP_LIST)
        ind = self.ui.tp_combo.findText(TP_TODAY)
        if ind >= 0:
            self.ui.tp_combo.setCurrentIndex(ind)
        self.ui.tp_combo.setAutoCompletion(True)
        self.ui.tp_combo.setEditable(False)

    def start_or_stop(self):
        pass





if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = TtForm()
    myapp.show()
    sys.exit(app.exec_())