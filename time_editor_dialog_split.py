# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'time_editor_dialog_split.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TimeEditorDialogBase(object):
    def setupUi(self, TimeEditorDialogBase):
        TimeEditorDialogBase.setObjectName("TimeEditorDialogBase")
        TimeEditorDialogBase.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(TimeEditorDialogBase)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(TimeEditorDialogBase)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(TimeEditorDialogBase)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_2 = QtWidgets.QLabel(TimeEditorDialogBase)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.textEdit = QtWidgets.QTextEdit(TimeEditorDialogBase)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.button_box = QtWidgets.QDialogButtonBox(TimeEditorDialogBase)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.verticalLayout_2.addWidget(self.button_box)

        self.retranslateUi(TimeEditorDialogBase)
        self.button_box.accepted.connect(TimeEditorDialogBase.accept)
        self.button_box.rejected.connect(TimeEditorDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(TimeEditorDialogBase)

    def retranslateUi(self, TimeEditorDialogBase):
        _translate = QtCore.QCoreApplication.translate
        TimeEditorDialogBase.setWindowTitle(_translate("TimeEditorDialogBase", "Time Split Features"))
        self.label.setText(_translate("TimeEditorDialogBase", "Date Selection (YYYY-MM-DD)"))
        self.label_2.setText(_translate("TimeEditorDialogBase", "Docstring"))

