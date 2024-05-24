# -*- coding: utf-8 -*-
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QObject, pyqtSignal, QSortFilterProxyModel, QModelIndex
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QMessageBox
from thefuzz import fuzz

from records_auto import Ui_MainWindow
from db import dbCompare, exportXML, dbGetAll

chosen_data = list()

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

    def insertRows(self, position, rows, parent=QModelIndex(), data=[]):
        self.beginInsertRows(parent, position, position + rows - 1)
        for i in range(rows):
            if data:
                self._data.insert(position + i, data[i])
            else:
                self._data.insert(position + i, ["", "", "", ""])  # Insert empty row if no data provided
        self.endInsertRows()
        return True

    def addRow(self, row_data=None):
        position = self.rowCount()
        self.insertRows(position, 1, data=[row_data if row_data else ["", "", "", ""]])

    def removeRows(self, position, rows, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in range(rows):
            del self._data[position]
        self.endRemoveRows()
        return True

    def getRowData(self, row):
        if 0 <= row < self.rowCount():
            return self._data[row]
        return None

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
        self.product_filter_text = ""
        self.store_filter_text = ""
        self.chosen_product_text = ""

    def setProductFilter(self, text):
        self.product_filter_text = text
        self.invalidateFilter()

    def setStoreFilter(self, text):
        self.store_filter_text = text
        self.invalidateFilter()

    def setChosenProduct(self, text):
        self.chosen_product_text = text
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()

        if self.store_filter_text and self.store_filter_text != "Hepsi":
            store_index = model.index(source_row, 0, source_parent)
            store_data = model.data(store_index)
            if self.store_filter_text.lower() != str(store_data).lower():
                return False

        product_index = model.index(source_row, 2, source_parent)
        product_data = str(model.data(product_index)).lower()

        if self.product_filter_text and self.chosen_product_text:
            if (fuzz.WRatio(self.product_filter_text, product_data) <= 85 or
                    fuzz.WRatio(self.chosen_product_text, product_data) <= 85):
                return False

        elif self.product_filter_text:
            if fuzz.WRatio(self.product_filter_text, product_data) <= 85:
                return False

        elif self.chosen_product_text:
            if fuzz.WRatio(self.chosen_product_text, product_data) <= 85:
                return False

        return True

    def getColumn(self, column_index):
        model = self.sourceModel()
        if model is None:
            return

        row_count = model.rowCount()

        items = list()
        for row in range(row_count):
            index = model.index(row, column_index)
            item = model.data(index)
            if item is not None and item not in items:
                items.append(item)
        return items

class Records(QMainWindow, Ui_MainWindow):
    shutdown_trigger = ShutDownTrigger()

    def __init__(self, data):
        super(Records, self).__init__()
        self.setupUi(self)
        productModel = RecordViewModel(data)
        self.chosenProductModel = RecordViewModel([])

        self.proxyModel = FuzzyFilterProxyModel(self)
        self.proxyModel.setSourceModel(productModel)
        self.productRecordsTable.setModel(self.proxyModel)
        self.productRecordsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.productRecordsTable.horizontalHeader().setStretchLastSection(True)

        self.chosenProductsTable.setModel(self.chosenProductModel)
        self.chosenProductsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.chosenProductsTable.horizontalHeader().setStretchLastSection(True)

        self.marketComboBox.addItem("Hepsi")
        self.marketComboBox.addItems(self.proxyModel.getColumn(0))
        self.marketComboBox.currentTextChanged.connect(self.proxyModel.setStoreFilter)
        self.actionUpload.triggered.connect(self.onMenuAction)
        self.actionExport.triggered.connect(self.exportToXML)
        self.searchLE.textChanged.connect(self.proxyModel.setProductFilter)

        self.chooseButton.clicked.connect(self.addSelectedRow)
        self.deleteButton.clicked.connect(self.deleteSelectedRow)
        self.compareButton.clicked.connect(self.compareChosenProducts)

    def addSelectedRow(self):
        selected_indexes = self.productRecordsTable.selectionModel().selectedIndexes()
        if selected_indexes:
            proxy_index = selected_indexes[0]
            source_index = self.proxyModel.mapToSource(proxy_index)
            selected_row = source_index.row()
            row_data = self.proxyModel.sourceModel().getRowData(selected_row)

            row_count = self.chosenProductModel.rowCount()
            if row_count == 0:
                self.proxyModel.setChosenProduct(row_data[2])
                self.chosenProductModel.addRow(row_data)
            elif row_count == 1 and row_data != self.chosenProductModel.getRowData(0):
                date1 = self.chosenProductModel.getRowData(0)[1]
                date2 = row_data[1]
                if date1 != date2:
                    self.chosenProductModel.addRow(row_data)
                else:
                    QMessageBox.warning(self, "Aynı Tarihli Ürün", "Aynı tarihte alınmış ürünleri karşılaştıramazsınız.")
            else:
                QMessageBox.warning(self, "Ürün Eklenmiş", "Aynı ürünü tekrar seçemezsiniz.")

    def deleteSelectedRow(self):
        selected_indexes = self.chosenProductsTable.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_row = selected_indexes[0].row()
            self.chosenProductModel.removeRows(selected_row, 1)
        row_count = self.chosenProductModel.rowCount()
        if row_count == 1:
            row_data = self.chosenProductModel.getRowData(0)
            self.proxyModel.setChosenProduct(row_data[2])
        else:
            self.proxyModel.setChosenProduct("")

    def compareChosenProducts(self):
        if self.chosenProductModel.rowCount() == 2:
            product1_arr = self.chosenProductModel.getRowData(0)
            product2_arr = self.chosenProductModel.getRowData(1)
            product1 = {"shop": product1_arr[0], "date": product1_arr[1], "product_name": product1_arr[2], "price": product1_arr[3]}
            product2 = {"shop": product2_arr[0], "date": product2_arr[1], "product_name": product2_arr[2], "price": product2_arr[3]}
            percentage, timediff = dbCompare(product1, product2)
            result_str = f"Aradaki {timediff} günde, bu üründe %{percentage} fiyat değişimi gerçekleşmiş."
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("Fiyat Değişimi")
            msgBox.setText(f"Bu iki ürünü seçtiniz:\n{product1_arr[2]}\n{product2_arr[2]}\n{result_str}")
            msgBox.exec_()

    def exportToXML(self):
        exportXML(dbGetAll())
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Dışarı aktarma")
        msgBox.setText("Veritabanındaki ürünler \"assets/products.xml\" dizinine kaydedildi.")
        msgBox.exec_()

    def clearChosenProducts(self):
        self.chosenProductModel.removeRows(0, 2)

    def closeEvent(self, event):
        self.shutdown_trigger.trigger.emit(True)
        event.accept()

    def onMenuAction(self):
        self.shutdown_trigger.trigger.emit(False)
        self.destroy()
