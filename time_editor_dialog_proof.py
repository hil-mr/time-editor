# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'time_editor_dialog_proof.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TimeEditorDialogProof(object):
    def setupUi(self, TimeEditorDialogProof):
        TimeEditorDialogProof.setObjectName("TimeEditorDialogProof")
        TimeEditorDialogProof.resize(630, 387)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(TimeEditorDialogProof)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(TimeEditorDialogProof)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(TimeEditorDialogProof)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_3 = QtWidgets.QLabel(TimeEditorDialogProof)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.textEdit = QtWidgets.QTextEdit(TimeEditorDialogProof)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(TimeEditorDialogProof)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(TimeEditorDialogProof)
        self.buttonBox.accepted.connect(TimeEditorDialogProof.accept)
        self.buttonBox.rejected.connect(TimeEditorDialogProof.reject)
        QtCore.QMetaObject.connectSlotsByName(TimeEditorDialogProof)

    def retranslateUi(self, TimeEditorDialogProof):
        _translate = QtCore.QCoreApplication.translate
        TimeEditorDialogProof.setWindowTitle(_translate("TimeEditorDialogProof", "Add Proof"))
        self.label.setText(_translate("TimeEditorDialogProof", "Proof Date (YYYY-MM-DD)"))
        self.label_3.setText(_translate("TimeEditorDialogProof", "Dokumentation"))

