from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtQuick import QQuickView

from src.movableqmlwindow import MovableQmlWindow


class OverlayWidget(MovableQmlWindow):
    def __init__(self):
        super().__init__()
        self.model = None
        self.setColor(QColor(Qt.transparent))
        self.setResizeMode(QQuickView.SizeRootObjectToView)

    def setup(self, model, qml_file_path):
        self.model = model
        self.rootContext().setContextProperty('dataModel', self.model)
        self.setSource(QUrl.fromLocalFile(qml_file_path))
