import PyQt5.uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from src.ServiceInteraction.data import weekend_info
from src.ServiceInteraction.positionmodel import PositionModel
from src.ServiceInteraction.reader import DataReader
from src.overlaywidget import OverlayWidget

ui_class = PyQt5.uic.loadUiType('gui/mainwindow.ui')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = ui_class[0]()
        self.ui.setupUi(self)

        self.data_reader = DataReader()

        self.ui.actionStart.triggered.connect(self.startReader)
        self.ui.actionStop.triggered.connect(self.stopReader)

        self.mw = OverlayWidget()

    @pyqtSlot()
    def startReader(self):
        self.data_reader.run()
        self.mw.setup(PositionModel(weekend_info), 'qml/EntryList.qml')
        self.mw.show()

    @pyqtSlot()
    def stopReader(self):
        pass


