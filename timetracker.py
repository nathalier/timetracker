__author__ = 'Nathalie'

import sys
from PyQt5 import QtCore, QtWidgets
from datetime import datetime, date, timedelta
from time import time
from functools import partial

from dbconnector import *
from mainform import Ui_MainWindow
from modif_task import Ui_TaskDialog


TP_TODAY = 'Today'
TP_YESTERDAY = 'Yesterday'
TP_THIS_WEEK = 'This Week'
TP_THIS_MONTH = 'This Month'
TP_LAST_7 = 'Last 7 Days'
TP_LAST_30 = 'Last 30 Days'
TP_LIST = [TP_TODAY, TP_YESTERDAY, TP_THIS_WEEK, TP_LAST_7, TP_THIS_MONTH, TP_LAST_30]
TP_DEF = TP_TODAY
LABEL_START = "Start"
LABEL_STOP = "Stop"
TU_SECOND = 1
TU_MINUTE = 60 * TU_SECOND
TU_5MIN = 5 * TU_MINUTE
TU_HOUR = 60 * TU_MINUTE
TIMER_TIMEOUT = TU_SECOND


class TtForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.ui.actionLayer.setChecked(True)
        self.task_started = False
        self.timer_start = 0
        self.time_current = 0
        self.cur_task, self.cur_task_id = '', -1
        self.cur_period = TP_DEF
        self.cur_dialog = None
        prepare_db()
        self.saved_states = retrieve_saved_state()
        self.task_combo_init()
        self.tp_combo_init()
        self.timer = QtCore.QTimer()

        self.timer.timeout.connect(self.tick)
        self.ui.startStop_btn.clicked.connect(self.start_btn_clicked)
        self.ui.task_combo.currentIndexChanged.connect(self.new_task_selected)
        self.ui.tp_combo.currentIndexChanged.connect(self.new_period_selected)

        self.ui.actionAddTask.triggered.connect(partial(self.open_dialog, 'AddTaskDialog'))
        self.ui.actionLayer.triggered.connect(self.toggle_ontop)


    def tick(self):
        self.time_current += TIMER_TIMEOUT
        # self.ui.timeFromStart_lb.setText(self.time_to_str(self.time_current, TIMER_TIMEOUT))
        self.ui.cur_time.display(str(timedelta(seconds=self.time_current))) #self.time_current. toString('hh:mm:ss'))

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
        time_spent = time() - self.timer_start
        if abs(time_spent - self.time_current) > TIMER_TIMEOUT:
            if time_spent < 0: time_spent = 0
            # TODO show error, propose to correct time
        log_time(self.cur_task_id, self.timer_start, self.timer_start + time_spent, time_spent, offline_l=0)
        self.timer.stop()
        self.time_current = 0
        self.task_started = False
        self.ui.startStop_btn.setText(LABEL_START)
        self.update_time_for_cur_period()

    def update_time_for_cur_period(self):
        # TODO period definition
        if self.cur_task_id > 0:
            start_t, end_t = self.period_to_timestamp(self.cur_period)
            total_time = select_time(self.cur_task_id, start_t, end_t)
            total_time_lb = self.time_to_str(total_time, TU_SECOND)
        else:
            total_time_lb = '0m'
        self.ui.totalForPeriod_lb.setText(total_time_lb)
        if self.task_started:
            # self.ui.timeFromStart_lb.setText(self.time_to_str(self.time_current, TIMER_TIMEOUT))
            self.ui.cur_time.display(str(timedelta(seconds=self.time_current)))
        else:
            # self.ui.timeFromStart_lb.setText('0m')
            self.ui.cur_time.display('0:00')

    def new_task_selected(self):
        if self.task_started:
            self.stop_tracking()
        self.proceed_selected_task()

    def proceed_selected_task(self):
        t_name = self.ui.task_combo.currentText()
        if len(t_name) == 0:
            self.cur_task, self.cur_task_id = '', -1
        else:
            self.cur_task, self.cur_task_id = t_name, self.all_tasks[t_name]
        self.update_time_for_cur_period()

    def find_task_by_id(self, task_id):
        for t_name, t_id in self.all_tasks.items():
            if t_id == task_id:
                return t_name

    def update_task_combo(self):
        last_task_id = self.cur_task_id
        self.ui.task_combo.clear()
        self.task_combo_init(last_task_id)
    
    def task_combo_init(self, cur_task_id=-1):
        self.all_tasks = retrieve_tasks()
        self.ui.task_combo.addItems(sorted(self.all_tasks.keys(), key=lambda t: t.lower()))
        try:
            if cur_task_id < 0:
                t_id = int(self.saved_states['last_task_id'])
            else:
                t_id = cur_task_id
            combo_text = self.find_task_by_id(t_id)
        except:
            combo_text = ''
        self.ui.task_combo.setCurrentText(combo_text)
        self.proceed_selected_task()
        self.ui.task_combo.setEditable(False)

    def tp_combo_init(self):
        self.ui.tp_combo.addItems(TP_LIST)
        ind = self.ui.tp_combo.findText(self.cur_period)
        if ind >= 0:
            self.ui.tp_combo.setCurrentIndex(ind)
        self.ui.tp_combo.setEditable(False)

    def new_period_selected(self):
        new_period = self.ui.tp_combo.currentText()
        for period in TP_LIST:
            if new_period == period:
                self.cur_period = period
        self.update_time_for_cur_period()

    def closeEvent(self, event):
        if self.task_started:
            self.stop_tracking()
        save_cur_state([('last_task_id', str(self.cur_task_id))])
        self.cur_dialog.close()
        event.accept()

    def named_period_to_gmtime(self, period):
        if period == TP_TODAY:
            pass
            # return ( , time())

    def period_to_timestamp(self, period = TP_DEF):
        if period == TP_TODAY:
            start_t = datetime.combine(date.today(), datetime.min.time()).timestamp()
            end_t = datetime.now().timestamp()
        elif period == TP_YESTERDAY:
            start_t = datetime.combine(date.today() - timedelta(days=1), datetime.min.time()).timestamp()
            end_t = datetime.combine(date.today(), datetime.min.time()).timestamp()
        elif period == TP_THIS_WEEK:
            start_t = datetime.combine(date.today() - timedelta(days=date.today().weekday()), datetime.min.time()).timestamp()
            end_t = datetime.now().timestamp()
        elif period == TP_THIS_MONTH:
            start_t = datetime.combine(date.today() - timedelta(days=date.today().day - 1), datetime.min.time()).timestamp()
            end_t = datetime.now().timestamp()
        elif period == TP_LAST_7:
            start_t = datetime.combine(date.today() - timedelta(days=7), datetime.min.time()).timestamp()
            end_t = datetime.now().timestamp()
        elif period == TP_LAST_30:
            start_t = datetime.combine(date.today() - timedelta(days=30), datetime.min.time()).timestamp()
            end_t = datetime.now().timestamp()
        else:
            # TODO SHOW ERROR
            start_t, end_t = 0, 0
        return (start_t, end_t)

    def time_to_str(self, time_amount, rounding_unit=TU_5MIN):
        result = ''
        time_rounded = round(time_amount / rounding_unit) * rounding_unit
        h, m = divmod(time_rounded, TU_HOUR)
        m, s = divmod(m, TU_MINUTE)
        if h > 0: result += str(h) + 'h '
        result += str(m) + 'm '
        if s > 0: result += str(s) + 's'
        return result

    def open_dialog(self, dial_name):
        constructor = globals()[dial_name]
        dialog = constructor()
        self.cur_dialog = dialog
        self.last_ontop_val = self.ui.actionLayer.isChecked()
        if self.last_ontop_val:
            self.toggle_ontop(False)
        self.ui.menubar.setEnabled(False)
        self.cur_dialog.task_added_s.connect(self.update_task_combo)
        self.cur_dialog.dialog_closed_s.connect(self.dialog_closed)
        dialog.show()
        dialog.exec()

    def dialog_closed(self):
        self.cur_dialog.task_added_s.disconnect(self.update_task_combo)
        self.cur_dialog.dialog_closed_s.disconnect(self.dialog_closed)
        self.cur_dialog = None
        self.ui.menubar.setEnabled(True)
        if self.last_ontop_val:
            self.toggle_ontop(True)

    def toggle_ontop(self, new_val=True):
        if self.ui.actionLayer.isChecked() and new_val:
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        self.show()


class AddTaskDialog(QtWidgets.QDialog, Ui_TaskDialog):
    task_added_s = QtCore.pyqtSignal()
    dialog_closed_s = QtCore.pyqtSignal()

    def __init__(self):
        super(AddTaskDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Add New Task')
        self.saveButton.setText('Add Task')
        self.taskNameEdit.setText('')
        self.init_cat_combo()
        self.init_parent_tasks()
        self.saveButton.clicked.connect(self.add_btn_clicked)
        self.addcloseButton.clicked.connect(self.add_close_btn_clicked)
        self.category_combo.currentIndexChanged.connect(self.filter_ptasks)
        self.ptask_combo.currentIndexChanged.connect(self.set_category)

    def init_cat_combo(self):
        self.category_combo.addItem('')
        self.categories = retrieve_categories()
        self.category_combo.addItems(sorted(self.categories.keys(), key=lambda c: c.lower()))

    def init_parent_tasks(self):
        self.ptask_combo.addItem('')
        self.ptasks_with_id, self.ptasks_with_cat = retrieve_super_tasks_with_cat()
        self.ptask_combo.addItems(sorted(self.ptasks_with_id.keys(), key=lambda c: c.lower()))

    def filter_ptasks(self):
        last_task = self.ptask_combo.currentText()
        if last_task == ['']: return
        new_task_list = ['']
        if self.category_combo.currentText() == '':
            new_task_list.extend(sorted(self.ptasks_with_id.keys(), key=lambda c: c.lower()))
        else:
            filtered_tasks, cur_cat = [], self.category_combo.currentText()
            for task, cat in self.ptasks_with_cat.items():
                if cat == cur_cat:
                    filtered_tasks.append(task)
            new_task_list.extend(sorted(filtered_tasks, key=lambda c: c.lower()))
        self.ptask_combo.currentIndexChanged.disconnect(self.set_category)
        self.ptask_combo.clear()
        self.ptask_combo.addItems(new_task_list)
        cur_task = last_task if last_task in new_task_list else ''
        self.ptask_combo.setCurrentText(cur_task)
        self.ptask_combo.currentIndexChanged.connect(self.set_category)

    def set_category(self):
        ptask_new = self.ptask_combo.currentText()
        last_cat = self.category_combo.currentText()
        if ptask_new == '': return
        if last_cat == '' or last_cat != self.ptasks_with_cat[ptask_new]:
            self.category_combo.currentIndexChanged.disconnect(self.filter_ptasks)
            self.category_combo.setCurrentText(self.ptasks_with_cat[ptask_new])
            self.category_combo.currentIndexChanged.connect(self.filter_ptasks)

    def add_btn_clicked(self):
        if self.taskNameEdit.text().strip() != '':
            cur_ptask, cur_cat = self.ptask_combo.currentText(), self.category_combo.currentText()
            ptask_id = self.ptasks_with_id[cur_ptask] if len(cur_ptask) > 0 else None
            cat_id = self.categories[cur_cat] if len(cur_cat) > 0 else None
            if add_task(self.taskNameEdit.text(), ptask_id, cat_id):
                self.ptask_combo.clear()
                self.init_parent_tasks()
                self.task_added_s.emit()
                self.taskNameEdit.setText('')
            else:
                pass
#             TODO show error
        else:
            pass
    #     TODO ask to enter task name

    def add_close_btn_clicked(self):
        self.add_btn_clicked()
        self.close()

    def closeEvent(self, QCloseEvent):
        self.dialog_closed_s.emit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = TtForm()
    myapp.show()
    sys.exit(app.exec())