# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'time_editor_dialog_expand.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TimeEditorDialogExpand(object):
    def setupUi(self, TimeEditorDialogExpand):
        TimeEditorDialogExpand.setObjectName("TimeEditorDialogExpand")
        TimeEditorDialogExpand.resize(630, 387)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(TimeEditorDialogExpand)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(TimeEditorDialogExpand)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.comboBox = QtWidgets.QComboBox(TimeEditorDialogExpand)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        self.label = QtWidgets.QLabel(TimeEditorDialogExpand)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(TimeEditorDialogExpand)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_3 = QtWidgets.QLabel(TimeEditorDialogExpand)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.textEdit = QtWidgets.QTextEdit(TimeEditorDialogExpand)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(TimeEditorDialogExpand)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(TimeEditorDialogExpand)
        self.buttonBox.accepted.connect(TimeEditorDialogExpand.accept) # type: ignore
        self.buttonBox.rejected.connect(TimeEditorDialogExpand.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(TimeEditorDialogExpand)

    def retranslateUi(self, TimeEditorDialogExpand):
        _translate = QtCore.QCoreApplication.translate
        TimeEditorDialogExpand.setWindowTitle(_translate("TimeEditorDialogExpand", "Expand Time Span"))
        self.label_2.setText(_translate("TimeEditorDialogExpand", "TODO: Zeige Werte für Feature und vorhergehendes und nachfolgendes"))
        self.comboBox.setItemText(0, _translate("TimeEditorDialogExpand", "Life Start"))
        self.comboBox.setItemText(1, _translate("TimeEditorDialogExpand", "Life End"))
        self.label.setText(_translate("TimeEditorDialogExpand", "Expand Date (YYYY-MM-DD)"))
        self.label_3.setText(_translate("TimeEditorDialogExpand", "Dokumentation"))
