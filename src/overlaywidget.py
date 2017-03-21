from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QColor

from src.movableqmlwindow import MovableQmlWindow


class OverlayWidget(MovableQmlWindow):
    def __init__(self):
        super(OverlayWidget, self).__init__()
        self.setColor(QColor(255, 255, 255, 0))
        self.model = None

    def setup(self, model, qml_file_path):
        self.model = model
        self.rootContext().setContextProperty('dataModel', self.model)
        self.setSource(QUrl.fromLocalFile(qml_file_path))
