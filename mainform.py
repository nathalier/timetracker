# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainform.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(412, 128)
        MainWindow.setWindowOpacity(0.7)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setHorizontalSpacing(10)
        self.mainLayout.setVerticalSpacing(5)
        self.mainLayout.setObjectName("mainLayout")
        self.task_combo = QtWidgets.QComboBox(self.centralwidget)
        self.task_combo.setMinimumSize(QtCore.QSize(230, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.task_combo.setFont(font)
        self.task_combo.setToolTipDuration(-1)
        self.task_combo.setObjectName("task_combo")
        self.mainLayout.addWidget(self.task_combo, 0, 1, 1, 2, QtCore.Qt.AlignVCenter)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cur_time = QtWidgets.QLCDNumber(self.centralwidget)
        self.cur_time.setMinimumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.cur_time.setFont(font)
        self.cur_time.setDigitCount(8)
        self.cur_time.setObjectName("cur_time")
        self.horizontalLayout_2.addWidget(self.cur_time)
        self.mainLayout.addLayout(self.horizontalLayout_2, 1, 3, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tp_combo = QtWidgets.QComboBox(self.centralwidget)
        self.tp_combo.setMinimumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tp_combo.setFont(font)
        self.tp_combo.setToolTipDuration(-1)
        self.tp_combo.setObjectName("tp_combo")
        self.horizontalLayout.addWidget(self.tp_combo, 0, QtCore.Qt.AlignVCenter)
        self.totalForPeriod_lb = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.totalForPeriod_lb.setFont(font)
        self.totalForPeriod_lb.setIndent(10)
        self.totalForPeriod_lb.setObjectName("totalForPeriod_lb")
        self.horizontalLayout.addWidget(self.totalForPeriod_lb, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.mainLayout.addLayout(self.horizontalLayout, 1, 1, 1, 2)
        self.startStop_btn = QtWidgets.QPushButton(self.centralwidget)
        self.startStop_btn.setMinimumSize(QtCore.QSize(120, 30))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.startStop_btn.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.startStop_btn.setFont(font)
        self.startStop_btn.setObjectName("startStop_btn")
        self.mainLayout.addWidget(self.startStop_btn, 0, 3, 1, 1, QtCore.Qt.AlignVCenter)
        self.verticalLayout.addLayout(self.mainLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 412, 21))
        self.menubar.setObjectName("menubar")
        self.menuReport = QtWidgets.QMenu(self.menubar)
        self.menuReport.setObjectName("menuReport")
        self.menuTasks = QtWidgets.QMenu(self.menubar)
        self.menuTasks.setObjectName("menuTasks")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuToDo = QtWidgets.QMenu(self.menubar)
        self.menuToDo.setObjectName("menuToDo")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionDay = QtWidgets.QAction(MainWindow)
        self.actionDay.setObjectName("actionDay")
        self.actionWeek = QtWidgets.QAction(MainWindow)
        self.actionWeek.setObjectName("actionWeek")
        self.actionMonth = QtWidgets.QAction(MainWindow)
        self.actionMonth.setObjectName("actionMonth")
        self.actionAddTask = QtWidgets.QAction(MainWindow)
        self.actionAddTask.setObjectName("actionAddTask")
        self.actionDeleteTask = QtWidgets.QAction(MainWindow)
        self.actionDeleteTask.setObjectName("actionDeleteTask")
        self.actionModifyTask = QtWidgets.QAction(MainWindow)
        self.actionModifyTask.setObjectName("actionModifyTask")
        self.actionTaskReport = QtWidgets.QAction(MainWindow)
        self.actionTaskReport.setObjectName("actionTaskReport")
        self.actionLogTime = QtWidgets.QAction(MainWindow)
        self.actionLogTime.setObjectName("actionLogTime")
        self.actionAddMemo = QtWidgets.QAction(MainWindow)
        self.actionAddMemo.setObjectName("actionAddMemo")
        self.actionLayer = QtWidgets.QAction(MainWindow)
        self.actionLayer.setCheckable(True)
        self.actionLayer.setObjectName("actionLayer")
        self.actionOpacity = QtWidgets.QAction(MainWindow)
        self.actionOpacity.setObjectName("actionOpacity")
        self.actionPeriodReport = QtWidgets.QAction(MainWindow)
        self.actionPeriodReport.setObjectName("actionPeriodReport")
        self.actionEditTime = QtWidgets.QAction(MainWindow)
        self.actionEditTime.setObjectName("actionEditTime")
        self.actionAddToDo = QtWidgets.QAction(MainWindow)
        self.actionAddToDo.setObjectName("actionAddToDo")
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.menuReport.addAction(self.actionTaskReport)
        self.menuReport.addAction(self.actionPeriodReport)
        self.menuTasks.addAction(self.actionAddTask)
        self.menuTasks.addAction(self.actionModifyTask)
        self.menuTasks.addSeparator()
        self.menuTasks.addAction(self.actionLogTime)
        self.menuTasks.addAction(self.actionEditTime)
        self.menuTasks.addSeparator()
        self.menuTasks.addAction(self.actionAddMemo)
        self.menuSettings.addAction(self.actionLayer)
        self.menuSettings.addAction(self.actionOpacity)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionPreferences)
        self.menuToDo.addAction(self.actionAddToDo)
        self.menuToDo.addSeparator()
        self.menuToDo.addAction(self.actionImport)
        self.menuToDo.addAction(self.actionExport)
        self.menubar.addAction(self.menuTasks.menuAction())
        self.menubar.addAction(self.menuReport.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuToDo.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Time Tracker"))
        self.totalForPeriod_lb.setText(_translate("MainWindow", "0m"))
        self.startStop_btn.setText(_translate("MainWindow", "Start"))
        self.menuReport.setTitle(_translate("MainWindow", "Report"))
        self.menuTasks.setTitle(_translate("MainWindow", "Tasks"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuToDo.setTitle(_translate("MainWindow", "ToDo"))
        self.actionDay.setText(_translate("MainWindow", "Day"))
        self.actionWeek.setText(_translate("MainWindow", "Week"))
        self.actionMonth.setText(_translate("MainWindow", "Month"))
        self.actionAddTask.setText(_translate("MainWindow", "Add Task"))
        self.actionAddTask.setShortcut(_translate("MainWindow", "Ctrl++"))
        self.actionDeleteTask.setText(_translate("MainWindow", "Delete"))
        self.actionModifyTask.setText(_translate("MainWindow", "Modify Task"))
        self.actionTaskReport.setText(_translate("MainWindow", "For Task"))
        self.actionTaskReport.setShortcut(_translate("MainWindow", "Ctrl+T"))
        self.actionLogTime.setText(_translate("MainWindow", "Log Time"))
        self.actionAddMemo.setText(_translate("MainWindow", "Add Memo"))
        self.actionAddMemo.setShortcut(_translate("MainWindow", "Ctrl+M"))
        self.actionLayer.setText(_translate("MainWindow", "Always on Top"))
        self.actionOpacity.setText(_translate("MainWindow", "Opacity"))
        self.actionPeriodReport.setText(_translate("MainWindow", "For Period"))
        self.actionPeriodReport.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.actionEditTime.setText(_translate("MainWindow", "Edit Time"))
        self.actionAddToDo.setText(_translate("MainWindow", "Add ToDo"))
        self.actionImport.setText(_translate("MainWindow", "Import..."))
        self.actionExport.setText(_translate("MainWindow", "Export..."))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences..."))

