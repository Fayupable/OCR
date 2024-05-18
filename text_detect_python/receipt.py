# -*- coding: utf-8 -*-
import json
import os.path

import torch.cuda
from PyQt5.QtCore import QRegularExpression, Qt, QDate
from PyQt5.QtGui import QPixmap, QRegularExpressionValidator
from PyQt5.QtWidgets import (QMainWindow, QHeaderView, QFileDialog, QApplication, QTableWidgetItem,
                             QLineEdit, QItemDelegate, QMessageBox, QMenu, QAction)

from mainwindow import Ui_MainWindow
from addrowdialog import AddRowDialog
from safa_yardim import ocr_image, process_receipt
import sys


class ValidatorDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        if index.column() == 1:
            validator = QRegularExpressionValidator(QRegularExpression(r"\d+(\,\d+)?"), editor)
            editor.setValidator(validator)
        return editor


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.chooseButton.clicked.connect(self.loadImage)
        self.addButton.clicked.connect(self.openRowDialog)
        self.deleteButton.clicked.connect(self.deleteRowFromTable)
        self.productTable.setItemDelegate(ValidatorDelegate())
        header = self.productTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        self.imageMenu = QMenu(self)
        try:
            with open("assets/recent_files.json") as json_file:
                self.imagePaths = json.load(json_file)
        except FileNotFoundError:
            self.imagePaths = list()
        self.updateMenu()
        self.recentImgToolButton.setMenu(self.imageMenu)

    def closeEvent(self, event):
        if not os.path.exists("assets"):
            os.makedirs("assets")
        with open("assets/recent_files.json", "w") as json_file:
            json.dump(self.imagePaths, json_file)
        event.accept()

    def loadImage(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.gif)")
        self.loadImageInternal(file_path)

    def loadImageInternal(self, file_path):
        if file_path:
            if file_path in self.imagePaths:
                self.imagePaths.remove(file_path)
            elif len(self.imagePaths) >= 8:
                self.imagePaths.pop()
            self.imagePaths.insert(0, file_path)
            self.updateMenu()

            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.photoLabel.setPixmap(pixmap.scaled(self.photoLabel.size(),
                                                        Qt.KeepAspectRatio, Qt.SmoothTransformation))
                if torch.cuda.is_available():
                    date_str, store, products = process_receipt(ocr_image(file_path, True))
                else:
                    date_str, store, products = process_receipt(ocr_image(file_path, False))

                if date_str:
                    date = QDate.fromString(date_str, "dd/MM/yyyy")
                    self.dateEdit.setDate(date)
                if store:
                    self.marketLE.setText(store)

                row_position = self.productTable.rowCount()
                if row_position > 0:
                    self.productTable.setRowCount(0)
                for product in products:
                    product_name = product["Product"]
                    if "Weight" in product:
                        price = product["Price per KG"]
                    else:
                        price = product["Price"]
                    self.productTable.insertRow(row_position)
                    self.productTable.setItem(row_position, 0, QTableWidgetItem(product_name))
                    self.productTable.setItem(row_position, 1, QTableWidgetItem(price))
                    row_position += 1
            else:
                QMessageBox.warning(self, "Hatalı Dosya",
                                    "Seçtiğiniz dosya yüklenemedi. Lütfen başka bir dosya seçin.")
    def openRowDialog(self):
        dialog = AddRowDialog()
        dialog.trigger.row_trigger.connect(self.addRowToTable)
        dialog.exec_()
        dialog.trigger.row_trigger.disconnect()

    def addRowToTable(self, fields):
        row_position = self.productTable.rowCount()
        self.productTable.insertRow(row_position)
        self.productTable.setItem(row_position, 0, QTableWidgetItem(fields[0]))
        self.productTable.setItem(row_position, 1, QTableWidgetItem(fields[1]))

    def deleteRowFromTable(self):
        selected_indexes = self.productTable.selectedIndexes()
        if selected_indexes:
            selected_row = selected_indexes[0].row()
            self.productTable.removeRow(selected_row)

    def updateMenu(self):
        self.imageMenu.clear()
        if not self.imagePaths is None:
            for path in self.imagePaths:
                action = QAction(path, self)
                action.triggered.connect(lambda checked, arg=path: self.loadImageInternal(arg))
                self.imageMenu.addAction(action)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
