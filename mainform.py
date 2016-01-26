# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainform.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(372, 94)
        MainWindow.setWindowOpacity(0.6)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 371, 73))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.mainLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.mainLayout.setObjectName(_fromUtf8("mainLayout"))
        self.currentTask_cb = QtGui.QComboBox(self.gridLayoutWidget)
        self.currentTask_cb.setMinimumSize(QtCore.QSize(0, 25))
        self.currentTask_cb.setObjectName(_fromUtf8("currentTask_cb"))
        self.mainLayout.addWidget(self.currentTask_cb, 0, 1, 1, 2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.runningForText = QtGui.QLabel(self.gridLayoutWidget)
        self.runningForText.setIndent(10)
        self.runningForText.setObjectName(_fromUtf8("runningForText"))
        self.horizontalLayout_2.addWidget(self.runningForText)
        self.timeFromStart_lb = QtGui.QLabel(self.gridLayoutWidget)
        self.timeFromStart_lb.setIndent(10)
        self.timeFromStart_lb.setObjectName(_fromUtf8("timeFromStart_lb"))
        self.horizontalLayout_2.addWidget(self.timeFromStart_lb)
        self.mainLayout.addLayout(self.horizontalLayout_2, 1, 3, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.Period_cb = QtGui.QComboBox(self.gridLayoutWidget)
        self.Period_cb.setMinimumSize(QtCore.QSize(180, 0))
        self.Period_cb.setObjectName(_fromUtf8("Period_cb"))
        self.horizontalLayout.addWidget(self.Period_cb)
        self.totalForPeriod_lb = QtGui.QLabel(self.gridLayoutWidget)
        self.totalForPeriod_lb.setIndent(10)
        self.totalForPeriod_lb.setObjectName(_fromUtf8("totalForPeriod_lb"))
        self.horizontalLayout.addWidget(self.totalForPeriod_lb)
        self.mainLayout.addLayout(self.horizontalLayout, 1, 1, 1, 2)
        self.startStop_btn = QtGui.QPushButton(self.gridLayoutWidget)
        self.startStop_btn.setMinimumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.startStop_btn.setFont(font)
        self.startStop_btn.setObjectName(_fromUtf8("startStop_btn"))
        self.mainLayout.addWidget(self.startStop_btn, 0, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 372, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuReport = QtGui.QMenu(self.menubar)
        self.menuReport.setObjectName(_fromUtf8("menuReport"))
        MainWindow.setMenuBar(self.menubar)
        self.actionDay = QtGui.QAction(MainWindow)
        self.actionDay.setObjectName(_fromUtf8("actionDay"))
        self.actionWeek = QtGui.QAction(MainWindow)
        self.actionWeek.setObjectName(_fromUtf8("actionWeek"))
        self.actionMonth = QtGui.QAction(MainWindow)
        self.actionMonth.setObjectName(_fromUtf8("actionMonth"))
        self.menuReport.addAction(self.actionDay)
        self.menuReport.addAction(self.actionWeek)
        self.menuReport.addAction(self.actionMonth)
        self.menubar.addAction(self.menuReport.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.runningForText.setText(_translate("MainWindow", "Running for:", None))
        self.timeFromStart_lb.setText(_translate("MainWindow", "0 m", None))
        self.totalForPeriod_lb.setText(_translate("MainWindow", "0 m", None))
        self.startStop_btn.setText(_translate("MainWindow", "Start", None))
        self.menuReport.setTitle(_translate("MainWindow", "Report", None))
        self.actionDay.setText(_translate("MainWindow", "Day", None))
        self.actionWeek.setText(_translate("MainWindow", "Week", None))
        self.actionMonth.setText(_translate("MainWindow", "Month", None))

