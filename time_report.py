# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'time_report.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ReportMainWindow(object):
    def setupUi(self, ReportMainWindow):
        ReportMainWindow.setObjectName("ReportMainWindow")
        ReportMainWindow.resize(661, 448)
        self.centralwidget = QtWidgets.QWidget(ReportMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.startDateTime = QtWidgets.QDateTimeEdit(self.groupBox)
        self.startDateTime.setMinimumSize(QtCore.QSize(0, 25))
        self.startDateTime.setCurrentSection(QtWidgets.QDateTimeEdit.DaySection)
        self.startDateTime.setCalendarPopup(True)
        self.startDateTime.setObjectName("startDateTime")
        self.gridLayout.addWidget(self.startDateTime, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.stopDateTime = QtWidgets.QDateTimeEdit(self.groupBox)
        self.stopDateTime.setMinimumSize(QtCore.QSize(0, 25))
        self.stopDateTime.setCalendarPopup(True)
        self.stopDateTime.setObjectName("stopDateTime")
        self.gridLayout.addWidget(self.stopDateTime, 1, 2, 1, 1)
        self.tp_combo = QtWidgets.QComboBox(self.groupBox)
        self.tp_combo.setMinimumSize(QtCore.QSize(0, 25))
        self.tp_combo.setObjectName("tp_combo")
        self.gridLayout.addWidget(self.tp_combo, 0, 0, 2, 1)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 3)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMinimumSize(QtCore.QSize(45, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.cat_combo = QtWidgets.QComboBox(self.centralwidget)
        self.cat_combo.setMinimumSize(QtCore.QSize(0, 25))
        self.cat_combo.setObjectName("cat_combo")
        self.horizontalLayout.addWidget(self.cat_combo)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3, 0, QtCore.Qt.AlignHCenter)
        self.task_combo = QtWidgets.QComboBox(self.centralwidget)
        self.task_combo.setMinimumSize(QtCore.QSize(0, 25))
        self.task_combo.setObjectName("task_combo")
        self.horizontalLayout.addWidget(self.task_combo)
        self.withSubTaskCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.withSubTaskCheckBox.setEnabled(False)
        self.withSubTaskCheckBox.setObjectName("withSubTaskCheckBox")
        self.horizontalLayout.addWidget(self.withSubTaskCheckBox)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 6)
        self.horizontalLayout.setStretch(4, 2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.reportWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.reportWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.reportWidget.setObjectName("reportWidget")
        self.reportWidget.setColumnCount(0)
        self.reportWidget.setRowCount(0)
        self.verticalLayout_2.addWidget(self.reportWidget)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 7)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setEnabled(True)
        self.searchButton.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.searchButton.setFont(font)
        self.searchButton.setObjectName("searchButton")
        self.verticalLayout.addWidget(self.searchButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.sumDetButton = QtWidgets.QPushButton(self.centralwidget)
        self.sumDetButton.setMinimumSize(QtCore.QSize(80, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sumDetButton.setFont(font)
        self.sumDetButton.setObjectName("sumDetButton")
        self.verticalLayout.addWidget(self.sumDetButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)
        self.addTimeButton = QtWidgets.QPushButton(self.centralwidget)
        self.addTimeButton.setMinimumSize(QtCore.QSize(80, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.addTimeButton.setFont(font)
        self.addTimeButton.setObjectName("addTimeButton")
        self.verticalLayout.addWidget(self.addTimeButton)
        self.editTimeButton = QtWidgets.QPushButton(self.centralwidget)
        self.editTimeButton.setMinimumSize(QtCore.QSize(80, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.editTimeButton.setFont(font)
        self.editTimeButton.setObjectName("editTimeButton")
        self.verticalLayout.addWidget(self.editTimeButton)
        self.deleteTimeButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteTimeButton.setMinimumSize(QtCore.QSize(80, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.deleteTimeButton.setFont(font)
        self.deleteTimeButton.setObjectName("deleteTimeButton")
        self.verticalLayout.addWidget(self.deleteTimeButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem4)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem5)
        self.printButton = QtWidgets.QPushButton(self.centralwidget)
        self.printButton.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.printButton.setFont(font)
        self.printButton.setObjectName("printButton")
        self.verticalLayout.addWidget(self.printButton)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem6)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setMinimumSize(QtCore.QSize(80, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.closeButton.setFont(font)
        self.closeButton.setObjectName("closeButton")
        self.verticalLayout.addWidget(self.closeButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.setStretch(0, 5)
        self.horizontalLayout_2.setStretch(1, 1)
        ReportMainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ReportMainWindow)
        self.closeButton.clicked.connect(ReportMainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(ReportMainWindow)

    def retranslateUi(self, ReportMainWindow):
        _translate = QtCore.QCoreApplication.translate
        ReportMainWindow.setWindowTitle(_translate("ReportMainWindow", "Reports"))
        self.groupBox.setTitle(_translate("ReportMainWindow", "Period"))
        self.label_4.setText(_translate("ReportMainWindow", "Since"))
        self.startDateTime.setDisplayFormat(_translate("ReportMainWindow", "dd-MMM-yyyy hh:mm"))
        self.label_5.setText(_translate("ReportMainWindow", "To"))
        self.stopDateTime.setDisplayFormat(_translate("ReportMainWindow", "dd-MMM-yyyy hh:mm"))
        self.label_2.setText(_translate("ReportMainWindow", "Category"))
        self.label_3.setText(_translate("ReportMainWindow", "Task"))
        self.withSubTaskCheckBox.setText(_translate("ReportMainWindow", "Including Subtasks"))
        self.searchButton.setText(_translate("ReportMainWindow", "Show Report"))
        self.sumDetButton.setText(_translate("ReportMainWindow", "Summary"))
        self.addTimeButton.setText(_translate("ReportMainWindow", "Add"))
        self.editTimeButton.setText(_translate("ReportMainWindow", "Edit"))
        self.deleteTimeButton.setText(_translate("ReportMainWindow", "Delete"))
        self.printButton.setText(_translate("ReportMainWindow", "Print to ..."))
        self.closeButton.setText(_translate("ReportMainWindow", "Close"))
