# -*- coding: utf-8 -*-
import json
import os.path
import re

import torch.cuda
from PyQt5.QtCore import QRegularExpression, Qt, QDate, QThread
from PyQt5.QtGui import QPixmap, QRegularExpressionValidator
from PyQt5.QtWidgets import (QMainWindow, QHeaderView, QFileDialog, QApplication, QTableWidgetItem,
                             QLineEdit, QItemDelegate, QMessageBox, QMenu, QAction)

from mainwindow_auto import Ui_MainWindow
from addrowdialog import AddRowDialog
from records import Records
from settings import Settings
from db import *
import sys

from worker import Worker


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
        self.saveButton.clicked.connect(self.submitProducts)
        self.actionKayitlar.triggered.connect(self.redirectToRecords)
        self.actionAyarlar.triggered.connect(self.openSettings)
        self.productTable.setItemDelegate(ValidatorDelegate())
        header = self.productTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        self.record_window = None
        self.startup = True
        self.imageMenu = QMenu(self)
        try:
            with open("assets/settings.json") as json_file:
                json_obj = json.load(json_file)
                self.imagePaths = json_obj["recent_files"]
                self.use_gpu = json_obj["use_gpu"]
        except FileNotFoundError:
            self.imagePaths = list()
            self.use_gpu = False
        self.updateMenu()
        self.recentImgToolButton.setMenu(self.imageMenu)

        self.worker = None
        self.thread = None
        connectToDB()

    def closeEvent(self, event):
        if not os.path.exists("assets"):
            os.makedirs("assets")
        with open("assets/settings.json", "w") as json_file:
            settings = {"recent_files": self.imagePaths, "use_gpu": self.use_gpu}
            json.dump(settings, json_file, indent=4)
        closeConnection()
        event.accept()

    def submitProducts(self):
        products = list()
        shop = self.marketLE.text().strip()
        date = self.dateEdit.date().toString("dd/MM/yyyy")

        pattern = r"(\d{1,3}[.,\s]?\d{0,3})\s*K[C]?[G]?\s*[xX\s]\s*(\d{1,3}[.,\s]?\d{0,2})\s*TL[\/I]?[K]?[G]?\s*(.+?)\s*[%]?[#l1]?(\d+)|(.+?)\s*[%#l1](\d+)\s*[xX]\s*(\d{1,3}[.,\s]?\d{0,2})\s*TL\s*(\d{1,3}[.,\s]?\d{0,3})\s*K[CG]?\s*(.+?)\s*[%#l1]?(\d+)"
        for row in range(self.productTable.rowCount()):
            product_name = self.productTable.item(row, 0).text()
            try:
                product_price = float(self.productTable.item(row, 1).text().replace(",", "."))
            except ValueError:
                product_price = float(self.productTable.item(row, 1).text().replace(" ", "."))
            match = re.search(pattern, product_name)
            if match:
                product_name = match.group(3)
                product_price = float(match.group(2).replace(",", "."))

            products.append({"shop": shop, "date": date, "product_name": product_name, "price": product_price})
        left_out_products = dbInsert(products)
        msgBox = QMessageBox()
        if left_out_products:
            msgBox.setText("Ürün kaydı gerçekleşti fakat aşağıdaki ürünler veritabanına kaydedilemedi.\n"
                           "Bu ürünler halihazırda veritabanında benzer fiyatlarla bulunuyor olabilir.\n"
                           "Kaydedilemeyen ürünler:\n" + left_out_products)
        else:
            msgBox.setText("Ürünlerin tamamı veritabanına kaydedildi.")
        msgBox.setWindowTitle("Ürün Kaydı")
        msgBox.exec_()

    def redirectToRecords(self):
        if self.record_window is None:
            products = dbGetAll()

            data = [
                [product["shop"], product["date"], product["product_name"], product["price"]]
                for product in products
            ]
            self.record_window = Records(data)
            self.record_window.shutdown_trigger.trigger.connect(self.onRecordsDestroyed)
        if not self.record_window.isVisible():
            self.record_window.show()
            self.hide()

    def openSettings(self):
        setting_dialog = Settings()
        setting_dialog.gpu_trigger.trigger.connect(self.setGpuUsage)
        setting_dialog.exec_()
        setting_dialog.gpu_trigger.trigger.disconnect()

    def setGpuUsage(self, gpu):
        self.use_gpu = gpu
        json_file = open("assets/settings.json")
        json_obj = json.load(json_file)
        json_obj["use_gpu"] = self.use_gpu
        json_file.close()
        with open("assets/settings.json", "w") as settings:
            json.dump(json_obj, settings, indent=4)

    def onRecordsDestroyed(self, shutdown):
        if shutdown:
            self.close()
        else:
            self.record_window = None
            self.show()

    def loadImage(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.gif)")
        self.loadImageInternal(file_path, False)

    def loadImageInternal(self, file_path, repeat):
        if file_path:
            if self.startup is False and repeat is False and file_path == self.imagePaths[0]:
                QMessageBox.warning(self, "Uyarı!", "Bu dosya halihazırda ekranda okunmuş halde görülebilir.")
                return
            elif file_path in self.imagePaths:
                self.imagePaths.remove(file_path)
            elif len(self.imagePaths) >= 8:
                self.imagePaths.pop()
            self.imagePaths.insert(0, file_path)
            self.updateMenu()
            if self.startup is True:
                self.startup = False

            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.photoLabel.setPixmap(pixmap.scaled(self.photoLabel.size(),
                                                        Qt.KeepAspectRatio, Qt.SmoothTransformation))

                self.setButtonStates(False)
                self.worker = Worker(file_path, self.use_gpu)
                self.thread = QThread()
                self.worker.moveToThread(self.thread)
                self.thread.started.connect(self.worker.run)
                self.thread.finished.connect(self.handleEmptyTable)
                self.worker.result_signal.signal.connect(self.fillProductsTable)
                self.worker.finish_signal.signal.connect(self.worker.deleteLater)
                self.worker.finish_signal.signal.connect(self.thread.quit)
                self.worker.finish_signal.signal.connect(self.thread.wait)
                self.thread.start()
            else:
                QMessageBox.warning(self, "Hatalı Dosya",
                                    "Seçtiğiniz dosya yüklenemedi. Lütfen başka bir dosya seçin.")

    def fillProductsTable(self, date_str, store, products):
        error_str = ""
        if date_str:
            date = QDate.fromString(date_str, "dd/MM/yyyy")
            self.dateEdit.setDate(date)
        else:
            error_str += "Mevcut backend ile fiş üzerindeki tarih okunamadı.\n"

        if store:
            self.marketLE.setText(store)
        else:
            error_str += "Mevcut backend ile fişin alındığı market okunamadı."

        if error_str:
            QMessageBox.warning(self, "Eksik Okuma", error_str)

        row_position = self.productTable.rowCount()
        if row_position > 0:
            self.productTable.setRowCount(0)
        for product in products:
            product_name = product["Product"]
            if "Weight" in product:
                price = product["Price per KG"]
            elif "Quantity" in product:
                price = product["Price per Unit"]
            else:
                price = product["Price"]
            self.productTable.insertRow(row_position)
            self.productTable.setItem(row_position, 0, QTableWidgetItem(product_name))
            self.productTable.setItem(row_position, 1, QTableWidgetItem(price))
            row_position += 1
        self.setButtonStates(True)

    def handleEmptyTable(self):
        if self.productTable.rowCount() == 0 and torch.cuda.is_available():
            backend_str = "GPU" if self.use_gpu else "CPU"
            fallback_str = "CPU" if self.use_gpu else "GPU"
            result = QMessageBox.question(self, "Boş Sepet", f"{backend_str} backend'i ile herhangi bir ürün "
                                                             f"okunamadı.\n"
                                                             f"{fallback_str} backend'i ile tekrar denemek ister "
                                                             f"misiniz?")
            if result == QMessageBox.Yes:
                backend_is_gpu = False if self.use_gpu else True
                self.setGpuUsage(backend_is_gpu)
                self.loadImageInternal(self.imagePaths[0], True)

    def setButtonStates(self, status):
        self.deleteButton.setEnabled(status)
        self.saveButton.setEnabled(status)
        self.addButton.setEnabled(status)

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
                action.triggered.connect(lambda checked, arg=path: self.loadImageInternal(arg, False))
                self.imageMenu.addAction(action)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
