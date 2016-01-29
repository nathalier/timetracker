__author__ = 'Nathalie'

import sys
from PyQt4 import QtCore, QtGui
from time import time, strftime, gmtime

from dbconnector import *
from mainform import Ui_MainWindow


TP_TODAY = 'Today'
TP_YESTERDAY = 'Yesterday'
TP_THIS_WEEK = 'This Week'
TP_THIS_MONTH = 'This Month'
TP_LIST = [TP_TODAY, TP_YESTERDAY, TP_THIS_WEEK, TP_THIS_MONTH]
TP_DEF = TP_TODAY
LABEL_START = "Start"
LABEL_STOP = "Stop"
TU_SECOND = 1
TU_MINUTE = 60 * TU_SECOND
TU_5MIN = 5 * TU_MINUTE
TU_HOUR = 60 * TU_MINUTE
TIMER_TIMEOUT = TU_SECOND


class TtForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.task_started = False
        self.timer_start = 0
        self.time_current = 0
        self.current_task_id = -1   # tuple of two values: [0] - task_id, [1] - task_name
        prepare_db()
        self.all_tasks, self.saved_states = init_db()
        self.task_combo_init()
        self.tp_combo_init()
        self.timer = QtCore.QTimer()

        self.timer.timeout.connect(self.tick)
        self.ui.startStop_btn.clicked.connect(self.start_btn_clicked)
        self.ui.task_combo.currentIndexChanged.connect(self.new_task_selected)

    def tick(self):
        self.time_current += TIMER_TIMEOUT
        self.ui.timeFromStart_lb.setText(self.time_to_str(self.time_current, TIMER_TIMEOUT))

    def start_btn_clicked(self):
        if not self.task_started:
            self.start_tracking()
        else:
            self.stop_tracking()

    def start_tracking(self):
        self.timer_start = time()
        self.timer.start(1000 * TIMER_TIMEOUT)
        self.task_started = True
        self.ui.startStop_btn.setText(LABEL_STOP)

    def stop_tracking(self):
        log_time(self.current_task_id, int(self.timer_start), int(time()))
        self.timer.stop()
        self.time_current = 0
        self.task_started = False
        self.ui.startStop_btn.setText(LABEL_START)
        self.update_time_for_period()

    def update_time_for_period(self):
        # TODO period definition
        if self.current_task_id > 0:
            total_time = select_time(self.current_task_id, TP_TODAY)
            total_time_lb = self.time_to_str(total_time, TU_SECOND)
        else:
            total_time_lb = '0m'
        self.ui.totalForPeriod_lb.setText(total_time_lb)
        self.ui.timeFromStart_lb.setText('0m')

    def new_task_selected(self):
        if self.task_started:
            self.stop_tracking()
        self.proceed_selected_task()

    def proceed_selected_task(self):
        t_name = self.ui.task_combo.currentText()
        if len(t_name) == 0:
            self.current_task_id = -1
        else:
            self.current_task_id = self.find_task_id_by_name(t_name)
        self.update_time_for_period()

    def find_task_id_by_name(self, task_name):
        for id, t_name in self.all_tasks.items():
            if t_name == task_name:
                return id

    def task_combo_init(self):
        for id, t_name in self.all_tasks.items():
            self.ui.task_combo.addItem(t_name)
        try:
        # if 'last_task_id' in self.saved_states and int(self.saved_states['last_task_id']) in self.all_tasks:
            t_id = int(self.saved_states['last_task_id'])
            combo_ind = self.ui.task_combo.findText(self.all_tasks[t_id])
        except:
            combo_ind = 0
        self.ui.task_combo.setCurrentIndex(combo_ind)
        self.proceed_selected_task()
        self.ui.task_combo.setAutoCompletion(True)
        self.ui.task_combo.setEditable(False)

    def tp_combo_init(self):
        self.ui.tp_combo.addItems(TP_LIST)
        ind = self.ui.tp_combo.findText(TP_TODAY)
        if ind >= 0:
            self.ui.tp_combo.setCurrentIndex(ind)
        self.ui.tp_combo.setAutoCompletion(True)
        self.ui.tp_combo.setEditable(False)

    def closeEvent(self, event):
        if self.task_started:
            self.stop_tracking()
        save_cur_state([('last_task_id', str(self.current_task_id))])
        event.accept()


    def time_to_str(self, time_amount, rounding_unit=TU_5MIN):
        result = ''
        time_rounded = round(time_amount / rounding_unit) * rounding_unit
        h, m = divmod(time_rounded, TU_HOUR)
        m, s = divmod(m, TU_MINUTE)
        if h > 0: result += str(h) + 'h '
        result += str(m) + 'm '
        if s > 0: result += str(s) + 's'
        return result







if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = TtForm()
    myapp.show()
    sys.exit(app.exec_())