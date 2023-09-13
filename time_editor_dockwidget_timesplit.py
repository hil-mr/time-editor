
import os

from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'time_editor_dockwidget_timesplit_base.ui'))


class TimeSplitDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    abortTimesplit = pyqtSignal()
    requestCopy = pyqtSignal()

    def __init__(self, doc_string=None, date_string=None, parent=None):
        """Constructor."""
        super(TimeSplitDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        if doc_string:
            self.labelDocContent.setText(doc_string)
        if date_string: 
            self.labelDateContent.setText(date_string)
        self.cancelButton.clicked.connect(self.abortTimesplit.emit)
        self.proceedButton.clicked.connect(self.proceedEvent)

    def closeEvent(self, event):
        self.abortTimesplit.emit()
        event.accept()

    def proceedEvent(self, event):
        self.requestCopy.emit()