# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'time_editor_dockwidget_timesplit_base.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TimeSplitDockWidget(object):
    def setupUi(self, TimeSplitDockWidget):
        TimeSplitDockWidget.setObjectName("TimeSplitDockWidget")
        TimeSplitDockWidget.resize(669, 404)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.labelDateContent = QtWidgets.QLabel(self.dockWidgetContents)
        self.labelDateContent.setText("")
        self.labelDateContent.setObjectName("labelDateContent")
        self.horizontalLayout.addWidget(self.labelDateContent)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.labelDocContent = QtWidgets.QLabel(self.dockWidgetContents)
        self.labelDocContent.setText("")
        self.labelDocContent.setObjectName("labelDocContent")
        self.horizontalLayout_2.addWidget(self.labelDocContent)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cancelButton = QtWidgets.QPushButton(self.dockWidgetContents)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_3.addWidget(self.cancelButton)
        self.proceedButton = QtWidgets.QPushButton(self.dockWidgetContents)
        self.proceedButton.setObjectName("proceedButton")
        self.horizontalLayout_3.addWidget(self.proceedButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        TimeSplitDockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(TimeSplitDockWidget)
        QtCore.QMetaObject.connectSlotsByName(TimeSplitDockWidget)

    def retranslateUi(self, TimeSplitDockWidget):
        _translate = QtCore.QCoreApplication.translate
        TimeSplitDockWidget.setWindowTitle(_translate("TimeSplitDockWidget", "Timesplit Dock Widget"))
        self.label_3.setText(_translate("TimeSplitDockWidget", "Date"))
        self.label_5.setText(_translate("TimeSplitDockWidget", "Documentation"))
        self.cancelButton.setText(_translate("TimeSplitDockWidget", "Cancel"))
        self.proceedButton.setText(_translate("TimeSplitDockWidget", "Apply Edited Geometries"))
