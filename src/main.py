from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlEngine, QQmlComponent

from src.ServiceInteraction.reader import DataReader

if __name__ == '__main__':
    app = QGuiApplication([])
    engine = QQmlEngine()
    engine.rootContext().setContextProperty("dataReader", DataReader())
    component = QQmlComponent(engine, 'qml/main.qml')
    rootWindow = component.create(engine.rootContext())
    app.exec()
