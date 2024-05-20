# -*- coding: utf-8 -*-
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QObject, pyqtSignal, QSortFilterProxyModel
from PyQt5.QtWidgets import QMainWindow, QHeaderView
from thefuzz import fuzz

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
        if not index.isValid():
            return QVariant()
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

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class FuzzyFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(FuzzyFilterProxyModel, self).__init__(parent)
        self.filter_text = ""

    def setFilterText(self, text):
        self.filter_text = text
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        if not self.filter_text:
            return True

        model = self.sourceModel()
        # Check only the third column (index 2)
        index = model.index(source_row, 2, source_parent)
        data = model.data(index)
        if data and fuzz.partial_ratio(self.filter_text.lower(),
                                       str(data).lower()) > 85:  # Adjust the ratio threshold as needed
            return True
        return False


class Records(QMainWindow, Ui_MainWindow):
    shutdown_trigger = ShutDownTrigger()

    def __init__(self, data):
        super(Records, self).__init__()
        self.setupUi(self)
        productModel = RecordViewModel(data)
        self.proxyModel = FuzzyFilterProxyModel(self)
        self.proxyModel.setSourceModel(productModel)
        self.productRecordsTable.setModel(self.proxyModel)
        self.productRecordsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.actionUpload.triggered.connect(self.onMenuAction)
        self.searchLE.textChanged.connect(self.proxyModel.setFilterText)

    def closeEvent(self, event):
        self.shutdown_trigger.trigger.emit(True)
        event.accept()

    def onMenuAction(self):
        self.shutdown_trigger.trigger.emit(False)
        self.destroy()
