from PyQt5.QtWidgets import QTableWidgetItem

__author__ = 'Nathalie'

import sys
from PyQt5 import QtCore, QtWidgets
from datetime import datetime, date, timedelta
from time import time
from functools import partial

from dbconnector import *
from mainform import Ui_MainWindow
from modif_task import Ui_TaskDialog
from add_memo import Ui_MemoDialog
from time_report import Ui_ReportMainWindow


TP_TODAY = 'Today'
TP_YESTERDAY = 'Yesterday'
TP_THIS_WEEK = 'This Week'
TP_THIS_MONTH = 'This Month'
TP_LAST_7 = 'Last 7 Days'
TP_LAST_30 = 'Last 30 Days'
TP_All_TIME = 'All Time'
all_time_start = 0
TP_LIST = [TP_TODAY, TP_YESTERDAY, TP_THIS_WEEK, TP_LAST_7, TP_THIS_MONTH, TP_LAST_30, TP_All_TIME]
TP_DEF = TP_TODAY
LABEL_START, LABEL_STOP = "Start", "Stop"
TU_SECOND = 1
TU_MINUTE = 60 * TU_SECOND
TU_5MIN = 5 * TU_MINUTE
TU_HOUR = 60 * TU_MINUTE
TIMER_TIMEOUT = TU_SECOND * 200 #in ms
TIME_REPORT, TASK_REPORT = 1, 2
NULL_CAT, NULL_TASK = '', ''
REPORT_CUSTOM_TP, REPORT_ALL_CAT, REPORT_ALL_TASK = 'Custom', 'All', 'All'


def period_to_timestamp(period = TP_DEF):
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
    elif period == TP_All_TIME:
        start_t = all_time_start
        end_t = datetime.now().timestamp()
    else:
        # TODO SHOW ERROR
        start_t, end_t = 0, 0
    return (start_t, end_t)

def time_to_str(time_amount, rounding_unit=TU_5MIN):
    result = ''
    time_rounded = round(time_amount / rounding_unit) * rounding_unit
    h, m = divmod(time_rounded, TU_HOUR)
    m, s = divmod(m, TU_MINUTE)
    if h > 0: result += str(h) + 'h '
    result += str(m) + 'm '
    if s > 0: result += str(s) + 's'
    return result


class TtForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.ui.memo_text_lb = QtWidgets.QLabel(self.ui.centralwidget, text='')
        self.statusBar.addWidget(self.ui.memo_text_lb)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.ui.actionLayer.setChecked(True)
        self.task_started = False
        self.timer_start = 0
        self.cur_task, self.cur_task_id = NULL_TASK, -1
        self.cur_period = TP_DEF
        self.cur_dialog = None
        prepare_db()
        self.saved_states = retrieve_saved_state()
        all_time_start = float(self.saved_states.get('all_time_start', '0'))
        # TODO correct it when manually added/edited time reports
        self.task_combo_init()
        self.tp_combo_init()
        self.timer = QtCore.QTimer()

        self.timer.timeout.connect(self.tick)
        self.ui.startStop_btn.clicked.connect(self.start_btn_clicked)
        self.ui.task_combo.currentIndexChanged.connect(self.new_task_selected)
        self.ui.tp_combo.currentIndexChanged.connect(self.new_period_selected)

        self.ui.actionAddTask.triggered.connect(partial(self.open_dialog, 'AddTaskDialog'))
        self.ui.actionAddMemo.triggered.connect(partial(self.open_dialog, 'MemoDialog'))
        self.ui.actionPeriodReport.triggered.connect(partial(self.open_dialog, 'ReportMainWindow', TIME_REPORT))
        self.ui.actionTaskReport.triggered.connect(partial(self.open_dialog, 'ReportMainWindow', TASK_REPORT))
        self.ui.actionLayer.triggered.connect(self.toggle_ontop)


    def tick(self):
        delta = time() - self.timer_start
        self.ui.cur_time.display(str(timedelta(seconds=round(delta))))

    def start_btn_clicked(self):
        if not self.task_started:
            self.start_tracking()
        else:
            self.stop_tracking()

    def start_tracking(self):
        self.timer_start = time()
        self.timer.start(TIMER_TIMEOUT)
        self.task_started = True
        self.ui.startStop_btn.setText(LABEL_STOP)

    def stop_tracking(self):
        time_spent = time() - self.timer_start
        if time_spent < 0: time_spent = 0
            # TODO show error, propose to correct time
        log_time(self.cur_task_id, self.timer_start, self.timer_start + time_spent, time_spent, offline_l=0)
        self.timer.stop()
        self.task_started = False
        self.ui.startStop_btn.setText(LABEL_START)
        self.update_time_for_cur_period()

    def update_time_for_cur_period(self):
        # TODO period definition
        if self.cur_task_id > 0:
            start_t, end_t = period_to_timestamp(self.cur_period)
            total_time = select_time(self.cur_task_id, start_t, end_t)
            total_time_lb = time_to_str(total_time, TU_SECOND)
        else:
            total_time_lb = '0m'
        self.ui.totalForPeriod_lb.setText(total_time_lb)
        if self.task_started:
            self.ui.cur_time.display(str(timedelta(seconds=round(time() - self.timer_start))))
        else:
            self.ui.cur_time.display('0:00:00')

    def new_task_selected(self):
        if self.task_started:
            self.stop_tracking()
        self.proceed_selected_task()

    def proceed_selected_task(self):
        t_name = self.ui.task_combo.currentText()
        if len(t_name) == 0:
            self.cur_task, self.cur_task_id = NULL_TASK, -1
        else:
            self.cur_task, self.cur_task_id = t_name, self.all_tasks[t_name]
        self.update_time_for_cur_period()
        self.show_last_memo()

    def find_task_by_id(self, task_id):
        for t_name, t_id in self.all_tasks.items():
            if t_id == task_id:
                return t_name

    def update_task_combo(self):
        last_task_id = self.cur_task_id
        self.ui.task_combo.clear()
        self.task_combo_init(last_task_id)
    
    def task_combo_init(self, cur_task_id=-1):
        self.all_tasks = get_tasks()
        self.ui.task_combo.addItems(sorted(self.all_tasks.keys(), key=lambda t: t.lower()))
        try:
            if cur_task_id < 0:
                t_id = int(self.saved_states['last_task_id'])
            else:
                t_id = cur_task_id
            combo_text = self.find_task_by_id(t_id)
        except:
            combo_text = NULL_TASK
        self.ui.task_combo.setCurrentText(combo_text)
        self.proceed_selected_task()

    def tp_combo_init(self):
        self.ui.tp_combo.addItems(TP_LIST)
        ind = self.ui.tp_combo.findText(self.cur_period)
        if ind >= 0:
            self.ui.tp_combo.setCurrentIndex(ind)

    def new_period_selected(self):
        new_period = self.ui.tp_combo.currentText()
        for period in TP_LIST:
            if new_period == period:
                self.cur_period = period
        self.update_time_for_cur_period()

    def show_last_memo(self):
        if self.cur_task_id < 0: return
        memo = select_last_memo(self.cur_task_id)
        memo_to_show = '' if memo[0] is None \
            else ('Last Memo (' + str(datetime.fromtimestamp(int(memo[1]))) + '): ' + memo[0])
        self.ui.memo_text_lb.setText(memo_to_show)


    def closeEvent(self, event):
        if self.task_started:
            self.stop_tracking()
        save_cur_state([('last_task_id', str(self.cur_task_id))])
        # self.cur_dialog.close()
        event.accept()


    def open_dialog(self, dial_name, dial_type):
        self.last_ontop_val = self.ui.actionLayer.isChecked()
        if self.last_ontop_val:
            self.toggle_ontop(False)
        self.ui.menubar.setEnabled(False)

        self.cur_dialog_name = dial_name
        constructor = globals()[dial_name]
        if dial_name == 'AddTaskDialog':
            dialog = constructor()
            dialog.task_added_s.connect(self.update_task_combo)
        elif dial_name == 'MemoDialog':
            dialog = constructor(cur_task=self.cur_task, all_tasks=self.all_tasks)
            dialog.memo_added_s.connect(self.show_last_memo)
        elif dial_name == 'ReportMainWindow':
            cur_task = None
            if dial_type == TASK_REPORT:
                ddd = self.cur_task.find('::')
                cur_task = self.cur_task[ddd + 2:]
            dialog = constructor(cur_period=self.cur_period, cur_task=cur_task)
        self.cur_dialog = dialog
        self.cur_dialog.dialog_closed_s.connect(self.dialog_closed)
        dialog.show()
        # dialog.exec()

    def dialog_closed(self):
        if self.cur_dialog_name == 'AddTaskDialog':
            self.cur_dialog.task_added_s.disconnect(self.update_task_combo)
        elif self.cur_dialog_name == 'MemoDialog':
            self.cur_dialog.memo_added_s.disconnect(self.show_last_memo)
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

    def __init__(self, **params):
        super(AddTaskDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Add New Task')
        self.saveButton.setText('Add Task')
        self.taskNameEdit.setText(NULL_TASK)
        self.init_cat_combo()
        self.init_tasks()
        self.saveButton.clicked.connect(self.add_btn_clicked)
        self.addcloseButton.clicked.connect(self.add_close_btn_clicked)
        self.category_combo.currentIndexChanged.connect(self.filter_ptasks)
        self.ptask_combo.currentIndexChanged.connect(self.set_category)

    def init_cat_combo(self):
        self.category_combo.addItem(NULL_CAT)
        self.categories = retrieve_categories()
        self.category_combo.addItems(sorted(self.categories.keys(), key=lambda c: c.lower()))

    def init_tasks(self):
        self.ptask_combo.addItem(NULL_TASK)
        self.ptasks_with_id, self.ptasks_with_cat = get_tasks_with_cat()
        self.ptask_combo.addItems(sorted(self.ptasks_with_id.keys(), key=lambda c: c.lower()))

    def filter_ptasks(self):
        last_task = self.ptask_combo.currentText()
        if last_task == [NULL_TASK]: return
        new_task_list = [NULL_TASK]
        if self.category_combo.currentText() == NULL_CAT:
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
        cur_task = last_task if last_task in new_task_list else NULL_CAT
        self.ptask_combo.setCurrentText(cur_task)
        self.ptask_combo.currentIndexChanged.connect(self.set_category)

    def set_category(self):
        ptask_new = self.ptask_combo.currentText()
        last_cat = self.category_combo.currentText()
        if ptask_new == NULL_TASK: return
        if last_cat == NULL_CAT or last_cat != self.ptasks_with_cat[ptask_new]:
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
                self.init_tasks()
                self.task_added_s.emit()
                self.taskNameEdit.setText(NULL_TASK)
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


class MemoDialog(QtWidgets.QDialog, Ui_MemoDialog):
    memo_added_s = QtCore.pyqtSignal()
    dialog_closed_s = QtCore.pyqtSignal()

    def __init__(self,  **params):
        super(MemoDialog, self).__init__()
        self.setupUi(self)
        self.cur_task, self.all_tasks = params['cur_task'], params['all_tasks']
        self.memoEdit.setText('')
        self.init_task_combo()
        self.saveButton.clicked.connect(self.add_btn_clicked)
        self.clearButton.clicked.connect(self.clear_btn_clicked)

    def init_task_combo(self):
        self.task_combo.addItem(NULL_TASK)
        self.task_combo.addItems(sorted(self.all_tasks.keys(), key=lambda t: t.lower()))
        self.task_combo.setCurrentText(self.cur_task)

    def add_btn_clicked(self):
        if self.memoEdit.toPlainText().strip() != '':
            t_name = self.task_combo.currentText()
            t_id = None if t_name == NULL_TASK else self.all_tasks[t_name]
            if add_memo(self.memoEdit.toPlainText(), time(), t_id):
                self.memo_added_s.emit()
                self.close()
            else:
                pass
#             TODO show error
        else:
            pass
    #     TODO ask to enter memo

    def clear_btn_clicked(self):
        self.memoEdit.setText('')

    def closeEvent(self, QCloseEvent):
        self.dialog_closed_s.emit()


class ReportMainWindow(QtWidgets.QMainWindow, Ui_ReportMainWindow):
    # memo_added_s = QtCore.pyqtSignal()
    dialog_closed_s = QtCore.pyqtSignal()

    def __init__(self, **params):
        super(ReportMainWindow, self).__init__()
        self.setupUi(self)
        self.tasks_with_id, self.tasks_with_cat = get_tasks_with_cat()
        self.cur_period = params['cur_period'] if 'cur_period' in params and params['cur_period'] else REPORT_CUSTOM_TP
        task_to_set = params['cur_task'] if 'cur_task' in params and params['cur_task'] else REPORT_ALL_TASK
        self.cur_task, self.cur_task_ind = task_to_set, 0 if task_to_set == REPORT_ALL_TASK else self.tasks_with_id[task_to_set]
        self.cur_cat = self.tasks_with_cat[task_to_set] if task_to_set != REPORT_ALL_TASK else REPORT_ALL_CAT
        self.task_combo_init()
        self.tp_combo_init()
        self.cat_combo_init()
        self.detailed_flag = False
        self.sumDetButton.setText('Get Detailed')
        self.cat_only_flag = False
        self.reportByCatCheckBox.setChecked(False)

        self.tp_combo.currentIndexChanged.connect(self.adjust_date_time)
        self.startDateTime.dateTimeChanged.connect(self.clear_tp_combo)
        self.stopDateTime.dateTimeChanged.connect(self.clear_tp_combo)
        self.task_combo.currentIndexChanged.connect(self.set_category)
        self.cat_combo.currentIndexChanged.connect(self.filter_tasks)
        self.searchButton.clicked.connect(self.search)
        self.sumDetButton.clicked.connect(self.sum_det_toggle)
        self.reportByCatCheckBox.stateChanged.connect(self.cat_only_toggle)

        self.tp_combo.setCurrentText(self.cur_period)
        self.cat_combo.setCurrentText(self.cur_cat)
        self.task_combo.setCurrentText(task_to_set)
        self.search()

    def tp_combo_init(self):
        self.tp_combo.addItem(REPORT_CUSTOM_TP)
        self.tp_combo.addItems(TP_LIST)

    def cat_combo_init(self):
        self.cat_combo.addItem(REPORT_ALL_CAT)
        self.cat_combo.addItem(NULL_CAT)
        self.categories = retrieve_categories()
        self.cat_combo.addItems(sorted(self.categories.keys(), key=lambda c: c.lower()))

    def task_combo_init(self):
        self.task_combo.addItem(REPORT_ALL_TASK)
        self.task_combo.addItems(sorted(self.tasks_with_id.keys(), key=lambda c: c.lower()))

    def adjust_date_time(self):
        self.searchButton.setEnabled(True)
        self.cur_period = self.tp_combo.currentText()
        if self.cur_period == REPORT_CUSTOM_TP: return
        from PyQt5.QtCore import QDateTime
        start_t, end_t = period_to_timestamp(self.cur_period)
        self.startDateTime.dateTimeChanged.disconnect(self.clear_tp_combo)
        self.stopDateTime.dateTimeChanged.disconnect(self.clear_tp_combo)
        self.startDateTime.setDateTime(QDateTime.fromTime_t(start_t))
        self.stopDateTime.setDateTime(QDateTime.fromTime_t(end_t))
        self.startDateTime.dateTimeChanged.connect(self.clear_tp_combo)
        self.stopDateTime.dateTimeChanged.connect(self.clear_tp_combo)

    def clear_tp_combo(self):
        self.searchButton.setEnabled(True)
        self.tp_combo.currentIndexChanged.disconnect(self.adjust_date_time)
        self.tp_combo.setCurrentText(REPORT_CUSTOM_TP)
        self.cur_period = self.tp_combo.currentText()
        self.tp_combo.currentIndexChanged.connect(self.adjust_date_time)

    def filter_tasks(self):
        self.searchButton.setEnabled(True)
        self.cur_cat = self.cat_combo.currentText()
        new_task_list = [REPORT_ALL_TASK]
        if self.cat_combo.currentText() == REPORT_ALL_CAT:
            new_task_list.extend(sorted(self.tasks_with_id.keys(), key=lambda c: c.lower()))
        else:
            filtered_tasks = []
            for task, cat in self.tasks_with_cat.items():
                if cat == self.cur_cat:
                    filtered_tasks.append(task)
            new_task_list.extend(sorted(filtered_tasks, key=lambda c: c.lower()))
        self.task_combo.currentIndexChanged.disconnect(self.set_category)
        self.task_combo.clear()
        self.task_combo.addItems(new_task_list)
        self.cur_task, self.cur_task_ind = REPORT_ALL_TASK, 0
        self.task_combo.setCurrentText(self.cur_task)
        self.task_combo.currentIndexChanged.connect(self.set_category)

    def set_category(self):
        self.searchButton.setEnabled(True)
        self.cur_task = self.task_combo.currentText()
        self.cur_task_ind = 0 if self.cur_task == REPORT_ALL_TASK else self.tasks_with_id[self.cur_task]
        if self.cur_task == REPORT_ALL_TASK:
            return
        # if self.cur_cat == REPORT_ALL_CAT or self.cur_cat != self.tasks_with_cat[self.cur_task]:
        self.cur_cat = self.tasks_with_cat[self.cur_task]
        self.cat_combo.currentIndexChanged.disconnect(self.filter_tasks)
        self.cat_combo.setCurrentText(self.cur_cat)
        self.cat_combo.currentIndexChanged.connect(self.filter_tasks)

    def sum_det_toggle(self):
        self.detailed_flag = not self.detailed_flag
        new_btn_name = 'Get Summary' if self.detailed_flag else 'Get Detailed'
        self.sumDetButton.setText(new_btn_name)
        self.search()

    def cat_only_toggle(self):
        self.searchButton.setEnabled(True)
        self.cat_only_flag = self.reportByCatCheckBox.isChecked()
        if self.cat_only_flag:
            self.task_combo.setCurrentText(REPORT_ALL_TASK)
            self.task_combo.setEnabled(False)
            # self.withSubTaskCheckBox.setEnabled(False)
        else:
            self.task_combo.setEnabled(True)
            # self.withSubTaskCheckBox.setEnabled(True)

    def search(self):
        self.searchButton.setEnabled(False)
        params = self.construct_search_params()
        columns, data = select_time_report(*params)
        self.reportWidget.setColumnCount(len(columns))
        self.reportWidget.setRowCount(len(data))
        self.reportWidget.setHorizontalHeaderLabels(columns)
        self.reportWidget.setAlternatingRowColors(True)
        if len(columns) > 3:
            self.reportWidget.setColumnWidth(3, 120)
            self.reportWidget.setColumnWidth(2, 120)
        for i, entry in enumerate(data):
            for j, item in enumerate(entry):
                val = QTableWidgetItem(data[i][j])
                self.reportWidget.setItem(i, j, val)

    def construct_search_params(self):
        time_start = self.startDateTime.dateTime().toMSecsSinceEpoch() / 1000
        time_stop = self.stopDateTime.dateTime().toMSecsSinceEpoch() / 1000
        if time_stop < time_start:
            time_stop = time_start
            self.stopDateTime.setDateTime(self.startDateTime.dateTime())
            # TODO show error
        cur_cat = None if self.cur_cat == REPORT_ALL_CAT else self.cur_cat
        cur_task = None if self.cur_task == REPORT_ALL_TASK else self.cur_task
        flag_with_subtasks = self.withSubTaskCheckBox.isChecked()
        flag_detailed = self.detailed_flag
        flag_cat_only = self.reportByCatCheckBox.isChecked()
        return (time_start, time_stop, cur_cat, cur_task, flag_with_subtasks, flag_detailed, flag_cat_only)


    def closeEvent(self, QCloseEvent):
        self.dialog_closed_s.emit()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = TtForm()
    myapp.show()
    sys.exit(app.exec())