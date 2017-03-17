import PyQt5.uic
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtQml import QQmlEngine
from PyQt5.QtWidgets import QMainWindow

from src.ServiceInteraction.reader import DataReader
from src.movableqmlwindow import MovableQmlWindow

ui_class = PyQt5.uic.loadUiType('gui/mainwindow.ui')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = ui_class[0]()
        self.ui.setupUi(self)

        self.data_reader = DataReader()

        self.ui.actionStart.triggered.connect(self.startReader)
        self.ui.actionStop.triggered.connect(self.stopReader)

        self.engine = QQmlEngine()
        self.mw = MovableQmlWindow()

    @pyqtSlot()
    def startReader(self):
        #self.data_reader.start()
        self.mw.setSource(QUrl.fromLocalFile('qml/EntryList.qml'))
        self.mw.show()

    def stopReader(self):
        pass


