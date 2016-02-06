# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modif_task.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TaskDialog(object):
    def setupUi(self, TaskDialog):
        TaskDialog.setObjectName("TaskDialog")
        TaskDialog.resize(364, 144)
        self.widget = QtWidgets.QWidget(TaskDialog)
        self.widget.setGeometry(QtCore.QRect(1, 4, 361, 141))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.taskNameEdit = QtWidgets.QLineEdit(self.widget)
        self.taskNameEdit.setMinimumSize(QtCore.QSize(220, 25))
        self.taskNameEdit.setObjectName("taskNameEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.taskNameEdit)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setEnabled(False)
        self.label_2.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setEnabled(False)
        self.comboBox.setMinimumSize(QtCore.QSize(220, 28))
        self.comboBox.setObjectName("comboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setEnabled(False)
        self.label_3.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBox_2 = QtWidgets.QComboBox(self.widget)
        self.comboBox_2.setEnabled(False)
        self.comboBox_2.setMinimumSize(QtCore.QSize(220, 28))
        self.comboBox_2.setObjectName("comboBox_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_2)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.saveButton = QtWidgets.QPushButton(self.widget)
        self.saveButton.setMinimumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.saveButton.setFont(font)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.closeButton = QtWidgets.QPushButton(self.widget)
        self.closeButton.setMinimumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.closeButton.setFont(font)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TaskDialog)
        self.closeButton.clicked.connect(TaskDialog.close)
        QtCore.QMetaObject.connectSlotsByName(TaskDialog)

    def retranslateUi(self, TaskDialog):
        _translate = QtCore.QCoreApplication.translate
        TaskDialog.setWindowTitle(_translate("TaskDialog", "Dialog"))
        self.label.setText(_translate("TaskDialog", "New Task"))
        self.label_2.setText(_translate("TaskDialog", "Subtask Of"))
        self.label_3.setText(_translate("TaskDialog", "Category"))
        self.saveButton.setText(_translate("TaskDialog", "Add Task"))
        self.closeButton.setText(_translate("TaskDialog", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TaskDialog = QtWidgets.QDialog()
    ui = Ui_TaskDialog()
    ui.setupUi(TaskDialog)
    TaskDialog.show()
    sys.exit(app.exec_())

