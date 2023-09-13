# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'time_editor_dialog_inspect.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(596, 505)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkTypeComboBox = QtWidgets.QComboBox(Dialog)
        self.checkTypeComboBox.setObjectName("checkTypeComboBox")
        self.checkTypeComboBox.addItem("")
        self.checkTypeComboBox.addItem("")
        self.checkTypeComboBox.addItem("")
        self.checkTypeComboBox.addItem("")
        self.verticalLayout.addWidget(self.checkTypeComboBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.progressBarFeature = QtWidgets.QProgressBar(Dialog)
        self.progressBarFeature.setProperty("value", 0)
        self.progressBarFeature.setObjectName("progressBarFeature")
        self.verticalLayout.addWidget(self.progressBarFeature)
        self.reportTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.reportTextEdit.setObjectName("reportTextEdit")
        self.verticalLayout.addWidget(self.reportTextEdit)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableWidget)
        self.mQgsFileWidget = gui.QgsFileWidget(Dialog)
        self.mQgsFileWidget.setStorageMode(gui.QgsFileWidget.SaveFile)
        self.mQgsFileWidget.setObjectName("mQgsFileWidget")
        self.verticalLayout.addWidget(self.mQgsFileWidget)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.startButton = QtWidgets.QPushButton(Dialog)
        self.startButton.setObjectName("startButton")
        self.horizontalLayout_3.addWidget(self.startButton)
        self.abortButton = QtWidgets.QPushButton(Dialog)
        self.abortButton.setEnabled(False)
        self.abortButton.setObjectName("abortButton")
        self.horizontalLayout_3.addWidget(self.abortButton)
        self.exportButton = QtWidgets.QPushButton(Dialog)
        self.exportButton.setEnabled(False)
        self.exportButton.setObjectName("exportButton")
        self.horizontalLayout_3.addWidget(self.exportButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Perform Integrity Checks"))
        self.checkTypeComboBox.setItemText(0, _translate("Dialog", "Time Integrity", "time"))
        self.checkTypeComboBox.setItemText(1, _translate("Dialog", "Date Integrity", "date"))
        self.checkTypeComboBox.setItemText(2, _translate("Dialog", "Spatial Integrity", "spatial"))
        self.checkTypeComboBox.setItemText(3, _translate("Dialog", "Geometric Integrity", "geometric"))
        self.tableWidget.setSortingEnabled(False)
        self.startButton.setText(_translate("Dialog", "Start"))
        self.abortButton.setText(_translate("Dialog", "Abort"))
        self.exportButton.setText(_translate("Dialog", "Export CSV"))
from qgis import gui
