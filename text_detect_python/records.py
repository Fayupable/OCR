# -*- coding: utf-8 -*-
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QObject, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView

from records_auto import Ui_MainWindow

class ShutDownTrigger(QObject):
    trigger = pyqtSignal(bool)


class RecordViewModel(QAbstractTableModel):
    def __init__(self, data):
        super(RecordViewModel, self).__init__()
        self._data = data
        self._headers = ["Market", "Tarih", "Ürün", "Fiyat"]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            elif orientation == Qt.Vertical:
                return section + 1
        return QVariant()


class Records(QMainWindow, Ui_MainWindow):
    shutdown_trigger = ShutDownTrigger()

    def __init__(self, data):
        super(Records, self).__init__()
        self.setupUi(self)
        productModel = RecordViewModel(data)
        self.productRecordsTable.setModel(productModel)
        self.productRecordsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.actionUpload.triggered.connect(self.onMenuAction)

    def closeEvent(self, event):
        self.shutdown_trigger.trigger.emit(True)
        event.accept()

    def onMenuAction(self):
        self.shutdown_trigger.trigger.emit(False)
        self.destroy()

