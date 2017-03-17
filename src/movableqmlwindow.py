from PyQt5.QtCore import Qt
from PyQt5.QtQuick import QQuickView


class MovableQmlWindow(QQuickView):
    def __init__(self):
        super(MovableQmlWindow, self).__init__(None)
        self.setFlags(Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.startPos = self.position()

    def mousePressEvent(self, event):
        self.startPos = event.pos()

    def mouseMoveEvent(self, event):
        if int(event.buttons()) & Qt.LeftButton != 0:
            self.setPosition(self.position() + event.pos() - self.startPos)
            event.accept()
