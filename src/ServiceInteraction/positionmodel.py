from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt


class PositionModel(QAbstractItemModel):
    def __init__(self, weekend_info):
        super(PositionModel, self).__init__(None)
        self.weekendInfo = weekend_info

    def roleNames(self):
        return {Qt.UserRole: bytearray(b'position'), Qt.UserRole + 1: bytearray(b'name')}

    def rowCount(self, parent_index=None, *args, **kwargs):
        if not parent_index.isValid():
            for i in range(self.weekendInfo.car_max):
                if self.weekendInfo.cars[i] is None:
                    return i

            return self.weekendInfo.car_max
        else:
            return 0

    def columnCount(self, parent_index=None, *args, **kwargs):
        if parent_index.isValid():
            return 0
        else:
            return 1

    def index(self, row, column, parent_index=None, *args, **kwargs):
        if not parent_index.isValid():
            return self.createIndex(row, column, parent_index)
        else:
            return QModelIndex()

    def parent(self, index=None):
        return QModelIndex()

    def data(self, index, role=None):
        if role == Qt.UserRole:
            return self.weekendInfo.cars[index.row()].position
        elif role == Qt.UserRole + 1:
            car = self.weekendInfo.cars[index.row()]
            return self.weekendInfo.drivers[car.user_id].name
        else:
            return None
